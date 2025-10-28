# Production Configuration
# This file contains production-ready settings for the chatbot application

import os
import logging
from datetime import datetime

# Logging Configuration
def setup_logging():
    """Setup production logging"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', '/app/logs/app.log')
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# Security Configuration
SECURITY_CONFIG = {
    'SECRET_KEY': os.getenv('SECRET_KEY', 'your-super-secret-key-change-in-production'),
    'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS', 'localhost').split(','),
    'RATE_LIMIT_PER_MINUTE': int(os.getenv('RATE_LIMIT_PER_MINUTE', '60')),
    'RATE_LIMIT_PER_HOUR': int(os.getenv('RATE_LIMIT_PER_HOUR', '1000')),
}

# Firebase Configuration
FIREBASE_CONFIG = {
    'PROJECT_ID': os.getenv('FIREBASE_PROJECT_ID'),
    'PRIVATE_KEY_ID': os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    'PRIVATE_KEY': os.getenv('FIREBASE_PRIVATE_KEY'),
    'CLIENT_EMAIL': os.getenv('FIREBASE_CLIENT_EMAIL'),
    'CLIENT_ID': os.getenv('FIREBASE_CLIENT_ID'),
    'AUTH_URI': os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth'),
    'TOKEN_URI': os.getenv('FIREBASE_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
    'AUTH_PROVIDER_X509_CERT_URL': os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL', 'https://www.googleapis.com/oauth2/v1/certs'),
    'CLIENT_X509_CERT_URL': os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
}

# OAuth Configuration
OAUTH_CONFIG = {
    'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
    'GOOGLE_CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET'),
    'GOOGLE_REDIRECT_URI': os.getenv('GOOGLE_REDIRECT_URI'),
    'APPLE_CLIENT_ID': os.getenv('APPLE_CLIENT_ID'),
    'APPLE_CLIENT_SECRET': os.getenv('APPLE_CLIENT_SECRET'),
    'APPLE_REDIRECT_URI': os.getenv('APPLE_REDIRECT_URI'),
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    'SERVER_PORT': int(os.getenv('STREAMLIT_SERVER_PORT', '8501')),
    'SERVER_ADDRESS': os.getenv('STREAMLIT_SERVER_ADDRESS', '0.0.0.0'),
    'SERVER_HEADLESS': os.getenv('STREAMLIT_SERVER_HEADLESS', 'true').lower() == 'true',
    'BROWSER_GATHER_USAGE_STATS': os.getenv('STREAMLIT_BROWSER_GATHER_USAGE_STATS', 'false').lower() == 'true',
    'SERVER_ENABLE_CORS': os.getenv('STREAMLIT_SERVER_ENABLE_CORS', 'false').lower() == 'true',
    'SERVER_ENABLE_XSRF_PROTECTION': os.getenv('STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION', 'true').lower() == 'true',
}

# Application Configuration
APP_CONFIG = {
    'DEBUG': os.getenv('DEBUG', 'false').lower() == 'true',
    'ENVIRONMENT': os.getenv('ENVIRONMENT', 'production'),
    'VERSION': '1.0.0',
    'BUILD_DATE': datetime.now().isoformat(),
}

def get_config():
    """Get complete configuration dictionary"""
    return {
        'security': SECURITY_CONFIG,
        'firebase': FIREBASE_CONFIG,
        'oauth': OAUTH_CONFIG,
        'streamlit': STREAMLIT_CONFIG,
        'app': APP_CONFIG,
    }

def validate_config():
    """Validate required configuration"""
    required_vars = [
        'FIREBASE_PROJECT_ID',
        'FIREBASE_CLIENT_EMAIL',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET',
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True
