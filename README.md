# 🔥 Wishilience - Chaos Engineering API for Kubernetes

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/wishilience/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/YOUR_USERNAME/wishilience/actions)
[![Docker Image](https://img.shields.io/docker/v/YOUR_USERNAME/wishilience?label=docker&logo=docker)](https://hub.docker.com/r/YOUR_USERNAME/wishilience)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Wishilience** is a chaos engineering API designed to demonstrate Kubernetes self-healing capabilities through controlled failure scenarios.

## 🎯 Features

- **🔥 Chaos Scenarios**: CPU burn, memory leak, process termination
- **📊 Observability**: Prometheus metrics, structured JSON logs, OpenTelemetry tracing
- **🔒 Security**: SAST (Bandit, Trivy) and DAST (OWASP ZAP) scanning
- **☸️ Kubernetes-Ready**: HPA, liveness/readiness probes, resource limits
- **🚀 CI/CD**: Automated testing, building, scanning, and deployment

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Local Development](#local-development)
- [Docker Usage](#docker-usage)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Observability](#observability)
- [Security](#security)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Kubernetes (minikube/kind) with metrics-server
- kubectl CLI

### Local Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/wishilience.git
cd wishilience

# Install dependencies
pip install -r requirements.txt

# Run application
python src/app.py

# Test endpoints
curl http://localhost:8000/health
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check (K8s probe) |
| `GET` | `/metrics` | Prometheus metrics |
| `POST` | `/chaos/burn-cpu` | Trigger CPU spike (30s) |
| `POST` | `/chaos/leak-memory` | Trigger memory leak |
| `POST` | `/chaos/terminate` | Force app crash |

### Example Usage

```bash
# Trigger CPU burn to test HPA
curl -X POST http://localhost:8000/chaos/burn-cpu

# Watch Kubernetes scale pods
kubectl get hpa -w

# Trigger crash to test self-healing
curl -X POST http://localhost:8000/chaos/terminate

# Watch pod restart
kubectl get pods -w
```

---

## 💻 Local Development

### Run Tests

```bash
# Unit tests
pytest tests/ -v

# Code coverage
pytest --cov=src tests/
```

### SAST Scanning

```bash
# Bandit security scan
bandit -r src/ -f txt

# Trivy filesystem scan
trivy fs --severity HIGH,CRITICAL .
```

---

## 🐳 Docker Usage

### Build Image

```bash
docker build -t wishilience:local .
```

### Run with Docker Compose

```bash
# Start all services (API + Prometheus + Grafana)
docker-compose up -d

# View logs
docker-compose logs -f wishilience

# Access services
# - API: http://localhost:8000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

### Push to Docker Hub

```bash
docker tag wishilience:local YOUR_USERNAME/wishilience:v1.0.0
docker push YOUR_USERNAME/wishilience:v1.0.0
```

---

## ☸️ Kubernetes Deployment

### Setup Minikube

```bash
# Start minikube with metrics-server
minikube start --cpus=4 --memory=4096
minikube addons enable metrics-server

# Verify metrics-server
kubectl top nodes
```

### Deploy Application

```bash
# Update image in deployment.yaml
sed -i 's/YOUR_DOCKERHUB_USERNAME/YOUR_USERNAME/g' kubernetes/deployment.yaml

# Apply manifests
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml

# Verify deployment
kubectl get all
kubectl describe hpa wishilience-hpa
```

### Access Application

```bash
# Get service URL
minikube service wishilience-service --url

# Or port-forward
kubectl port-forward svc/wishilience-service 8080:80
```

### Demo: Self-Healing

```bash
# Terminal 1: Watch pods
kubectl get pods -w

# Terminal 2: Trigger crash
curl -X POST http://$(minikube service wishilience-service --url)/chaos/terminate

# Observe: Pod status changes to "Error", then K8s recreates it
```

### Demo: Auto-Scaling

```bash
# Terminal 1: Watch HPA
kubectl get hpa wishilience-hpa -w

# Terminal 2: Generate CPU load
for i in {1..10}; do
  curl -X POST http://$(minikube service wishilience-service --url)/chaos/burn-cpu &
done

# Observe: HPA scales from 2 to 10 pods
```

---

## 📊 Observability

### Metrics (Prometheus)

```bash
# Access Prometheus
kubectl port-forward svc/prometheus 9090:9090

# Query examples
# - Total chaos injections: chaos_injections_total
# - App crashes: app_crashes_total
# - Request duration: request_duration_seconds_bucket
```

### Logs (Structured JSON)

```bash
# View logs
kubectl logs -l app=wishilience --tail=50 -f

# Example log entry
{
  "timestamp": 1703001234.56,
  "level": "critical",
  "event": "chaos_injection",
  "type": "terminate",
  "message": "Application terminating NOW!"
}
```

### Tracing (OpenTelemetry)

Traces are exported to console. For production, configure Jaeger:

```bash
# Deploy Jaeger (optional)
kubectl apply -f https://raw.githubusercontent.com/jaegertracing/jaeger-kubernetes/main/all-in-one/jaeger-all-in-one-template.yml
```

---

## 🔒 Security

### SAST Results

- **Bandit**: Scans for Python security issues
- **Trivy**: Scans for vulnerabilities in dependencies and Docker image

```bash
# View SAST results in CI/CD artifacts
gh run download <run-id> -n sast-report
```

### DAST Results

- **OWASP ZAP**: Baseline scan for runtime vulnerabilities

```bash
# View DAST results in CI/CD artifacts
gh run download <run-id> -n dast-report
```

### Security Features

- ✅ Non-root user in Docker
- ✅ Resource limits to prevent DoS
- ✅ Health checks for automatic recovery
- ✅ No hardcoded secrets
- ✅ Dependency scanning in CI/CD

---

## 🛠 CI/CD Pipeline

### GitHub Actions Workflow

1. **Test**: Unit tests with pytest
2. **SAST**: Bandit + Trivy filesystem scan
3. **Build**: Docker image build & push
4. **DAST**: OWASP ZAP runtime scan
5. **Deploy**: Kubernetes manifest generation

### Required Secrets

Set these in GitHub Settings → Secrets:

- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub access token

---

## 📝 Architecture Diagram

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       v
┌─────────────────────────────────────┐
│     Kubernetes Service (LB)         │
└──────┬──────────────────────────────┘
       │
       v
┌──────────────────────────────────────┐
│  HPA (Auto-scaling 2-10 pods)        │
└──────┬───────────────────────────────┘
       │
       ├───> Pod 1 (Wishilience API)
       ├───> Pod 2 (Wishilience API)
       └───> Pod N (Wishilience API)
              │
              ├──> Liveness Probe (/health)
              ├──> Readiness Probe (/health)
              └──> Metrics (/metrics)
                      │
                      v
              ┌───────────────┐
              │  Prometheus   │
              └───────────────┘
                      │
                      v
              ┌───────────────┐
              │   Grafana     │
              └───────────────┘
```

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ RESTful API design with FastAPI
- ✅ Containerization with Docker multi-stage builds
- ✅ CI/CD automation with GitHub Actions
- ✅ Kubernetes orchestration (Deployments, Services, HPA)
- ✅ Observability (metrics, logs, tracing)
- ✅ Security scanning (SAST, DAST)
- ✅ Chaos engineering principles
- ✅ DevOps best practices

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👤 Author

**Your Name**  
📧 your.email@example.com  
🔗 [GitHub](https://github.com/YOUR_USERNAME) | [LinkedIn](https://linkedin.com/in/YOUR_USERNAME)

---

## 🙏 Acknowledgments

- FastAPI documentation
- Kubernetes official docs
- Prometheus & Grafana communities
- OWASP ZAP project
