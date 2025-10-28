# Firebase Setup for Production Deployment

## Step-by-Step Firebase Setup

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter project name: `your-chatbot-project`
4. Enable Google Analytics (optional)
5. Click "Create project"

### 2. Enable Firestore Database
1. In Firebase Console, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (we'll secure it later)
4. Select a location (choose closest to your users)
5. Click "Done"

### 3. Create Service Account
1. Go to Project Settings (gear icon) → "Service accounts"
2. Click "Generate new private key"
3. Download the JSON file
4. Rename it to `firebase_service_account.json`
5. Place it in your project root directory

### 4. Set Up Firestore Security Rules
1. Go to Firestore Database → "Rules" tab
2. Replace the rules with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Allow authenticated users to read/write their own chat history
    match /chat_history/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### 5. Enable Authentication
1. Go to "Authentication" → "Sign-in method"
2. Enable "Email/Password"
3. Enable "Google" (optional)
4. Enable "Apple" (optional)

### 6. Test Your Setup
1. Place `firebase_service_account.json` in your project root
2. Restart your Streamlit app
3. Try saving chat history - should work now!

## Project Structure After Setup
```
Chatbot/
├── firebase_service_account.json  ← Your downloaded service account
├── user_data/                    ← Local fallback (can be deleted later)
├── chatbot.py
├── firebase_utils.py
├── auth.py
└── ...
```

## For Production Deployment

### Environment Variables (Recommended)
Instead of the JSON file, use environment variables:

```bash
export FIREBASE_PROJECT_ID="your-project-id"
export FIREBASE_PRIVATE_KEY_ID="your-private-key-id"
export FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
export FIREBASE_CLIENT_EMAIL="your-service-account@your-project.iam.gserviceaccount.com"
export FIREBASE_CLIENT_ID="your-client-id"
```

### Update firebase_utils.py for Production
```python
import os
import json

def get_firebase_credentials():
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
```

## Cost Information
- **Firestore**: Free tier includes 50K reads, 20K writes, 1GB storage per day
- **Authentication**: Free for up to 10K users
- **For most personal/small business apps**: Stays within free limits

## Next Steps
1. Follow the setup steps above
2. Test locally with Firebase
3. When ready to deploy, use environment variables
4. Remove local file storage fallback for production
