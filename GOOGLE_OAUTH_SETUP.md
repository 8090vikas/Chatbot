# Google OAuth Setup Guide

## Step 1: Complete Project Settings
In Google Cloud Console:
- **Public-facing name**: Enter your app name (e.g., "Chatbot" or "AI Chatbot")
- **Support email**: vikas2000.gupta@gmail.com (already filled)
- Click "Save and Continue"

## Step 2: Configure OAuth Consent Screen
1. Choose **User Type**: Select "External" (unless you have a Google Workspace)
2. Fill in required fields:
   - **App name**: Your app name
   - **User support email**: vikas2000.gupta@gmail.com
   - **Developer contact information**: vikas2000.gupta@gmail.com
3. Click "Save and Continue"
4. Add scopes (if needed):
   - email
   - profile
   - openid
5. Add test users (for testing before publishing):
   - Add your Google account email
6. Review and continue

## Step 3: Create OAuth 2.0 Credentials
1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Choose **Application type**: Web application
4. Configure:
   - **Name**: Chatbot OAuth Client
   - **Authorized JavaScript origins**: 
     - `http://localhost:8501` (for local development)
     - `https://chatbot-6063d.firebaseapp.com` (for production)
   - **Authorized redirect URIs**:
     - `http://localhost:8501/oauth2callback/google` (for local)
     - `https://chatbot-6063d.firebaseapp.com/oauth2callback/google` (for production)
5. Click **Create**
6. Copy the **Client ID** and **Client Secret**

## Step 4: Update Your Code
Update `oauth_handler.py` with your credentials:

```python
GOOGLE_CLIENT_ID = "YOUR_ACTUAL_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "YOUR_ACTUAL_CLIENT_SECRET"
GOOGLE_REDIRECT_URI = "http://localhost:8501/oauth2callback/google"  # Change for production
```

## Step 5: Enable Required APIs
Make sure these APIs are enabled:
- Google+ API (or Google Identity API)
- Google OAuth2 API

Go to **APIs & Services** > **Library** and enable these APIs.

## Important Notes:
- Keep your Client Secret secure - never commit it to public repositories
- Use environment variables or Streamlit secrets for production
- For production, update redirect URIs to your deployed URL
- Test with test users first before publishing

