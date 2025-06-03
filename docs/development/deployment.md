# Deployment Guide

This document provides comprehensive guidance for deploying the disaster response coordination web application to production environments.

## Deployment Overview

The application supports multiple deployment strategies:

- **Docker Compose**: Simple single-server deployment
- **Kubernetes**: Scalable container orchestration
- **Azure Container Apps**: Cloud-native deployment
- **Manual Deployment**: Traditional server setup

## Prerequisites

### System Requirements

- **CPU**: 2+ cores for production workloads
- **Memory**: 4GB+ RAM (8GB+ recommended)
- **Storage**: 20GB+ available disk space
- **Network**: Stable internet connection with proper firewall configuration

### Required Services

- **Database**: PostgreSQL 13+ or SQLite for development
- **Cache**: Redis 6+ for session management and real-time features
- **Message Queue**: Redis or RabbitMQ for background tasks
- **File Storage**: Local filesystem or cloud storage (AWS S3, Azure Blob)

## Environment Configuration

### Production Environment Variables

Create production environment files:

```bash
# ai_services/.env.production
DATABASE_URL=postgresql://user:password@localhost:5432/disaster_response_prod
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secure-secret-key-here
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=["https://yourdomain.com"]
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# AI Service Configuration
OPENAI_API_KEY=your-openai-api-key
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_API_KEY=your-azure-openai-key
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8001

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
ALLOWED_HOSTS=["yourdomain.com", "www.yourdomain.com"]
SECURE_COOKIES=true
```

```bash
# frontend/.env.production
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_WS_BASE_URL=wss://api.yourdomain.com
VITE_ENVIRONMENT=production
VITE_SENTRY_DSN=your-sentry-dsn
VITE_GOOGLE_MAPS_API_KEY=your-google-maps-key
```

## Docker Deployment

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: "3.8"

services:
  # Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: disaster_response_prod
      POSTGRES_USER: disaster_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./ai_services/database/migrations:/docker-entrypoint-initdb.d
    restart: unless-stopped
    networks:
      - backend

  # Cache and Message Queue
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - backend

  # Backend API
  backend:
    build:
      context: ./ai_services
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://disaster_user:${POSTGRES_PASSWORD}@postgres:5432/disaster_response_prod
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    networks:
      - backend
      - frontend
    volumes:
      - ./ai_services/logs:/app/logs

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/ssl:/etc/nginx/ssl:ro

  # Load Balancer / Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/ssl:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
    networks:
      - frontend

volumes:
  postgres_data:
  redis_data:

networks:
  frontend:
  backend:
```

### Nginx Configuration

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Frontend
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/ssl/certs/yourdomain.crt;
        ssl_certificate_key /etc/ssl/private/yourdomain.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Deploy with Docker Compose

```bash
# Production deployment
export POSTGRES_PASSWORD=your-secure-password

# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

## Kubernetes Deployment

### Kubernetes Manifests

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: disaster-response
---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: disaster-response
data:
  DATABASE_HOST: postgres-service
  REDIS_HOST: redis-service
  ENVIRONMENT: production
---
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: disaster-response
type: Opaque
stringData:
  DATABASE_PASSWORD: your-database-password
  SECRET_KEY: your-secret-key
  JWT_SECRET_KEY: your-jwt-secret
  OPENAI_API_KEY: your-openai-key
---
# k8s/postgres.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: disaster-response
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:15-alpine
          env:
            - name: POSTGRES_DB
              value: disaster_response_prod
            - name: POSTGRES_USER
              value: disaster_user
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: DATABASE_PASSWORD
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: disaster-response
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
```

### Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n disaster-response

# View logs
kubectl logs -f deployment/backend -n disaster-response

# Scale deployment
kubectl scale deployment backend --replicas=3 -n disaster-response
```

## Azure Deployment

### Azure Container Apps

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create resource group
az group create --name disaster-response-rg --location eastus

# Create container app environment
az containerapp env create \
  --name disaster-response-env \
  --resource-group disaster-response-rg \
  --location eastus

# Deploy backend
az containerapp create \
  --name disaster-response-api \
  --resource-group disaster-response-rg \
  --environment disaster-response-env \
  --image your-registry/disaster-response-backend:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars DATABASE_URL=secretref:database-url \
  --secrets database-url="postgresql://..."

# Deploy frontend
az containerapp create \
  --name disaster-response-frontend \
  --resource-group disaster-response-rg \
  --environment disaster-response-env \
  --image your-registry/disaster-response-frontend:latest \
  --target-port 80 \
  --ingress external
