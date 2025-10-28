import streamlit as st
from firebase_utils import save_chat_history, get_user_data
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
import json
import os
from datetime import datetime

# --- Enhanced Prompt Templates ---
def get_prompt_template(personality="helpful"):
    templates = {
        "helpful": "You are a helpful, knowledgeable assistant. Provide clear, accurate, and detailed responses.",
        "creative": "You are a creative assistant with a flair for storytelling and imaginative solutions.",
        "professional": "You are a professional business assistant. Provide concise, business-focused responses.",
        "friendly": "You are a friendly, conversational assistant. Be warm, engaging, and personable.",
        "technical": "You are a technical expert. Provide detailed, accurate technical information and solutions."
    }
    
    return ChatPromptTemplate.from_messages([
        ("system", templates.get(personality, templates["helpful"])),
        ("user", "{question}")
    ])

# --- Custom CSS for Enhanced UI ---
def load_custom_css():
    st.markdown("""
        <style>
        /* Main Container */
        .main .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            max-width: 1200px !important;
        }
        
        /* Chat Messages */
        .stChatMessage {
            margin-bottom: 1rem !important;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        /* Custom Buttons */
        .custom-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .custom-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
        }
        
        /* Stats Cards */
        .stats-card {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Model Selector */
        .model-selector {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
            margin: 0.5rem 0 !important;
        }
        
        /* File Upload Area */
        .uploadedFile {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
            margin: 0.5rem 0 !important;
        }
        
        /* Chat Input Enhancement */
        .stChatInput > div > div {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Welcome Message */
        .welcome-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border-radius: 16px !important;
            padding: 2rem !important;
            margin: 1rem 0 !important;
            color: white !important;
            text-align: center !important;
        }
        
        /* Feature Cards */
        .feature-card {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            transition: transform 0.3s ease !important;
        }
        
        .feature-card:hover {
            transform: translateY(-5px) !important;
        }
        
        /* Typing Animation */
        .typing-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #667eea;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-indicator:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        </style>
    """, unsafe_allow_html=True)

