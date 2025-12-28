# AI TestOps - Distributed Systems Project

[![CI](https://github.com/CSU-ITMO-2025-2/team9-testops/actions/workflows/ci.yml/badge.svg)](https://github.com/CSU-ITMO-2025-2/team9-testops/actions/workflows/ci.yml)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?logo=argo&logoColor=white)](https://argo-cd.readthedocs.io/)
[![Helm](https://img.shields.io/badge/Helm-0F1689?logo=helm&logoColor=white)](https://helm.sh/)
[![GitOps](https://img.shields.io/badge/GitOps-100000?logo=git&logoColor=white)](https://www.gitops.tech/)

> **Курс**: Проектирование и разработка распределенных программных систем  
> **Университет**: ITMO University  
> **Команда**: Truong Huynh Duc

## 📋 Navigation

- [🇷🇺 Русский](#описание-russian)
- [🇺🇸 English](#description-english)

### 📚 Документация


- [📖 Полная документация по развертыванию](DEPLOYMENT.md)
       - Описывает пошаговый процесс установки всех сервисов: подготовка окружения, настройка переменных, запуск через Docker, Helm, и ArgoCD. Включает troubleshooting, примеры команд, и схемы взаимодействия сервисов.
- [🚀 ArgoCD и GitOps](argocd/README.md)
       - Подробно о GitOps workflow: автоматизация деплоя, auto-sync, self-heal, rollback, настройка Application manifests, best practices для production. Примеры интеграции с CI/CD и мониторингом.
- [🔥 Chaos Engineering тесты](chaos-experiments/README.md)
       - Описаны сценарии отказоустойчивости: использование Chaos Mesh, примеры экспериментов (network delay, pod kill, resource stress), анализ результатов, рекомендации по улучшению надежности.
- [🏗️ Структура проекта](PROJECT_STRUCTURE.md)
       - Детализированная схема директорий, описание каждого модуля (api_tests, canvas, home, notification-service, helm, argocd), связи между сервисами, flow данных, точки расширения.
- [🎓 Материалы для защиты](DEFENSE.md)
       - Слайды, схемы архитектуры, demo-сценарии, ответы на типовые вопросы, ссылки на видео/скринкасты, чеклист для подготовки к защите.
- [✅ Чеклист перед защитой](CHECKLIST.md)
       - Контрольный список: покрытие тестами, CI/CD статус, деплой всех сервисов, метрики, документация, демонстрация отказоустойчивости, готовность к вопросам.

---

# Проект AI TestOps

## Описание (Russian)

**AI TestOps** - распределенная система для автоматизации тестирования API с использованием искусственного интеллекта, развернутая в Kubernetes с соблюдением принципов GitOps.

### 🎯 Цель проекта

Демонстрация полноценной распределенной архитектуры с:
- ✅ Микросервисной архитектурой (3+ сервиса)
- ✅ Развертыванием в Kubernetes через Helm
- ✅ GitOps деплоем через ArgoCD
- ✅ CI/CD пайплайном
- ✅ Безопасностью (Secrets, RBAC, NetworkPolicy)
- ✅ Автомасштабированием (HPA)
- ✅ Отказоустойчивостью (Probes, Circuit Breaker)
- ✅ Pub/Sub через Kafka
- ✅ Chaos Engineering тестами

## 🎥 Demo | Демонстрация

Check out the full demo of this project on YouTube:  
Посмотрите полную демонстрацию этого проекта на YouTube:

[![Watch the Demo | Смотреть демонстрацию](https://img.youtube.com/vi/tNE39IoXOoc/maxresdefault.jpg)](https://www.youtube.com/watch?v=tNE39IoXOoc)


**👉 [Click here to watch the full demo on YouTube](https://www.youtube.com/watch?v=tNE39IoXOoc)!**  
**👉 [Нажмите здесь, чтобы посмотреть полную демонстрацию на YouTube](https://www.youtube.com/watch?v=tNE39IoXOoc)!**



### 🏗️ Архитектура

```
┌─────────────┐
│   Ingress   │ ← HTTPS/TLS
└──────┬──────┘
       │
       ├─────────────────┬──────────────────┬─────────────────┐
       │                 │                  │                 │
┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐   ┌─────▼─────┐
│  Django App │   │   Kafka UI  │   │  PostgreSQL │   │  Grafana  │
│  (HPA 2-10) │───│             │   │   (PVC)     │   │   Agent   │
└──────┬──────┘   └─────────────┘   └─────────────┘   └───────────┘
       │
       ```
       ┌─────────────┐      ┌─────────────┐
       │   Client    │────▶│ Django App  │
       └─────────────┘      └─────┬──────┘
                                   ▲                  │
                                   │                  │ REST API / Web UI
                                   │                  ▼
                                   │           ┌─────────────┐
                                   │           │ PostgreSQL  │
                                   │           └─────────────┘
                                   │                  │
                                   │                  ▼
                                   │           ┌─────────────┐
                                   │           │   Kafka     │◀─────────────┐
                                   │           └─────┬──────┘              │
                                   │                 │                     │
                                   │                 ▼                     │
                                   │           ┌─────────────┐             │
                                   │           │ Test Execute│             │
                                   │           │  Consumer   │─────────────┘
                                   │           └─────────────┘
                                   │                 │
                                   │                 ▼
                                   │           ┌─────────────┐
                                   │           │ Notification│
                                   │           │   Service   │
                                   │           └─────────────┘
                                   │
                                   │                 ▼
                                   │           ┌─────────────┐
                                   │           │ Analytics   │
                                   │           │   Runner    │
                                   │           └─────────────┘

       Rollout (Canary/Blue-Green):
              - Uses ArgoCD and Helm to deploy new versions of services (Django App, Consumer, Notification, Analytics) with canary or blue-green strategies, ensuring zero-downtime upgrades.

       KEDA (Autoscaling):
              - KEDA automatically scales Test Execute Consumer based on the number of messages in Kafka (test_run_queue), ensuring high performance under heavy test loads.

       Analytics Run:
              - Analytics Runner receives test results from Kafka or the database, performs analysis (statistics, reporting, anomaly detection), and outputs dashboards or sends alerts.
       ```

```bash
# Применение ArgoCD Application
kubectl apply -f argocd/application.yaml

# Проверка статуса
kubectl get application -n argocd
```

**Готово!** ArgoCD автоматически развернет все микросервисы из Git.

📖 **[Подробная инструкция по развертыванию](DEPLOYMENT.md)**

### ⚙️ Технические требования курса

| Требование | Статус | Реализация |
|-----------|---------|------------|
| 3+ микросервиса | ✅ | Django App, Test Consumer, PostgreSQL, Kafka, Zookeeper |
| Kubernetes + Helm | ✅ | Helm chart в `helm/ai-testops/` |
| GitOps (ArgoCD) | ✅ | Auto-sync, self-heal, prune |
| CI/CD Pipeline | ✅ | GitHub Actions в `.github/workflows/` |
| Secrets/RBAC | ✅ | ServiceAccounts, Roles, NetworkPolicies |
| Autoscaling | ✅ | HPA для Django и Consumer |
| Health Probes | ✅ | Liveness/Readiness для всех сервисов |
| Pub/Sub (Kafka) | ✅ | Асинхронная коммуникация |
| Circuit Breaker | ✅ | Retry/fallback механизмы |
| Chaos Engineering | ✅ | Chaos Mesh эксперименты |

### 📊 Функциональность

- **Автогенерация тестов**: Генерация тестовых скриптов для API на основе Swagger с использованием AI (Gemini)
- **Асинхронное выполнение**: Выполнение тестов через Kafka для масштабируемости
- **Визуализация результатов**: Веб-интерфейс для просмотра результатов тестирования
- **Мониторинг**: Метрики через Grafana Agent и Prometheus
- **API Documentation**: Swagger/OpenAPI интерфейс

## 📦 Содержание

- [🎥 Демонстрация](#-demo--демонстрация)
- [🏗️ Архитектура](#-архитектура)
- [🚀 Быстрый старт](#-быстрый-старт-gitops)
- [📖 Полная документация](DEPLOYMENT.md)
- [🔧 Локальная разработка](#локальная-разработка)
- [🔥 Chaos Testing](#chaos-engineering)
- [👥 Команда](#команда-разработки)

---

## Локальная разработка

### Предварительные требования

- Python 3.12+
- Docker & Docker Compose
- Git

# Team9 TestOps

Distributed API TestOps system for automated API testing, result management, and CI/CD integration. Built with Django, Kafka, PostgreSQL, and supports deployment via Docker, Helm, and ArgoCD.

## Features
---

## System Architecture & Deployment

### Architecture Overview
Team9 TestOps is a modular microservice system for automated API testing. Main components:
- **Django Web App**: API, test management, user interface
- **Test Execution Consumer**: Kafka consumer, executes test cases, collects metrics
- **Notification Service**: Sends notifications on test results/events
- **PostgreSQL**: Persistent storage
- **Kafka**: Message broker for asynchronous test execution
- **Analytics Runner**: Analyzes test results, generates reports/dashboards
- **Helm/ArgoCD**: Deployment and GitOps automation

### Rollout (Canary/Blue-Green)
Uses ArgoCD and Helm to deploy new versions of services (Django App, Consumer, Notification, Analytics) with canary or blue-green strategies, ensuring zero-downtime upgrades and safe rollbacks.

### Autoscaling (KEDA)
KEDA automatically scales Test Execute Consumer based on the number of messages in Kafka (test_run_queue), ensuring high performance under heavy test loads.

### Analytics Run
Analytics Runner receives test results from Kafka or the database, performs analysis (statistics, reporting, anomaly detection), and outputs dashboards or sends alerts.

---

## Documentation
- **Deployment Guide** ([DEPLOYMENT.md]): Step-by-step instructions for installing all services, environment setup, Docker/Helm/ArgoCD usage, troubleshooting, and service interaction diagrams.
- **ArgoCD & GitOps** ([argocd/README.md]): Details on GitOps workflow, auto-sync, self-heal, rollback, Application manifests, production best practices, CI/CD integration, and monitoring.
- **Chaos Engineering** ([chaos-experiments/README.md]): Fault tolerance scenarios using Chaos Mesh, experiment examples (network delay, pod kill, resource stress), result analysis, and reliability recommendations.
- **Project Structure** ([PROJECT_STRUCTURE.md]): Directory map, module descriptions (api_tests, canvas, home, notification-service, helm, argocd), service relationships, data flow, and extension points.
- **Defense Materials** ([DEFENSE.md]): Slides, architecture diagrams, demo scripts, FAQ, video/screencast links, and defense preparation checklist.
- **Pre-Defense Checklist** ([CHECKLIST.md]): Test coverage, CI/CD status, service deployment, metrics, documentation, fault tolerance demo, and Q&A readiness.

## Project Structure
```
team9-testops/
├── api_tests/           # API test logic, generators, views, models
│   ├── generators/      # Gemini, OpenAI, LLM modules
│   ├── migrations/      # Django migrations
│   └── ...
├── canvas/              # Django project settings, URLs, ASGI/WSGI
├── home/                # User management, homepage
├── notification-service # Notification microservice
├── helm/                # Helm charts for deployment
├── argocd/              # ArgoCD manifests
├── static/, staticfiles/# Static assets (CSS, JS)
├── templates/           # HTML templates
├── Dockerfile           # Main Docker build file
├── requirements.txt     # Python dependencies
├── manage.py            # Django management script
├── watch.py             # Kafka consumer for test execution
└── test-execute-consumer/Dockerfile # Consumer Dockerfile
```

## Getting Started
### Prerequisites
- Python 3.12+
- Docker
- Git

### Installation
```bash
git clone https://github.com/CSU-ITMO-2025-2/team9-testops.git
cd team9-testops
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Docker
```bash
docker build -t team9-testops .
docker run -p 8000:8000 team9-testops
```
Or use Docker Compose for all services (see notification-service, test-execute-consumer, etc).

### Helm & ArgoCD
- See helm/ and argocd/ for deployment manifests and charts.

## Usage
- Access web UI at http://localhost:8000
- Add Swagger/OpenAPI URL to generate test suite
- Run API tests and view results
- Kafka-based test execution via watch.py

## Environment Variables
See requirements in .env.example or set directly in your environment:
```
POSTGRES_DB=canvas_db
POSTGRES_USER=canvas_user
POSTGRES_PASSWORD=canvas_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your_secret_key
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
GEMINI_API_KEY=your_gemini_api_key
... (see notification-service/requirements.txt for more)
```

## Testing
```bash
pytest
```
All code is covered by tests in canvas/tests/ and api_tests/tests.py.

## Screenshots
See img/ for UI and dashboard screenshots.

## Contributing
Contributions are welcome! See CONTRIBUTING.md.

## License
MIT License. See LICENSE.
![Экран выполнения тестов](img/test-case%20info.png)
