# Docker Deployment Guide

This document describes how to deploy the SMS Spam Classifier using Docker.

## Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 1.29+)

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

The application will be available at `http://localhost:5001`

### 2. Build and Run with Docker

```bash
# Build the image
docker build -t spam-classifier:latest .

# Run the container
docker run -d \
  --name spam_classifier \
  -p 5001:5001 \
  spam-classifier:latest

# View logs
docker logs -f spam_classifier

# Stop the container
docker stop spam_classifier
docker rm spam_classifier
```

## Configuration

### Environment Variables

You can customize the application using environment variables:

```bash
docker run -d \
  -e FLASK_ENV=production \
  -e WORKERS=4 \
  -p 5001:5001 \
  spam-classifier:latest
```

### Volume Mounts

Mount local directories for data persistence:

```bash
docker run -d \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/model.pkl:/app/model.pkl \
  -p 5001:5001 \
  spam-classifier:latest
```

## Production Deployment

### With Nginx Reverse Proxy

1. Uncomment the nginx service in `docker-compose.yml`
2. Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server spam-classifier:5001;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

3. Start services:
```bash
docker-compose up -d
```

### Scaling

Scale the application to multiple instances:

```bash
docker-compose up -d --scale spam-classifier=3
```

## Health Checks

The container includes a health check that runs every 30 seconds:

```bash
# Check container health
docker ps

# View health check logs
docker inspect --format='{{json .State.Health}}' spam_classifier
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs spam_classifier

# Check if port is available
lsof -i :5001

# Rebuild without cache
docker build --no-cache -t spam-classifier:latest .
```

### Model Not Found

```bash
# Train model inside container
docker exec spam_classifier python src/train.py

# Or copy model from host
docker cp model.pkl spam_classifier:/app/model.pkl
```

## Building for Different Architectures

### Multi-platform Build

```bash
# Create builder
docker buildx create --name multiarch --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t yourusername/spam-classifier:latest \
  --push \
  .
```

## Image Optimization

Current image size: ~200MB

To reduce size:
- Use multi-stage builds
- Remove unnecessary dependencies
- Use alpine-based images

Example optimized Dockerfile:

```dockerfile
FROM python:3.9-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-alpine
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
RUN python src/train.py
CMD ["python", "ui/app.py"]
```

## Security Best Practices

1. **Don't run as root**:
```dockerfile
RUN useradd -m myuser
USER myuser
```

2. **Use specific base image versions**:
```dockerfile
FROM python:3.9.13-slim
```

3. **Scan for vulnerabilities**:
```bash
docker scan spam-classifier:latest
```

4. **Use secrets for sensitive data**:
```bash
docker run -d \
  --secret API_KEY \
  spam-classifier:latest
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Build Docker image
  run: docker build -t spam-classifier:${{ github.sha }} .

- name: Push to registry
  run: |
    docker tag spam-classifier:${{ github.sha }} ghcr.io/user/spam-classifier:latest
    docker push ghcr.io/user/spam-classifier:latest
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi spam-classifier:latest

# Prune unused images and containers
docker system prune -a
```
