# Flask API Cloud Native Deployment 🚀

A production-style Cloud Native Flask API deployment using Docker, Kubernetes, PostgreSQL, Prometheus, Grafana and GitHub Actions CI/CD.

## Architecture

Developer  
↓  
GitHub Repository  
↓  
GitHub Actions CI/CD  
↓  
Docker Image (GHCR)  
↓  
Kubernetes Cluster  
↓  
Flask API + PostgreSQL  
↓  
Prometheus Monitoring  
↓  
Grafana Dashboard  
↓  
AlertManager Email Alerts  

## Technologies Used

- Python Flask
- PostgreSQL
- Docker
- Docker Compose
- Kubernetes
- Minikube
- GitHub Actions
- GitHub Container Registry (GHCR)
- Prometheus
- Grafana
- AlertManager
- Linux

## Project Features

✅ Flask REST API application  
✅ PostgreSQL database integration  
✅ Docker containerization  
✅ Kubernetes production-style deployment  
✅ Multiple Flask API replicas for availability  
✅ Automated CI/CD pipeline using GitHub Actions  
✅ Docker image build and push to GHCR  
✅ Automated API testing  
✅ Prometheus metrics collection  
✅ Grafana monitoring dashboard  
✅ AlertManager email alerts  

## CI/CD Workflow

The project implements a complete DevOps pipeline:

1. Developer pushes code to GitHub
2. GitHub Actions triggers automatically
3. Application tests run successfully
4. Docker image is built
5. Docker image is pushed to GHCR
6. Kubernetes deploys the application
7. Prometheus and Grafana monitor the environment

## Kubernetes Deployment

Kubernetes manifests included:
kubernetes/
└── k8s-export/
├── namespace.yaml
├── flask-deployment.yaml
├── flask-service.yaml
├── postgres-deployment.yaml
└── postgres-service.yaml


