# Docker Flask API

A simple Flask REST API containerized with Docker.

## Features

- Flask REST API
- Dockerized application
- Health check endpoint

## Endpoints

GET /

Returns:

```json
{
  "message": "Hello from Docker Project!"
}
```

GET /health

Returns:

```json
{
  "status": "healthy"
}
```

## Run Locally

```bash
python3 app.py
```

## Build Docker Image

```bash
docker build -t flask-api .
```

## Run Docker Container

```bash
docker run -d -p 8000:8000 flask-api
```

# deployment test
