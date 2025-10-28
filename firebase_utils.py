import firebase_admin
from firebase_admin import credentials, firestore
from google.api_core import exceptions as gcp_exceptions
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase with error handling
db = None
firebase_initialized = False

def get_firebase_credentials():
    """Get Firebase credentials from environment variables or JSON file"""
    # Try environment variables first (for production)
    if os.getenv('FIREBASE_PROJECT_ID'):
        return {
            "type": "service_account",
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.getenv('FIREBASE_PRIVATE_KEY'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    
    # Fallback to JSON file (for development)
    elif os.path.exists("firebase_service_account.json"):
        with open("firebase_service_account.json", 'r') as f:
            return json.load(f)
    
    return None

def initialize_firebase():
    global db, firebase_initialized
    
    if firebase_initialized:
        return True
    
    try:
        # Get credentials from environment or file
        cred_data = get_firebase_credentials()
        
        if cred_data:
            # Create temporary file for credentials
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(cred_data, temp_file)
                temp_file_path = temp_file.name
            
            try:
                cred = credentials.Certificate(temp_file_path)
                if not firebase_admin._apps:
                    firebase_admin.initialize_app(cred)
                db = firestore.client()
                firebase_initialized = True
                print("✅ Firebase initialized successfully")
                return True
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
        else:
            print("⚠️ Firebase credentials not found. Using local file storage.")
            return False
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}. Using local file storage.")
        return False

def store_user_data(username, data):
    if not initialize_firebase():
        return store_user_data_local(username, data)
    
    try:
        db.collection("users").document(username).set(data)
        return True
    except gcp_exceptions.NotFound as e:
        print(f"Firestore database not found. Using local file storage: {e}")
        return store_user_data_local(username, data)
    except Exception as e:
        print(f"Error storing user data: {e}. Using local file storage.")
        return store_user_data_local(username, data)

def get_user_data(username):
    if not initialize_firebase():
        return get_user_data_local(username)
    
    try:
        doc = db.collection("users").document(username).get()
        if doc.exists:
            data = doc.to_dict()
            
            # Convert Firebase chat history format back to tuple format
            if "chat_history" in data and isinstance(data["chat_history"], list):
                firebase_chat_history = data["chat_history"]
                # Convert back to tuple format for compatibility
                converted_chat_history = []
                for msg in firebase_chat_history:
                    if isinstance(msg, dict) and "user_message" in msg and "bot_reply" in msg:
                        converted_chat_history.append((msg["user_message"], msg["bot_reply"]))
                    elif isinstance(msg, (list, tuple)) and len(msg) == 2:
                        # Handle old format (tuples)
                        converted_chat_history.append(tuple(msg))
                
                data["chat_history"] = converted_chat_history
            
            return data
        return None
    except gcp_exceptions.NotFound as e:
        print(f"Firestore database not found. Using local file storage: {e}")
        return get_user_data_local(username)
    except Exception as e:
        print(f"Error getting user data: {e}. Using local file storage.")
        return get_user_data_local(username)

def save_chat_history(username, chat_history):
    if not initialize_firebase():
        return save_chat_history_local(username, chat_history)
    
    try:
        # Convert chat history to Firebase-compatible format
        # Firebase doesn't support nested arrays, so we convert to a list of objects
        firebase_chat_history = []
        for i, (user_msg, bot_reply) in enumerate(chat_history):
            firebase_chat_history.append({
                "message_id": i,
                "user_message": user_msg,
                "bot_reply": bot_reply,
                "timestamp": datetime.now().isoformat()
            })
        
        # Use set with merge=True to create document if it doesn't exist
        db.collection("users").document(username).set({
            "chat_history": firebase_chat_history,
            "last_updated": datetime.now().isoformat()
        }, merge=True)
        print(f"Chat history saved for user: {username}")
        return True
    except gcp_exceptions.NotFound as e:
        print(f"Firestore database not found. Using local file storage: {e}")
        return save_chat_history_local(username, chat_history)
    except Exception as e:
        print(f"Error saving chat history: {e}. Using local file storage.")
        return save_chat_history_local(username, chat_history)

# Local file storage functions
def store_user_data_local(username, data):
    try:
        # Create data directory if it doesn't exist
        os.makedirs("user_data", exist_ok=True)
        
        # Save user data to local file
        file_path = f"user_data/{username}.json"
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ User data saved locally for: {username}")
        return True
    except Exception as e:
        print(f"❌ Error saving user data locally: {e}")
        return False

def get_user_data_local(username):
    try:
        file_path = f"user_data/{username}.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        return None
    except Exception as e:
        print(f"❌ Error loading user data locally: {e}")
        return None

def save_chat_history_local(username, chat_history):
    try:
        # Create data directory if it doesn't exist
        os.makedirs("user_data", exist_ok=True)
        
        # Load existing user data or create new
        user_data = get_user_data_local(username) or {}
        user_data["chat_history"] = chat_history
        user_data["last_updated"] = datetime.now().isoformat()
        
        # Save updated data
        file_path = f"user_data/{username}.json"
        with open(file_path, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        print(f"✅ Chat history saved locally for: {username}")
        return True
    except Exception as e:
        print(f"❌ Error saving chat history locally: {e}")
        return False