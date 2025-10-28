import streamlit as st
import requests
import secrets
import urllib.parse
import time
from firebase_utils import store_user_data, get_user_data

# OAuth Configuration (These should be in environment variables or secrets.toml in production)
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
GOOGLE_REDIRECT_URI = "http://localhost:8501/oauth2callback/google"

GITHUB_CLIENT_ID = "YOUR_GITHUB_CLIENT_ID"
GITHUB_CLIENT_SECRET = "YOUR_GITHUB_CLIENT_SECRET"
GITHUB_REDIRECT_URI = "http://localhost:8501/oauth2callback/github"

LINKEDIN_CLIENT_ID = "YOUR_LINKEDIN_CLIENT_ID"
LINKEDIN_CLIENT_SECRET = "YOUR_LINKEDIN_CLIENT_SECRET"
LINKEDIN_REDIRECT_URI = "http://localhost:8501/oauth2callback/linkedin"

APPLE_CLIENT_ID = "YOUR_APPLE_CLIENT_ID"
APPLE_CLIENT_SECRET = "YOUR_APPLE_CLIENT_SECRET"
APPLE_REDIRECT_URI = "http://localhost:8501/oauth2callback/apple"

def generate_state():
    """Generate a random state for OAuth security"""
    return secrets.token_urlsafe(32)

def get_google_auth_url():
    """Generate Google OAuth URL"""
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = generate_state()
    
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": st.session_state.oauth_state,
        "access_type": "offline",
        "prompt": "consent"
    }
    
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

def get_github_auth_url():
    """Generate GitHub OAuth URL"""
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = generate_state()
    
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "user:email",
        "state": st.session_state.oauth_state
    }
    
    return f"https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}"

def get_linkedin_auth_url():
    """Generate LinkedIn OAuth URL"""
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = generate_state()
    
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "state": st.session_state.oauth_state,
        "scope": "r_liteprofile r_emailaddress"
    }
    
    return f"https://www.linkedin.com/oauth/v2/authorization?{urllib.parse.urlencode(params)}"

def get_apple_auth_url():
    """Generate Apple OAuth URL"""
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = generate_state()
    
    params = {
        "client_id": APPLE_CLIENT_ID,
        "redirect_uri": APPLE_REDIRECT_URI,
        "response_type": "code",
        "response_mode": "form_post",
        "scope": "name email",
        "state": st.session_state.oauth_state
    }
    
    return f"https://appleid.apple.com/auth/authorize?{urllib.parse.urlencode(params)}"

def handle_google_callback(code, state):
    """Handle Google OAuth callback"""
    if state != st.session_state.get("oauth_state"):
        return None, "Invalid state parameter"
    
    # Exchange code for token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        tokens = response.json()
        
        if "access_token" not in tokens:
            return None, "Failed to get access token"
        
        # Get user info
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        user_response = requests.get(user_info_url, headers=headers)
        user_info = user_response.json()
        
        return user_info, None
    except Exception as e:
        return None, str(e)

def handle_github_callback(code, state):
    """Handle GitHub OAuth callback"""
    if state != st.session_state.get("oauth_state"):
        return None, "Invalid state parameter"
    
    # Exchange code for token
    token_url = "https://github.com/login/oauth/access_token"
    token_data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "state": state
    }
    
    try:
        response = requests.post(token_url, data=token_data, headers={"Accept": "application/json"})
        tokens = response.json()
        
        if "access_token" not in tokens:
            return None, "Failed to get access token"
        
        # Get user info
        user_info_url = "https://api.github.com/user"
        headers = {"Authorization": f"token {tokens['access_token']}"}
        user_response = requests.get(user_info_url, headers=headers)
        user_info = user_response.json()
        
        # Get email
        email_url = "https://api.github.com/user/emails"
        email_response = requests.get(email_url, headers=headers)
        emails = email_response.json()
        if emails:
            user_info["email"] = emails[0]["email"]
        
        return user_info, None
    except Exception as e:
        return None, str(e)

def handle_linkedin_callback(code, state):
    """Handle LinkedIn OAuth callback"""
    if state != st.session_state.get("oauth_state"):
        return None, "Invalid state parameter"
    
    # Exchange code for token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        tokens = response.json()
        
        if "access_token" not in tokens:
            return None, "Failed to get access token"
        
        # Get user info
        user_info_url = "https://api.linkedin.com/v2/me"
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        user_response = requests.get(user_info_url, headers=headers)
        user_info = user_response.json()
        
        # Get email
        email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
        email_response = requests.get(email_url, headers=headers)
        email_data = email_response.json()
        if email_data.get("elements"):
            user_info["email"] = email_data["elements"][0]["handle~"]["emailAddress"]
        
        return user_info, None
    except Exception as e:
        return None, str(e)