```

## Database Setup

### Production Database Migration

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Create initial admin user
docker-compose exec backend python -c "
from app.core.database import get_db
from app.services.auth_service import create_user
from app.schemas.user import UserCreate
from app.models.user import UserRole

db = next(get_db())
admin_user = UserCreate(
    email='admin@yourdomain.com',
    password='secure-admin-password',
    full_name='System Administrator',
    role=UserRole.GOVERNMENT
)
create_user(db, admin_user)
print('Admin user created successfully')
"
```

### Database Backup and Restore

```bash
# Backup database
docker-compose exec postgres pg_dump -U disaster_user disaster_response_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
docker-compose exec -T postgres psql -U disaster_user disaster_response_prod < backup_20241201_120000.sql

# Automated backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U disaster_user disaster_response_prod > $BACKUP_DIR/backup_$DATE.sql
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
EOF
chmod +x backup.sh
```

## Monitoring and Logging

### Application Monitoring

```yaml
# monitoring/docker-compose.yml
version: "3.8"

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - monitoring

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
    networks:
      - monitoring

volumes:
  grafana_data:

networks:
  monitoring:
```

### Log Aggregation

```bash
# Install Filebeat for log shipping
docker run -d \
  --name filebeat \
  --user root \
  --volume="$(pwd)/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro" \
  --volume="/var/lib/docker/containers:/var/lib/docker/containers:ro" \
  --volume="/var/run/docker.sock:/var/run/docker.sock:ro" \
  docker.elastic.co/beats/filebeat:8.8.0
```

## Security Configuration

### SSL/TLS Setup

```bash
# Generate SSL certificate with Let's Encrypt
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to nginx volume
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/yourdomain.crt
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/yourdomain.key
```

### Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Block unnecessary ports
sudo ufw deny 5432  # PostgreSQL
sudo ufw deny 6379  # Redis
```

## Performance Optimization

### Database Optimization

```sql
-- Create database indexes for better performance
CREATE INDEX idx_requests_status ON requests(status);
CREATE INDEX idx_requests_priority ON requests(priority);
CREATE INDEX idx_requests_created_at ON requests(created_at);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_resources_type ON resources(type);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM requests WHERE status = 'pending';
```

### Caching Strategy

```python
# Redis caching configuration
CACHE_CONFIG = {
    "user_sessions": {"ttl": 3600},      # 1 hour
    "dashboard_stats": {"ttl": 300},     # 5 minutes
    "resource_status": {"ttl": 600},     # 10 minutes
    "agent_responses": {"ttl": 1800},    # 30 minutes
}
```

## Health Checks and Monitoring

### Application Health Checks

```bash
# Backend health check
curl -f http://localhost:8000/health || exit 1

# Frontend health check
curl -f http://localhost:3000/ || exit 1

# Database health check
docker-compose exec postgres pg_isready -U disaster_user
```

### Automated Deployment Script

```bash
#!/bin/bash
# deploy.sh - Production deployment script

set -e

echo "🚀 Starting production deployment..."

# Backup current database
echo "📦 Creating database backup..."
./backup.sh

# Pull latest images
echo "📥 Pulling latest images..."
docker-compose -f docker-compose.prod.yml pull

# Stop services gracefully
echo "⏹️ Stopping services..."
docker-compose -f docker-compose.prod.yml down

# Start services
echo "▶️ Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "🔍 Waiting for services to be healthy..."
sleep 30

# Run health checks
echo "🏥 Running health checks..."
./health-check.sh

echo "✅ Deployment completed successfully!"
```

## Troubleshooting Deployment Issues

### Common Issues and Solutions

1. **Container fails to start**

   ```bash
   # Check container logs
   docker-compose logs backend

   # Check resource usage
   docker stats
   ```

2. **Database connection issues**

   ```bash
   # Test database connectivity
   docker-compose exec backend python -c "
   from app.core.database import engine
   with engine.connect() as conn:
       print('Database connection successful')
   "
   ```

3. **WebSocket connection problems**

   ```bash
   # Check WebSocket endpoint
   wscat -c ws://localhost:8000/ws
   ```

4. **High memory usage**
   ```bash
   # Monitor memory usage
   docker-compose exec backend python -c "
   import psutil
   print(f'Memory usage: {psutil.virtual_memory().percent}%')
   "
   ```

## Maintenance

### Regular Maintenance Tasks

```bash
# Weekly maintenance script
#!/bin/bash
# maintenance.sh

echo "🧹 Starting maintenance tasks..."

# Clean up old logs
find /var/log/disaster-response -name "*.log" -mtime +30 -delete

# Database maintenance
docker-compose exec postgres vacuumdb -U disaster_user disaster_response_prod

# Update system packages
sudo apt update && sudo apt upgrade -y

# Restart services for memory cleanup
docker-compose restart

echo "✅ Maintenance completed!"
```

This deployment guide ensures your disaster response coordination system is production-ready with proper security, monitoring, and maintenance procedures.
