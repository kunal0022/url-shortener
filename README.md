# URL Shortener - Complete DevOps Project

A production-like DevOps project running on a local Kubernetes cluster.

## Architecture

GitHub → GitHub Actions → Docker Hub → Kubernetes (Kind)
                                            ↓
                                    Flask API + Redis
                                            ↓
                              Prometheus + Grafana + Jaeger

## Tech Stack

| Component | Technology |
|---|---|
| Application | Python Flask + Redis |
| Containerization | Docker |
| Container Registry | Docker Hub |
| Orchestration | Kubernetes (Kind) |
| CI/CD | GitHub Actions + Self-hosted Runner |
| Monitoring | Prometheus + Grafana |
| Alerting | Alertmanager |
| Tracing | Jaeger + OpenTelemetry |
| Autoscaling | HPA (2-8 replicas) |

## Access Services

| Service | URL | Credentials |
|---|---|---|
| API | http://localhost:5000 | - |
| Grafana | http://localhost:3000 | admin/admin123 |
| Prometheus | http://localhost:9090 | - |
| Alertmanager | http://localhost:9093 | - |
| Jaeger | http://localhost:16686 | - |

## API Endpoints

### Health check
```bash
curl http://localhost:5000/health
```

### Shorten URL
```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://google.com"}'
```

### Resolve short code
```bash
curl http://localhost:5000/r/{code}
```

## CI/CD Pipeline
On every push to main branch:
1. GitHub Actions builds Docker image
2. Pushes to Docker Hub with git SHA tag
3. Self-hosted runner deploys to Kubernetes
4. Rollout status verified

## Autoscaling
HPA configured to scale between 2-8 replicas:
- Scale up when CPU > 50%
- Scale up when Memory > 70%

## Monitoring
- Prometheus scrapes metrics every 30s
- Grafana dashboards (ID: 6417)
- Alertmanager alerts for high CPU, crashes
- Jaeger distributed tracing for all requests

## Quick Start

### 1. Create cluster
```bash
kind create cluster --config kind-config.yaml
```

### 2. Deploy app
```bash
kubectl apply -f k8s/
```

### 3. Install monitoring
```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f monitoring/prometheus-values.yaml
```

### 4. Start port forwards
```bash
~/port-forwards.sh
```

## Author
Kunal Gajbhare - DevOps Engineer