def handle_apple_callback(code, state):
    """Handle Apple OAuth callback"""
    if state != st.session_state.get("oauth_state"):
        return None, "Invalid state parameter"
    
    # Exchange code for token
    token_url = "https://appleid.apple.com/auth/token"
    token_data = {
        "client_id": APPLE_CLIENT_ID,
        "client_secret": APPLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": APPLE_REDIRECT_URI
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        tokens = response.json()
        
        if "access_token" not in tokens:
            return None, "Failed to get access token"
        
        # Apple provides user info in the ID token (JWT)
        # In production, you would decode the JWT to get user info
        # For now, return basic structure
        user_info = {
            "email": None,  # Apple may not provide email if user denied it
            "name": "Apple User",
            "id": tokens.get("id_token", "").split(".")[0] if "id_token" in tokens else ""
        }
        
        return user_info, None
    except Exception as e:
        return None, str(e)

def authenticate_with_provider(provider, user_info):
    """Store user info and authenticate user"""
    if provider == "google":
        username = user_info.get("email", user_info.get("name", "google_user"))
        display_name = user_info.get("name", username)
    elif provider == "github":
        username = user_info.get("email", user_info.get("login", "github_user"))
        display_name = user_info.get("name", user_info.get("login", username))
    elif provider == "linkedin":
        username = user_info.get("email", f"linkedin_{user_info.get('id', 'user')}")
        display_name = f"{user_info.get('localizedFirstName', '')} {user_info.get('localizedLastName', '')}".strip()
    elif provider == "apple":
        username = user_info.get("email", f"apple_{user_info.get('id', 'user')}")
        display_name = user_info.get("name", "Apple User")
    
    # Store or update user data
    existing_user = get_user_data(username)
    if existing_user:
        user_data = existing_user
    else:
        user_data = {
            "password": None,  # OAuth users don't have passwords
            "chat_history": [],
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "provider": provider,
            "oauth_user": True
        }
    
    user_data["last_login"] = time.strftime("%Y-%m-%d %H:%M:%S")
    user_data["display_name"] = display_name
    user_data["email"] = user_info.get("email", username)
    
    store_user_data(username, user_data)
    
    # Set session state
    st.session_state.authenticated = True
    st.session_state.current_user = username
    st.session_state.chat_history = user_data.get("chat_history", [])
    
    return username, display_name

# For demo purposes - simplified version that works without OAuth setup
def demo_oauth_login(provider):
    """Demo OAuth login that simulates successful authentication"""
    import time
    from google.api_core import exceptions as gcp_exceptions
    
    # Simulate user info based on provider
    if provider == "google":
        username = f"google_user_{secrets.token_hex(4)}"
        display_name = "Google User"
        email = f"{username}@gmail.com"
    elif provider == "github":
        username = f"github_user_{secrets.token_hex(4)}"
        display_name = "GitHub User"
        email = f"{username}@github.com"
    elif provider == "linkedin":
        username = f"linkedin_user_{secrets.token_hex(4)}"
        display_name = "LinkedIn User"
        email = f"{username}@linkedin.com"
    elif provider == "apple":
        username = f"apple_user_{secrets.token_hex(4)}"
        display_name = "Apple User"
        email = f"{username}@icloud.com"
    else:
        return False, "Invalid provider"
    
    try:
        # Store user data
        existing_user = get_user_data(username)
        if existing_user:
            user_data = existing_user
        else:
            user_data = {
                "password": None,
                "chat_history": [],
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "provider": provider,
                "oauth_user": True
            }
        
        user_data["last_login"] = time.strftime("%Y-%m-%d %H:%M:%S")
        user_data["display_name"] = display_name
        user_data["email"] = email
        
        # Try to store user data
        if not store_user_data(username, user_data):
            # If Firestore is not available, use session state only
            st.session_state.authenticated = True
            st.session_state.current_user = username
            st.session_state.chat_history = user_data.get("chat_history", [])
            return True, "Logged in (session only - Firestore not configured)"
        
        # Set session state
        st.session_state.authenticated = True
        st.session_state.current_user = username
        st.session_state.chat_history = user_data.get("chat_history", [])
        
        return True, "Success"
        
    except gcp_exceptions.NotFound as e:
        # Firestore database doesn't exist - use session state only
        st.session_state.authenticated = True
        st.session_state.current_user = username
        st.session_state.chat_history = []
        return True, "Logged in (session only - Firestore database not configured)"
    except Exception as e:
        return False, f"Error: {str(e)}"

