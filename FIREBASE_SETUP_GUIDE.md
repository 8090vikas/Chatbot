# Firebase Setup Guide

## Quick Setup for Chat History

### Option 1: Firebase Setup (Recommended)

1. **Go to [Firebase Console](https://console.firebase.google.com/)**
2. **Create a new project** or use existing one
3. **Enable Firestore Database**:
   - Go to Firestore Database
   - Click "Create database"
   - Choose "Start in test mode" (for development)
   - Select a location

4. **Create Service Account**:
   - Go to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Download the JSON file
   - Rename it to `firebase_service_account.json`
   - Place it in your project root directory

5. **Set Firestore Rules** (for production):
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

### Option 2: Session-Only Mode (No Setup Required)

If you don't want to set up Firebase, the app will work in session-only mode:
- Chat history will work during your session
- Data will be lost when you close the browser
- All other features work perfectly

### Option 3: Local File Storage (Alternative)

You can also save chat history to local files using the download buttons:
- **Download as Text**: Save as .txt file
- **Download as JSON**: Save as .json file
- **Manual backup**: Download and store locally

## Testing Firebase Setup

1. **Check if file exists**: Look for `firebase_service_account.json` in project root
2. **Test save**: Click "💾 Save Chat" button
3. **Should show**: "✅ Chat saved to Firebase!" instead of error
4. **Test load**: Click "📚 Load Previous Chat" button
5. **Should show**: "📚 Loaded X previous messages!" or "📭 No previous chat history found"

## Troubleshooting

- **"Firebase service account file not found"**: Download and place the service account JSON file
- **"Firestore database not found"**: Create Firestore database in Firebase Console
- **"Permission denied"**: Check Firestore security rules
- **Still not working**: Use session-only mode or local file downloads

## Cost Information

- **Firestore**: Free tier includes 50K reads, 20K writes, 1GB storage per day
- **For personal use**: Usually stays within free limits
- **Monitor usage**: Check Firebase Console for usage statistics
