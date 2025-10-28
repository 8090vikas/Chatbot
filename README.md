# 🤖 AI Chatbot - Production Ready

A modern, production-ready AI chatbot application supporting both OpenAI GPT and Google Gemini models, with Firebase authentication and chat history persistence.

## ✨ Features

- **🤖 Dual AI Models**: Support for OpenAI GPT (3.5, 4, 4 Turbo) and Google Gemini (Pro, Pro Vision)
- **🔐 Authentication**: Firebase Auth with Google and Apple OAuth
- **💾 Chat History**: Persistent chat storage with Firebase Firestore
- **📱 Responsive UI**: Modern, mobile-friendly interface
- **🔒 Security**: Production-ready security configurations
- **🐳 Docker Ready**: Containerized for easy deployment
- **📊 Monitoring**: Health checks and logging
- **⚡ Performance**: Optimized for production workloads

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Firebase project with Firestore enabled
- Google OAuth credentials
- OpenAI and/or Google API keys

### 1. Clone and Setup

```bash
git clone <your-repo>
cd Chatbot
cp env.example .env
```

### 2. Configure Environment

Edit `.env` with your production values:

```bash
# Firebase Configuration
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
# ... (see env.example for complete list)

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-domain.com/oauth2callback/google
```

### 3. Deploy with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f chatbot
```

### 4. Access Application

Open your browser to `http://localhost:8501` (or your configured domain).

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │────│  Streamlit App  │────│   Firebase      │
│   (SSL/HTTPS)   │    │   (Container)   │    │   (Auth/DB)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   AI Models     │    │   OAuth         │
│   (Optional)    │    │   OpenAI/Gemini │    │   Google/Apple  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FIREBASE_PROJECT_ID` | Firebase project ID | ✅ |
| `FIREBASE_CLIENT_EMAIL` | Service account email | ✅ |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | ✅ |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | ✅ |
| `OPENAI_API_KEY` | OpenAI API key | ⚠️ |
| `GOOGLE_API_KEY` | Google API key | ⚠️ |

### Firebase Setup

1. **Create Firebase Project**
2. **Enable Firestore Database**
3. **Enable Authentication** (Email/Password, Google, Apple)
4. **Create Service Account** and download JSON
5. **Set Security Rules** (see `firestore.rules`)

### OAuth Setup

1. **Google OAuth**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth 2.0 credentials
   - Add authorized redirect URIs

2. **Apple Sign-In** (Optional):
   - Configure in Apple Developer Console
   - Add redirect URI

## 🐳 Docker Deployment

### Single Container

```bash
docker build -t chatbot-app .
docker run -d \
  --name chatbot \
  -p 8501:8501 \
  --env-file .env \
  chatbot-app
```

### Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Production with Nginx

```bash
# With SSL certificates
docker-compose -f docker-compose.yml up -d
```

## ☁️ Cloud Deployment

### AWS ECS/Fargate

```bash
# Build and push to ECR
aws ecr create-repository --repository-name chatbot-app
docker tag chatbot-app:latest your-account.dkr.ecr.region.amazonaws.com/chatbot-app:latest
docker push your-account.dkr.ecr.region.amazonaws.com/chatbot-app:latest

# Deploy with ECS
aws ecs create-service --cluster your-cluster --service-name chatbot-app
```

### Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/chatbot-app
gcloud run deploy chatbot-app \
  --image gcr.io/your-project/chatbot-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
# Build and push to ACR
az acr build --registry your-registry --image chatbot-app .

# Deploy
az container create \
  --resource-group your-rg \
  --name chatbot-app \
  --image your-registry.azurecr.io/chatbot-app \
  --ports 8501
```

## 🔒 Security

### Production Security Checklist

- ✅ **Environment Variables**: All secrets in environment variables
- ✅ **HTTPS Only**: SSL/TLS encryption enabled
- ✅ **Firebase Rules**: Proper Firestore security rules
- ✅ **Rate Limiting**: API rate limiting configured
- ✅ **Input Validation**: User input sanitization
- ✅ **CORS**: Cross-origin requests properly configured
- ✅ **Headers**: Security headers implemented

### Security Headers

The application includes security headers:
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`

## 📊 Monitoring

### Health Checks

- **Application**: `/_stcore/health`
- **Custom**: `/health`

### Logging

- **Application Logs**: `/app/logs/app.log`
- **Access Logs**: Nginx access logs
- **Error Logs**: Nginx error logs

### Metrics

Monitor key metrics:
- Response time
- Error rate
- Memory usage
- CPU usage
- Database connections

## 🔄 CI/CD

### GitHub Actions

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
      - name: Build and Deploy
        run: |
          docker build -t chatbot-app .
          # Deploy to your cloud platform
```

## 🚨 Troubleshooting

### Common Issues

1. **Firebase Connection Failed**
   - Check environment variables
   - Verify service account permissions
   - Ensure Firestore is enabled

2. **OAuth Redirect Errors**
   - Update redirect URIs in OAuth providers
   - Check domain configuration

3. **SSL Certificate Issues**
   - Verify certificate validity
   - Check certificate chain

### Debug Commands

```bash
# Check container logs
docker logs chatbot-app

# Check environment variables
docker exec chatbot-app env

# Test Firebase connection
docker exec chatbot-app python -c "from firebase_utils import initialize_firebase; print(initialize_firebase())"
```

## 📈 Performance

### Optimization Tips

- **Caching**: Enable Redis for session storage
- **CDN**: Use CDN for static assets
- **Scaling**: Implement horizontal scaling
- **Database**: Use connection pooling

### Resource Requirements

- **Minimum**: 512MB RAM, 0.5 CPU
- **Recommended**: 1GB RAM, 1 CPU
- **High Traffic**: 2GB RAM, 2 CPU

## 📚 API Documentation

### Authentication Endpoints

- `POST /auth/login` - User login
- `POST /auth/signup` - User registration
- `GET /auth/logout` - User logout

### Chat Endpoints

- `POST /chat/send` - Send message
- `GET /chat/history` - Get chat history
- `POST /chat/save` - Save chat history

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting guide
- Review the deployment documentation

---

**🎉 Your AI Chatbot is production-ready!**

Built with ❤️ by Vikas Gupta
