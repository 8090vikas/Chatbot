#!/bin/bash

# Production startup script for AI Chatbot

set -e

echo "🚀 Starting AI Chatbot Application..."

# Create necessary directories
mkdir -p /app/logs /app/user_data

# Set proper permissions
chmod 755 /app/logs /app/user_data

# Validate environment variables
echo "🔍 Validating environment configuration..."

required_vars=(
    "FIREBASE_PROJECT_ID"
    "FIREBASE_CLIENT_EMAIL"
    "GOOGLE_CLIENT_ID"
    "GOOGLE_CLIENT_SECRET"
)

missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "❌ Missing required environment variables:"
    printf '%s\n' "${missing_vars[@]}"
    echo "Please check your .env file or environment configuration."
    exit 1
fi

echo "✅ Environment validation passed"

# Test Firebase connection
echo "🔥 Testing Firebase connection..."
python3 -c "
from firebase_utils import initialize_firebase
if initialize_firebase():
    print('✅ Firebase connection successful')
else:
    print('⚠️ Firebase connection failed - using local storage')
"

# Test OAuth configuration
echo "🔐 Testing OAuth configuration..."
if [ -n "$GOOGLE_CLIENT_ID" ] && [ -n "$GOOGLE_CLIENT_SECRET" ]; then
    echo "✅ Google OAuth configured"
else
    echo "⚠️ Google OAuth not configured"
fi

# Set Streamlit configuration
export STREAMLIT_SERVER_PORT=${STREAMLIT_SERVER_PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}
export STREAMLIT_SERVER_HEADLESS=${STREAMLIT_SERVER_HEADLESS:-true}
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=${STREAMLIT_BROWSER_GATHER_USAGE_STATS:-false}
export STREAMLIT_SERVER_ENABLE_CORS=${STREAMLIT_SERVER_ENABLE_CORS:-false}
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=${STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION:-true}

echo "🌐 Starting Streamlit server on port $STREAMLIT_SERVER_PORT..."

# Start the application
exec streamlit run app.py \
    --server.port=$STREAMLIT_SERVER_PORT \
    --server.address=$STREAMLIT_SERVER_ADDRESS \
    --server.headless=$STREAMLIT_SERVER_HEADLESS \
    --browser.gatherUsageStats=$STREAMLIT_BROWSER_GATHER_USAGE_STATS \
    --server.enableCORS=$STREAMLIT_SERVER_ENABLE_CORS \
    --server.enableXsrfProtection=$STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION
