# Firestore Security Rules Setup

## Current Situation
Your app uses Firebase Admin SDK (server-side), which **bypasses security rules**. Rules only apply to client-side Firebase SDK.

## Option 1: Rules for Admin SDK (Current Setup)
Since Admin SDK bypasses rules, you can keep them permissive for now:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

**Note**: This is only safe because Admin SDK has its own authentication. For production, implement proper server-side validation.

## Option 2: Proper Security Rules (Recommended)
Use the rules in `firestore.rules` for better security:

### Features:
- ✅ Users can only read/write their own data
- ✅ Validates data structure on creation
- ✅ Prevents unauthorized access
- ✅ Allows chat history updates

### To Deploy:
1. Go to [Firebase Console](https://console.firebase.google.com/project/chatbot-6063d/firestore/rules)
2. Click "Edit rules"
3. Copy contents from `firestore.rules`
4. Click "Publish"

## Option 3: Switch to Client-Side SDK (Future)
If you want rules to be enforced, switch from Admin SDK to client-side Firebase SDK:

```python
# Instead of firebase_admin, use:
import firebase_admin
from firebase_admin import auth
import pyrebase  # or firebase library for client-side
```

This requires different authentication setup but respects security rules.

## Current Rules Status
Your current rules deny all access, but since you're using Admin SDK, they don't affect your app's functionality.

## Recommendation
For now, update rules to allow access since Admin SDK bypasses them anyway:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

Or use the secure rules from `firestore.rules` if you plan to add client-side access later.

