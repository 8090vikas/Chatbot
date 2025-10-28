#!/usr/bin/env python3
"""
Test script to verify Firebase connection and user operations
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_firebase_connection():
    print("🧪 Testing Firebase Connection...")
    
    try:
        from firebase_utils import initialize_firebase, store_user_data, get_user_data
        
        # Test Firebase initialization
        print("1. Testing Firebase initialization...")
        firebase_status = initialize_firebase()
        print(f"   Firebase initialized: {firebase_status}")
        
        if not firebase_status:
            print("❌ Firebase initialization failed!")
            return False
        
        # Test user data operations
        test_username = "test_user_connection"
        test_data = {
            "password": "test123",
            "chat_history": [],
            "test": True,
            "created_at": "2024-01-01 00:00:00"
        }
        
        print(f"2. Testing user data storage for: {test_username}")
        store_result = store_user_data(test_username, test_data)
        print(f"   Store result: {store_result}")
        
        print(f"3. Testing user data retrieval for: {test_username}")
        get_result = get_user_data(test_username)
        print(f"   Get result: {get_result is not None}")
        
        if get_result:
            print(f"   Retrieved data keys: {list(get_result.keys())}")
            print("✅ Firebase connection test successful!")
            return True
        else:
            print("❌ Could not retrieve user data!")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_firebase_connection()
    if success:
        print("\n🎉 All tests passed! Firebase is working correctly.")
    else:
        print("\n💥 Tests failed! Check Firebase configuration.")
        sys.exit(1)
