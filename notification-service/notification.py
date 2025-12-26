import logging
import json
import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from confluent_kafka import Consumer
import uvicorn
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from fastapi import FastAPI, Request, Response

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
NOTIFICATION_QUEUE = 'notification_queue'
PORT = int(os.getenv('PORT', 8002))

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
NOTIFICATIONS_SENT = Counter('notifications_sent', 'Number of notifications sent', ['status'])

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global list of connected clients (queues)
clients = []

async def kafka_listener():
    """Background task to consume Kafka messages and broadcast to SSE clients."""
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'notification_service_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'auto.commit.interval.ms': 5000,
    })
    consumer.subscribe([NOTIFICATION_QUEUE])
    logger.info(f"Connected to Kafka: {KAFKA_BOOTSTRAP_SERVERS}, Topic: {NOTIFICATION_QUEUE}")

    try:
        while True:
            # Consume messages in batches (up to 50 messages at a time)
            msgs = consumer.consume(num_messages=50, timeout=1.0)
            
            if not msgs:
                await asyncio.sleep(0.1)
                continue
            
            for msg in msgs:
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue

                try:
                    payload = msg.value().decode('utf-8')
                    logger.info(f"Received notification: {payload}")
                    data = json.loads(payload)
                    
                    # Update metrics
                    NOTIFICATIONS_SENT.labels(status='success').inc()

                    # Broadcast to all connected clients
                    if clients:
                        logger.info(f"Broadcasting to {len(clients)} clients")
                        # Use a task to not block the consumer loop too much if there are many clients
                        for queue in clients:
                            await queue.put(data)
                    
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    NOTIFICATIONS_SENT.labels(status='error').inc()
                
            # Yield control back to event loop after processing a batch
            await asyncio.sleep(0)
                
    except Exception as e:
        logger.error(f"Kafka listener crashed: {e}")
    finally:
        consumer.close()

@app.on_event("startup")
async def startup_event():
    # Start Kafka listener in background
    asyncio.create_task(kafka_listener())
    
    # Start Prometheus server on separate port if needed, or just relying on uvicorn
    # Since we use 8002 for Uvicorn, we can run Prometheus on 8003 or just expose an endpoint
    # For now, let's keep it simple and maybe skip exposing metrics on a separate port or run it on 8001?
    # Consumer uses 8001. Notification used to use 8002.
    # We will let Uvicorn take 8002.
    pass

@app.get("/stream")
async def message_stream(request: Request):
    """SSE endpoint for streaming notifications."""
    async def event_generator():
        queue = asyncio.Queue()
        clients.append(queue)
        logger.info(f"Client connected. Total clients: {len(clients)}")
        try:
            while True:
                if await request.is_disconnected():
                    break
                data = await queue.get()
                yield {"data": json.dumps(data)}
        except asyncio.CancelledError:
            pass
        finally:
            clients.remove(queue)
            logger.info(f"Client disconnected. Total clients: {len(clients)}")

    return EventSourceResponse(event_generator())

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def readiness():
    return {"status": "ready"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

def main():
    # Run Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
