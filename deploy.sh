#!/bin/bash

# Production deployment script for AI Chatbot

set -e

echo "🚀 AI Chatbot Production Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

print_status "Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Docker Compose is installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        print_warning "Please edit .env file with your production values before continuing."
        print_warning "Required variables: FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET"
        exit 1
    else
        print_error "env.example file not found. Cannot create .env file."
        exit 1
    fi
fi

print_status ".env file found"

# Validate required environment variables
echo "🔍 Validating environment configuration..."

required_vars=(
    "FIREBASE_PROJECT_ID"
    "FIREBASE_CLIENT_EMAIL"
    "GOOGLE_CLIENT_ID"
    "GOOGLE_CLIENT_SECRET"
)

missing_vars=()

for var in "${required_vars[@]}"; do
    if ! grep -q "^${var}=" .env || grep -q "^${var}=$" .env || grep -q "^${var}=your-" .env; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    print_error "Missing or invalid environment variables:"
    printf '%s\n' "${missing_vars[@]}"
    print_error "Please update your .env file with valid values."
    exit 1
fi

print_status "Environment validation passed"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs user_data ssl
print_status "Directories created"

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t chatbot-app:latest .
print_status "Docker image built successfully"

# Run health check
echo "🏥 Running health check..."
if docker run --rm --env-file .env chatbot-app:latest python3 /app/health_check.py; then
    print_status "Health check passed"
else
    print_warning "Health check failed - continuing with deployment"
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true
print_status "Existing containers stopped"

# Start new containers
echo "🚀 Starting new containers..."
docker-compose up -d
print_status "Containers started"

# Wait for application to be ready
echo "⏳ Waiting for application to be ready..."
sleep 10

# Check if application is running
echo "🔍 Checking application status..."
if docker-compose ps | grep -q "Up"; then
    print_status "Application is running"
else
    print_error "Application failed to start"
    docker-compose logs chatbot
    exit 1
fi

# Get application URL
PORT=$(grep "STREAMLIT_SERVER_PORT" .env | cut -d'=' -f2 || echo "8501")
echo "🌐 Application is available at:"
echo "   Local: http://localhost:${PORT}"
echo "   Network: http://$(hostname -I | awk '{print $1}'):${PORT}"

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=20 chatbot

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📚 Next steps:"
echo "   1. Configure your domain and SSL certificates"
echo "   2. Update OAuth redirect URIs"
echo "   3. Set up monitoring and alerts"
echo "   4. Configure backups"
echo ""
echo "📖 For more information, see DEPLOYMENT_GUIDE.md"
