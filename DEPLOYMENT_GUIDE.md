# 🚀 Production Deployment Guide

This guide will help you deploy your AI Chatbot application to production using Docker and cloud platforms.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Domain name and SSL certificate
- Firebase project with Firestore enabled
- Google OAuth credentials
- OpenAI and/or Google API keys

## 🔧 Environment Setup

### 1. Environment Variables

Copy the example environment file and configure it:

```bash
cp env.example .env
```

Edit `.env` with your production values:

```bash
# Firebase Configuration
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-domain.com/oauth2callback/google

# Security
SECRET_KEY=your-super-secret-key-for-production
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### 2. SSL Certificate Setup

Create SSL directory and add your certificates:

```bash
mkdir -p ssl
# Copy your SSL certificates
cp your-cert.pem ssl/cert.pem
cp your-key.pem ssl/key.pem
```

## 🐳 Docker Deployment

### 1. Build and Run with Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Manual Docker Build

```bash
# Build the image
docker build -t chatbot-app .

# Run the container
docker run -d \
  --name chatbot \
  -p 8501:8501 \
  --env-file .env \
  chatbot-app
```

## ☁️ Cloud Platform Deployment

### AWS ECS/Fargate

1. **Push image to ECR:**
```bash
aws ecr create-repository --repository-name chatbot-app
docker tag chatbot-app:latest your-account.dkr.ecr.region.amazonaws.com/chatbot-app:latest
docker push your-account.dkr.ecr.region.amazonaws.com/chatbot-app:latest
```

2. **Create ECS Task Definition** with environment variables
3. **Create ECS Service** with load balancer
4. **Configure Route 53** for your domain

### Google Cloud Run

1. **Build and push:**
```bash
gcloud builds submit --tag gcr.io/your-project/chatbot-app
```

2. **Deploy:**
```bash
gcloud run deploy chatbot-app \
  --image gcr.io/your-project/chatbot-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FIREBASE_PROJECT_ID=your-project-id"
```

### Azure Container Instances

1. **Build and push to ACR:**
```bash
az acr build --registry your-registry --image chatbot-app .
```

2. **Deploy:**
```bash
az container create \
  --resource-group your-rg \
  --name chatbot-app \
  --image your-registry.azurecr.io/chatbot-app \
  --ports 8501 \
  --environment-variables FIREBASE_PROJECT_ID=your-project-id
```

## 🔒 Security Configuration

### 1. Firestore Security Rules

Update your Firestore rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### 2. Firebase Authentication

Enable authentication providers:
- Email/Password
- Google Sign-In
- Apple Sign-In (if using)

### 3. Rate Limiting

Configure rate limiting in your reverse proxy (Nginx/CloudFlare):
- API endpoints: 10 requests/second
- Login endpoints: 5 requests/minute

## 📊 Monitoring and Logging

### 1. Application Logs

Logs are written to `/app/logs/app.log` in the container.

### 2. Health Checks

The application includes health check endpoints:
- `/health` - Basic health check
- `/_stcore/health` - Streamlit health check

### 3. Monitoring Setup

Add monitoring with:
- **Prometheus + Grafana** for metrics
- **ELK Stack** for log aggregation
- **Sentry** for error tracking

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t chatbot-app .
      
      - name: Deploy to cloud
        run: |
          # Your deployment commands here
          echo "Deploying to production..."
```

## 🚨 Troubleshooting

### Common Issues

1. **Firebase Connection Issues:**
   - Check environment variables
   - Verify service account permissions
   - Ensure Firestore is enabled

2. **OAuth Redirect Issues:**
   - Update redirect URIs in OAuth providers
   - Check domain configuration

3. **SSL Certificate Issues:**
   - Verify certificate validity
   - Check certificate chain
   - Ensure private key matches

### Debug Commands

```bash
# Check container logs
docker logs chatbot-app

# Check environment variables
docker exec chatbot-app env

# Test Firebase connection
docker exec chatbot-app python -c "from firebase_utils import initialize_firebase; print(initialize_firebase())"
```

## 📈 Performance Optimization

### 1. Caching
- Enable Redis for session storage
- Cache Firebase queries
- Use CDN for static assets

### 2. Scaling
- Use horizontal pod autoscaling
- Implement database connection pooling
- Add load balancers

### 3. Resource Limits
```yaml
# In docker-compose.yml
services:
  chatbot:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

## 🔐 Backup and Recovery

### 1. Database Backup
```bash
# Backup Firestore data
gcloud firestore export gs://your-backup-bucket/backup-$(date +%Y%m%d)
```

### 2. Application Backup
- Regular Docker image backups
- Environment variable backups
- SSL certificate backups

## 📞 Support

For production support:
- Monitor application logs
- Set up alerts for errors
- Implement health checks
- Use monitoring tools

---

**🎉 Your AI Chatbot is now production-ready!**

Remember to:
- ✅ Test thoroughly before going live
- ✅ Monitor performance and errors
- ✅ Keep dependencies updated
- ✅ Backup your data regularly
- ✅ Follow security best practices
