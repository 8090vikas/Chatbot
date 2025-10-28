import streamlit as st
from firebase_utils import get_user_data, store_user_data, initialize_firebase
import time
from oauth_handler import demo_oauth_login

def show_loading_animation():
    with st.spinner("Processing..."):
        time.sleep(1)

def custom_css():
    st.markdown("""
        <style>
        /* Modern Glass Morphism Effect */
        .auth-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            margin: 2rem auto;
            max-width: 90%;
            border: 1px solid rgba(255, 255, 255, 0.18);
            transition: transform 0.3s ease;
        }
        .auth-container:hover {
            transform: translateY(-5px);
        }
        
        /* Gradient Text and Headers */
        .auth-header {
            background: linear-gradient(120deg, #4F46E5, #06B6D4);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            text-align: center;
            letter-spacing: -0.5px;
        }
        .auth-subheader {
            color: #6B7280;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 2.5rem;
            line-height: 1.6;
        }
        
        /* Modern Input Styling */
        .stTextInput input, .stTextInput div[data-baseweb="input"] {
            background: #F3F4F6 !important;
            border: 2px solid transparent !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            color: #111827 !important;
        }
        .stTextInput input::placeholder, .stTextInput div[data-baseweb="input"]::placeholder {
            color: #9CA3AF !important;
        }
        .stTextInput input:focus, .stTextInput div[data-baseweb="input"]:focus-within {
            background: white !important;
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1) !important;
            color: #111827 !important;
        }
        /* Ensure text input values are visible */
        .stTextInput input[type="text"],
        .stTextInput input[type="password"] {
            color: #111827 !important;
        }
        
        /* Button Styling */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #4F46E5, #06B6D4) !important;
            color: white !important;
            padding: 12px 24px !important;
            border-radius: 12px !important;
            border: none !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            margin-top: 1rem !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.23) !important;
        }
        
        /* Classic Social Login Buttons */
        button[key="google_login"],
        button[key="apple_login"] {
            background: white !important;
            color: #3c4043 !important;
            border: 1px solid #dadce0 !important;
            border-radius: 4px !important;
            padding: 12px 16px !important;
            width: 100% !important;
            margin: 8px 0 !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            text-transform: none !important;
            letter-spacing: 0.25px !important;
            box-shadow: 0 1px 2px 0 rgba(60,64,67,.3), 0 1px 3px 1px rgba(60,64,67,.15) !important;
            transition: background-color .218s, border-color .218s, box-shadow .218s !important;
            cursor: pointer !important;
        }
        button[key="google_login"]:hover,
        button[key="apple_login"]:hover {
            background: #f8f9fa !important;
            box-shadow: 0 1px 3px 0 rgba(60,64,67,.3), 0 4px 8px 3px rgba(60,64,67,.15) !important;
            border-color: #dadce0 !important;
        }
        button[key="google_login"]:active,
        button[key="apple_login"]:active {
            background: #f1f3f4 !important;
            box-shadow: 0 1px 2px 0 rgba(60,64,67,.3), 0 1px 3px 1px rgba(60,64,67,.15) !important;
        }
        /* Google specific styling */
        button[key="google_login"] {
            background: white !important;
        }
        /* Apple specific styling */
        button[key="apple_login"] {
            background: #000000 !important;
            color: white !important;
            border-color: #000000 !important;
        }
        button[key="apple_login"]:hover {
            background: #1a1a1a !important;
            border-color: #1a1a1a !important;
        }
        button[key="apple_login"]:active {
            background: #333333 !important;
        }
        
        /* Toggle Buttons */
        .auth-toggle {
            background: #F3F4F6;
            padding: 0.5rem;
            border-radius: 16px;
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
            position: relative;
        }
        .toggle-button {
            background-color: transparent;
            border: none;
            padding: 12px 32px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            color: #6B7280;
            position: relative;
            z-index: 1;
            transition: all 0.3s ease;
        }
        .toggle-button.active {
            color: #4F46E5;
        }
        
        /* Divider */
        .divider {
            text-align: center;
            margin: 1.5rem 0;
            position: relative;
            color: #6B7280;
        }
        .divider::before, .divider::after {
            content: "";
            position: absolute;
            top: 50%;
            width: 45%;
            height: 1px;
            background: linear-gradient(90deg, transparent, #E5E7EB, transparent);
        }
        .divider::before { left: 0; }
        .divider::after { right: 0; }
        
        /* Error Messages */
        .stAlert {
            border-radius: 12px !important;
            margin-top: 1rem !important;
        }
        
        /* Success Messages */
        .element-container:has(.stSuccess) {
            animation: slideIn 0.5s ease;
        }
        @keyframes slideIn {
            from { transform: translateY(-10px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        /* Page Background */
        .main .block-container {
            padding-top: 2rem !important;
            max-width: 800px !important;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .auth-container {
                padding: 1.5rem;
                margin: 1rem auto;
            }
            .auth-header {
                font-size: 2rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def auth_page():
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"

    custom_css()
    
    # Debug section (only show in development or when there are issues)
    if st.checkbox("🔧 Debug Firebase Connection", help="Check this to see Firebase connection status"):
        st.markdown("### 🔍 Firebase Debug Information")
        
        # Test Firebase initialization
        st.write("**Testing Firebase initialization...**")
        firebase_status = initialize_firebase()
        st.write(f"Firebase initialized: {firebase_status}")
        
        # Check Streamlit secrets
        try:
            if hasattr(st, 'secrets'):
                st.write("**Streamlit Secrets Available:**")
                if 'FIREBASE_PROJECT_ID' in st.secrets:
                    st.write(f"✅ FIREBASE_PROJECT_ID: {st.secrets['FIREBASE_PROJECT_ID']}")
                else:
                    st.write("❌ FIREBASE_PROJECT_ID not found in secrets")
                
                if 'FIREBASE_CLIENT_EMAIL' in st.secrets:
                    st.write(f"✅ FIREBASE_CLIENT_EMAIL: {st.secrets['FIREBASE_CLIENT_EMAIL']}")
                else:
                    st.write("❌ FIREBASE_CLIENT_EMAIL not found in secrets")
            else:
                st.write("❌ Streamlit secrets not available")
        except Exception as e:
            st.write(f"❌ Error accessing secrets: {e}")
        
        # Test user data operations
        test_username = "test_user_debug"
        st.write(f"**Testing user data operations with username: {test_username}**")
        
        # Test storing user data
        test_data = {"password": "test123", "chat_history": [], "test": True}
        store_result = store_user_data(test_username, test_data)
        st.write(f"Store user data result: {store_result}")
        
        # Test getting user data
        get_result = get_user_data(test_username)
        st.write(f"Get user data result: {get_result is not None}")
        if get_result:
            st.write(f"Retrieved data keys: {list(get_result.keys())}")
        
        st.markdown("---")
    
    # Add CSS for the toggle buttons
    st.markdown("""
        <style>
        .auth-toggle {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
        }
        .toggle-button {
            background-color: transparent;
            border: none;
            padding: 0.5rem 2rem;
            cursor: pointer;
            font-size: 1.1rem;
            position: relative;
        }
        .toggle-button.active {
            color: #1E88E5;
            font-weight: bold;
        }
        .toggle-button.active::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 3px;
            background-color: #1E88E5;
            border-radius: 3px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Modern toggle switch with sliding animation
    st.markdown("""
        <style>
        .toggle-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            width: 400px;
            margin: 0 auto 2rem auto;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .toggle-option {
            position: relative;
            z-index: 1;
            flex: 1;
            text-align: center;
            padding: 12px 24px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #6B7280;
            font-weight: 600;
            font-size: 1rem;
            user-select: none;
        }
        .toggle-slider {
            position: absolute;
            top: 5px;
            height: calc(100% - 10px);
            width: calc(50% - 10px);
            background: linear-gradient(135deg, #4F46E5, #06B6D4);
            border-radius: 15px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
        }
        .toggle-option.active {
            color: white;
        }
        .login-slider {
            left: 5px;
        }
        .signup-slider {
            left: calc(50% + 5px);
        }
        @media (max-width: 768px) {
            .toggle-container {
                width: 90%;
            }
        }
        /* Hover effect on inactive option */
        .toggle-option:not(.active):hover {
            color: #4F46E5;
        }
        </style>
        """, unsafe_allow_html=True)

    # Create the toggle switch with direct state management
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Style radio buttons to look like the toggle slider
        selected_index = 0 if st.session_state.auth_page == "login" else 1
        
        st.markdown("""
            <style>
            /* Hide default radio button styling */
            .stRadio > div {
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(10px) !important;
                border-radius: 20px !important;
                padding: 10px !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                position: relative !important;
                width: 400px !important;
                margin: 0 auto 2rem auto !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }
            
            /* Animated slider background */
            .stRadio > div {
                position: relative;
            }
            
            .stRadio > div::before {
                content: '';
                position: absolute;
                top: 5px;
                left: 5px;
                height: calc(100% - 10px);
                width: calc(50% - 10px);
                background: linear-gradient(135deg, #4F46E5, #06B6D4);
                border-radius: 15px;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
                z-index: 0;
            }
            
            /* Position slider for Sign Up */
            .stRadio > div:has(input[value="Sign Up"]:checked)::before {
                left: calc(50% + 5px);
            }
            
            /* Style radio options */
            .stRadio label {
                position: relative;
                z-index: 1;
                flex: 1;
                text-align: center;
                padding: 12px 24px;
                cursor: pointer;
                transition: all 0.3s ease;
                color: #6B7280;
                font-weight: 600;
                font-size: 1rem;
                user-select: none;
            }
            
            /* Active state */
            .stRadio input[type="radio"]:checked + label {
                color: white;
            }
            
            /* Hover effect on inactive option */
            .stRadio label:hover {
                color: #4F46E5;
            }
            
            /* Hide radio buttons */
            .stRadio input[type="radio"] {
                display: none;
            }
            
            @media (max-width: 768px) {
                .stRadio > div {
                    width: 90% !important;
                }
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Use radio buttons styled as toggle
        selected = st.radio(
            "Toggle",
            ["Sign In", "Sign Up"],
            index=selected_index,
            horizontal=True,
            label_visibility="collapsed",
            key="auth_toggle_radio"
        )
        
        # Update session state based on selection
        if selected == "Sign In" and st.session_state.auth_page != "login":
            st.session_state.auth_page = "login"
            st.rerun()
        elif selected == "Sign Up" and st.session_state.auth_page != "signup":
            st.session_state.auth_page = "signup"
            st.rerun()

    # Display the appropriate form based on the selected page
    if st.session_state.auth_page == "login":
        login_form()
    else:
        signup_form()

def login_form():
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('''
            <h2 class="auth-header">Welcome to the Future 👋</h2>
            <p class="auth-subheader">Experience the next generation of AI-powered conversations. 
            Your virtual assistant awaits.</p>
        ''', unsafe_allow_html=True)

        with st.form("login_form"):
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                username = st.text_input("📧 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                st.markdown("")  # Spacing
                login_button = st.form_submit_button("Sign In", use_container_width=True)

                if login_button:
                    if not username or not password:
                        st.error("Please fill in all fields")
                    else:
                        show_loading_animation()
                        user_data = get_user_data(username)
                        if user_data and user_data["password"] == password:
                            st.session_state.authenticated = True
                            st.session_state.current_user = username
                            st.session_state.chat_history = user_data.get("chat_history", [])
                            st.success("🎉 Login successful! Redirecting...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please try again.")

        st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown('<div class="social-buttons">', unsafe_allow_html=True)
            
            # Google OAuth - Classic Style
            if st.button("Sign in with Google", use_container_width=True, key="google_login"):
                with st.spinner("Connecting to Google..."):
                    time.sleep(0.5)
                    success, message = demo_oauth_login("google")
                    if success:
                        if "Firestore" in message:
                            st.warning(f"⚠️ {message}")
                        else:
                            st.success("🎉 Successfully logged in with Google!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Failed to authenticate with Google: {message}")
            
            # Apple OAuth - Classic Style
            if st.button("Sign in with Apple", use_container_width=True, key="apple_login"):
                with st.spinner("Connecting to Apple..."):
                    time.sleep(0.5)
                    success, message = demo_oauth_login("apple")
                    if success:
                        if "Firestore" in message:
                            st.warning(f"⚠️ {message}")
                        else:
                            st.success("🎉 Successfully logged in with Apple!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Failed to authenticate with Apple: {message}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    if login_button:
        user_data = get_user_data(username)
        if user_data and user_data["password"] == password:
            st.session_state.authenticated = True
            st.session_state.current_user = username
            st.session_state.chat_history = user_data.get("chat_history", [])
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")

def signup_form():
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('''
            <h2 class="auth-header">Innovate with AI 🚀</h2>
            <p class="auth-subheader">Join the elite community of innovators shaping the future of AI. 
            Your journey to unprecedented possibilities starts here.</p>
        ''', unsafe_allow_html=True)

        with st.form("signup_form"):
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                new_username = st.text_input("👤 Choose Username", placeholder="Enter desired username")
                new_password = st.text_input("🔒 Create Password", type="password", placeholder="Enter secure password")
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
                
                st.markdown("")  # Spacing
                signup_button = st.form_submit_button("Create Account", use_container_width=True)

                if signup_button:
                    if not new_username or not new_password or not confirm_password:
                        st.error("Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        show_loading_animation()
                        user_data = get_user_data(new_username)
                        if user_data:
                            st.error("Username already exists. Please choose a different one.")
                        else:
                            store_user_data(new_username, {
                                "password": new_password,
                                "chat_history": [],
                                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "last_login": time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                            st.success("🎉 Account created successfully! Please log in.")

        st.markdown('</div>', unsafe_allow_html=True)

    if signup_button:
        user_data = get_user_data(new_username)
        if user_data:
            st.error("Username already exists. Please choose a different one.")
        else:
            store_user_data(new_username, {"password": new_password, "chat_history": []})
            st.success("Account created successfully! Please log in.")