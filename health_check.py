#!/usr/bin/env python3
"""
Health check script for production deployment
"""

import os
import sys
import requests
import time
from datetime import datetime

def check_firebase_connection():
    """Check Firebase connection"""
    try:
        from firebase_utils import initialize_firebase
        if initialize_firebase():
            return True, "Firebase connection successful"
        else:
            return False, "Firebase connection failed"
    except Exception as e:
        return False, f"Firebase error: {str(e)}"

def check_environment_variables():
    """Check required environment variables"""
    required_vars = [
        'FIREBASE_PROJECT_ID',
        'FIREBASE_CLIENT_EMAIL',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        return False, f"Missing environment variables: {', '.join(missing_vars)}"
    
    return True, "All required environment variables present"

def check_api_keys():
    """Check API key availability"""
    openai_key = os.getenv('OPENAI_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')
    
    if not openai_key and not google_key:
        return False, "No API keys configured (OpenAI or Google)"
    
    available_keys = []
    if openai_key and openai_key.startswith('sk-'):
        available_keys.append('OpenAI')
    if google_key and google_key.startswith('AI'):
        available_keys.append('Google')
    
    if not available_keys:
        return False, "No valid API keys found"
    
    return True, f"Available API keys: {', '.join(available_keys)}"

def check_streamlit_health():
    """Check Streamlit application health"""
    try:
        port = os.getenv('STREAMLIT_SERVER_PORT', '8501')
        response = requests.get(f'http://localhost:{port}/_stcore/health', timeout=5)
        if response.status_code == 200:
            return True, "Streamlit application healthy"
        else:
            return False, f"Streamlit health check failed: {response.status_code}"
    except Exception as e:
        return False, f"Streamlit health check error: {str(e)}"

def main():
    """Main health check function"""
    print(f"🏥 Health Check - {datetime.now().isoformat()}")
    print("=" * 50)
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("Firebase Connection", check_firebase_connection),
        ("API Keys", check_api_keys),
        ("Streamlit Application", check_streamlit_health),
    ]
    
    all_healthy = True
    
    for check_name, check_func in checks:
        try:
            is_healthy, message = check_func()
            status = "✅" if is_healthy else "❌"
            print(f"{status} {check_name}: {message}")
            
            if not is_healthy:
                all_healthy = False
                
        except Exception as e:
            print(f"❌ {check_name}: Error - {str(e)}")
            all_healthy = False
    
    print("=" * 50)
    
    if all_healthy:
        print("🎉 All health checks passed!")
        sys.exit(0)
    else:
        print("⚠️ Some health checks failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
