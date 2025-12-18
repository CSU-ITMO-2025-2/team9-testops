import logging
from confluent_kafka import Consumer
import os
import json
from prometheus_client import start_http_server, Counter

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
NOTIFICATION_QUEUE = 'notification_queue'

# Prometheus metrics
NOTIFICATIONS_SENT = Counter('notifications_sent', 'Number of notifications sent', ['status'])

def listen_for_notifications():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'notification_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'auto.commit.interval.ms': 5000,
    })
    consumer.subscribe([NOTIFICATION_QUEUE])
    print("Notification Service: Listening for messages...")
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                continue

            print(f"Received notification request: {msg.value().decode('utf-8')}")
            try:
                data = json.loads(msg.value().decode('utf-8'))
                send_notification(data)
                NOTIFICATIONS_SENT.labels(status='success').inc()
            except Exception as e:
                logging.error(f"Error processing notification: {e}")
                NOTIFICATIONS_SENT.labels(status='error').inc()
                
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def send_notification(data):
    # Placeholder for actual notification logic (Email, Slack, etc.)
    test_id = data.get('test_id')
    status = data.get('status')
    log = data.get('log', '')
    
    print(f"Sending notification for Test ID: {test_id}, Status: {status}")
    # Example: requests.post(SLACK_WEBHOOK_URL, json={"text": f"Test {test_id} finished with status {status}"})

def main():
    start_http_server(8002) # Different port than consumer
    listen_for_notifications()

if __name__ == "__main__":
    main()