# --- Enhanced Chatbot UI ---
def chatbot_ui():
    load_custom_css()
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_user" not in st.session_state:
        st.session_state.current_user = "Anonymous_User"
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "gpt-3.5-turbo"
    if "personality" not in st.session_state:
        st.session_state.personality = "helpful"
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "message_count" not in st.session_state:
        st.session_state.message_count = 0
    if "chat_history_loaded" not in st.session_state:
        st.session_state.chat_history_loaded = False
    
    # Get user data and load chat history from Firebase
    user_data = get_user_data(st.session_state.current_user)
    display_name = user_data.get("display_name", st.session_state.current_user) if user_data else st.session_state.current_user
    
    # Load chat history from Firebase
    if not st.session_state.chat_history_loaded:
        if user_data and user_data.get("chat_history"):
            st.session_state.chat_history = user_data.get("chat_history", [])
            st.session_state.message_count = len(st.session_state.chat_history)
            st.session_state.chat_history_loaded = True
            st.success(f"📚 Loaded {len(st.session_state.chat_history)} previous messages!")
        elif user_data is None:
            # Firebase not configured or user not found
            st.session_state.chat_history_loaded = True
            st.info("💡 Firebase not configured - chat history will be session-only")
        else:
            # User exists but no chat history
            st.session_state.chat_history_loaded = True
            st.info("📭 No previous chat history found for this user")
    
    # Check if we need to refresh chat history (for logout/login scenarios)
    elif st.session_state.chat_history_loaded and user_data and user_data.get("chat_history"):
        # Check if the loaded chat history is different from what's in Firebase
        firebase_chat_history = user_data.get("chat_history", [])
        if len(firebase_chat_history) != len(st.session_state.chat_history):
            st.session_state.chat_history = firebase_chat_history
            st.session_state.message_count = len(firebase_chat_history)
            st.success(f"📚 Refreshed chat history - {len(firebase_chat_history)} messages loaded!")
            st.rerun()
    
    # --- Enhanced Sidebar ---
    with st.sidebar:
        st.markdown(f"""
            <div class="welcome-container">
                <h3>👋 Welcome, {display_name}!</h3>
                <p>Ready to chat with AI?</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Settings")
        
        # Model Selection
        st.markdown("**🤖 AI Model**")
        model_options = {
            # OpenAI Models
            "GPT-3.5 Turbo": "gpt-3.5-turbo",
            "GPT-4": "gpt-4",
            "GPT-4 Turbo": "gpt-4-turbo-preview",
            # Google Gemini Models
            "Gemini Pro": "gemini-pro",
            "Gemini Pro Vision": "gemini-pro-vision"
        }
        selected_model_name = st.selectbox(
            "Choose AI Model",
            options=list(model_options.keys()),
            index=list(model_options.keys()).index([k for k, v in model_options.items() if v == st.session_state.selected_model][0]) if st.session_state.selected_model in model_options.values() else 0,
            key="model_selector"
        )
        st.session_state.selected_model = model_options[selected_model_name]
        
        # Personality Selection
        st.markdown("**🎭 AI Personality**")
        personality_options = {
            "🤝 Helpful": "helpful",
            "🎨 Creative": "creative", 
            "💼 Professional": "professional",
            "😊 Friendly": "friendly",
            "🔧 Technical": "technical"
        }
        selected_personality_name = st.selectbox(
            "Choose AI Personality",
            options=list(personality_options.keys()),
            index=list(personality_options.values()).index(st.session_state.personality),
            key="personality_selector"
        )
        st.session_state.personality = personality_options[selected_personality_name]
        
        st.markdown("---")
        
        # File Upload
        st.markdown("### 📁 Upload Files")
        uploaded_files = st.file_uploader(
            "Upload documents for context",
            accept_multiple_files=True,
            type=['txt', 'pdf', 'docx', 'md'],
            help="Upload files to provide context for the AI"
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            for file in uploaded_files:
                st.success(f"📄 {file.name}")
        
        st.markdown("---")
        
        # Chat Statistics
        st.markdown("### 📊 Chat Statistics")
        st.markdown(f"""
            <div class="stats-card">
                <strong>Messages:</strong> {st.session_state.message_count}<br>
                <strong>Model:</strong> {st.session_state.selected_model}<br>
                <strong>Personality:</strong> {selected_personality_name}<br>
                <strong>Files:</strong> {len(st.session_state.uploaded_files)}
            </div>
        """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.message_count = 0
                st.rerun()
        
        with col2:
            if st.button("💾 Save Chat", use_container_width=True):
                if st.session_state.chat_history:
                    success = save_chat_history(st.session_state.current_user, st.session_state.chat_history)
                    if success:
                        st.success("✅ Chat saved to Firebase!")
                    else:
                        st.error("❌ Failed to save chat. Check Firebase configuration.")
                else:
                    st.warning("⚠️ No chat history to save.")
        
        # Load Previous Chat Button
        if st.button("📚 Load Previous Chat", use_container_width=True):
            user_data = get_user_data(st.session_state.current_user)
            if user_data is None:
                st.error("❌ Firebase not configured. Please set up Firebase to save chat history.")
            elif user_data and user_data.get("chat_history"):
                st.session_state.chat_history = user_data.get("chat_history", [])
                st.session_state.message_count = len(st.session_state.chat_history)
                st.session_state.chat_history_loaded = True
                st.success(f"📚 Loaded {len(st.session_state.chat_history)} previous messages!")
                st.rerun()
            else:
                st.info("📭 No previous chat history found for this user.")
        
        # Debug Button (for troubleshooting)
        if st.button("🔍 Debug Chat History", use_container_width=True):
            user_data = get_user_data(st.session_state.current_user)
            st.write("**Debug Information:**")
            st.write(f"Current User: {st.session_state.current_user}")
            st.write(f"User Data Exists: {user_data is not None}")
            if user_data:
                st.write(f"Chat History in Firebase: {len(user_data.get('chat_history', []))} messages")
                st.write(f"Current Session Chat History: {len(st.session_state.chat_history)} messages")
                st.write(f"Chat History Loaded Flag: {st.session_state.chat_history_loaded}")
            else:
                st.write("No user data found in Firebase")
        
        # Logout Button
        st.markdown("### 🚪 Account")
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            # Save current chat history before logout
            if st.session_state.chat_history:
                success = save_chat_history(st.session_state.current_user, st.session_state.chat_history)
                if success:
                    st.success("💾 Chat history saved before logout!")
                else:
                    st.warning("⚠️ Chat history not saved - Firebase not configured")
            
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Force refresh to go back to auth page
            st.rerun()
        
        st.markdown("---")
        
        # API Key Setup Section
        st.markdown("### 🔑 API Keys Setup")
        
        # Initialize API keys in session state
        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = ""
        if "google_api_key" not in st.session_state:
            st.session_state.google_api_key = ""
        
        # OpenAI API Key Input
        st.markdown("**OpenAI API Key**")
        openai_key_input = st.text_input(
            "Enter your OpenAI API Key",
            value=st.session_state.openai_api_key,
            type="password",
            placeholder="sk-...",
            help="Get your API key from https://platform.openai.com/api-keys",
            key="openai_key_input"
        )
        
        # Google API Key Input
        st.markdown("**Google API Key**")
        google_key_input = st.text_input(
            "Enter your Google API Key",
            value=st.session_state.google_api_key,
            type="password",
            placeholder="AI...",
            help="Get your API key from https://makersuite.google.com/app/apikey",
            key="google_key_input"
        )
        
        # Update session state when API keys change
        if openai_key_input != st.session_state.openai_api_key:
            st.session_state.openai_api_key = openai_key_input
            st.rerun()
        
        if google_key_input != st.session_state.google_api_key:
            st.session_state.google_api_key = google_key_input
            st.rerun()
        
        # Show status for both API keys
        openai_valid = st.session_state.openai_api_key and st.session_state.openai_api_key.startswith("sk-")
        google_valid = st.session_state.google_api_key and st.session_state.google_api_key.startswith("AI")
        
        if openai_valid:
            st.success("✅ OpenAI API key configured!")
        elif st.session_state.openai_api_key:
            st.error("❌ Invalid OpenAI API key format. Should start with 'sk-'")
        
        if google_valid:
            st.success("✅ Google API key configured!")
        elif st.session_state.google_api_key:
            st.error("❌ Invalid Google API key format. Should start with 'AI'")
        
        if not openai_valid and not google_valid:
            st.warning("⚠️ Enter at least one API key to enable AI responses")
        
        # Quick setup instructions
        with st.expander("📖 How to get API keys"):
            st.markdown("""
            **OpenAI API Key:**
            1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
            2. Sign in or create an account
            3. Click "Create new secret key"
            4. Copy the key (starts with `sk-`)
            
            **Google API Key:**
            1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Sign in with your Google account
            3. Click "Create API key"
            4. Copy the key (starts with `AI`)
            
            **Cost**: 
            - GPT-3.5 Turbo ~$0.002 per 1K tokens
            - Gemini Pro ~$0.0005 per 1K tokens
            """)
        
        st.markdown("---")
        
        # About Section
        st.markdown("### 📄 About")
        st.info("""
        **Enhanced AI Chatbot** 🤖
        
        Features:
        • Multiple AI models
        • Personality modes
        • File upload support
        • Chat history
        • Real-time responses
        """)
        
        st.markdown("**Developed by Vikas Gupta 💻**")
    
    # --- Main Chat Interface ---
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; 
                       background-clip: text; 
                       color: transparent; 
                       font-size: 3rem; 
                       font-weight: 800;">
                🤖 AI Chatbot
            </h1>
            <p style="color: #6B7280; font-size: 1.2rem;">
                Your intelligent conversation partner
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h4>🧠 Smart AI</h4>
                <p>Powered by OpenAI's latest models</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h4>📁 File Support</h4>
                <p>Upload documents for context</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h4>💾 Persistent</h4>
                <p>Chat history saved securely</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Chat Container
    chat_container = st.container()
    
    # Display Chat History
    with chat_container:
        if st.session_state.chat_history:
            for i, (user_msg, bot_reply) in enumerate(st.session_state.chat_history):
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(user_msg)
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(bot_reply)
        else:
            st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #6B7280;">
                    <h3>👋 Start a conversation!</h3>
                    <p>Ask me anything - I'm here to help!</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Input Section
    # Update placeholder based on API key status
    openai_valid = st.session_state.openai_api_key and st.session_state.openai_api_key.startswith("sk-")
    google_valid = st.session_state.google_api_key and st.session_state.google_api_key.startswith("AI")
    
    if openai_valid or google_valid:
        placeholder = f"Ask me anything... (Using {st.session_state.selected_model})"
    else:
        placeholder = "Enter at least one API key in the sidebar first..."
    
    user_input = st.chat_input(
        placeholder,
        key="chat_input"
    )
    
    if user_input:
        # Update message count
        st.session_state.message_count += 1
        
        # Add user message to history
        st.session_state.chat_history.append((user_input, ""))
        
        # Generate response with typing animation
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Check if any API key is available
                    openai_valid = st.session_state.openai_api_key and st.session_state.openai_api_key.startswith("sk-")
                    google_valid = st.session_state.google_api_key and st.session_state.google_api_key.startswith("AI")
                    
                    if not openai_valid and not google_valid:
                        # Demo response when no API key
                        demo_responses = {
                            "hello": "Hello! 👋 I'm your AI assistant. Please enter at least one API key (OpenAI or Google) in the sidebar to enable real AI responses.",
                            "help": "I can help you with various tasks! Enter an API key in the sidebar to unlock my full potential.",
                            "what": "I'm an AI chatbot powered by OpenAI and Google Gemini. Enter an API key in the sidebar to start chatting with real AI responses.",
                            "api": "To get API keys: 1) OpenAI: https://platform.openai.com/api-keys 2) Google: https://makersuite.google.com/app/apikey",
                        }
                        
                        # Simple keyword matching for demo
                        user_lower = user_input.lower()
                        response = "Thanks for your message! 🤖 To get real AI responses, please enter at least one API key in the sidebar. Click 'How to get API keys' for instructions."
                        
                        for keyword, demo_response in demo_responses.items():
                            if keyword in user_lower:
                                response = demo_response
                                break
                    else:
                        # Determine which model to use based on selection and available API keys
                        model_name = st.session_state.selected_model
                        
                        if model_name.startswith("gpt-"):
                            # Use OpenAI models
                            if not openai_valid:
                                response = "❌ OpenAI API key required for GPT models. Please enter your OpenAI API key in the sidebar."
                            else:
                                llm = ChatOpenAI(
                                    model=model_name,
                                    api_key=st.session_state.openai_api_key
                                )
                                prompt = get_prompt_template(st.session_state.personality)
                                output_parser = StrOutputParser()
                                chain = prompt | llm | output_parser
                                response = chain.invoke({"question": user_input})
                        
                        elif model_name.startswith("gemini-"):
                            # Use Google Gemini models
                            if not google_valid:
                                response = "❌ Google API key required for Gemini models. Please enter your Google API key in the sidebar."
                            else:
                                llm = ChatGoogleGenerativeAI(
                                    model=model_name,
                                    google_api_key=st.session_state.google_api_key
                                )
                                prompt = get_prompt_template(st.session_state.personality)
                                output_parser = StrOutputParser()
                                chain = prompt | llm | output_parser
                                response = chain.invoke({"question": user_input})
                        
                        else:
                            response = "❌ Unknown model selected. Please choose a valid model."
                    
                    # Update the last message in history
                    st.session_state.chat_history[-1] = (user_input, response)
                    
                    # Save to Firebase
                    save_chat_history(st.session_state.current_user, st.session_state.chat_history)

                    # Display response
                    st.markdown(response)
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.session_state.chat_history[-1] = (user_input, error_msg)
                    st.error(error_msg)
        
        # Rerun to show the new messages
        st.rerun()
    
    # Download and Export Options
    if st.session_state.chat_history:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download as text
            chat_text = "\n\n".join([f"User: {q}\nBot: {a}" for q, a in st.session_state.chat_history])
            st.download_button(
                "📥 Download as Text",
                chat_text,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                use_container_width=True
            )

        with col2:
            # Download as JSON
            chat_json = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                "📄 Download as JSON",
                chat_json,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            # Export to Firebase
            if st.button("☁️ Save to Cloud", use_container_width=True):
                save_chat_history(st.session_state.current_user, st.session_state.chat_history)
                st.success("✅ Chat saved to cloud!")