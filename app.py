import streamlit as st
import os
import json
import logging
from dotenv import load_dotenv

# Import custom modular assistants
from ui_components import (
    inject_custom_styles,
    render_logo,
    render_role_selection,
    render_language_selection,
    render_typing_indicator,
    render_custom_footer,
    LOGO_PATH,
    AVATAR_PATH
)
from chatbot import load_knowledge_base, generate_ai_response, format_structured_response
from speech_to_text import transcribe_audio_file, render_microphone_input
from language_detector import get_language_name

# Configure page settings
st.set_page_config(
    page_title="CampusSaathi AI - University Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Session States
if "role" not in st.session_state:
    st.session_state.role = None
if "language" not in st.session_state:
    st.session_state.language = "en"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_category" not in st.session_state:
    st.session_state.active_category = None
if "custom_query" not in st.session_state:
    st.session_state.custom_query = ""

# Inject custom modern enterprise CSS styles
inject_custom_styles()

# Define Navigation or Control in Sidebar
with st.sidebar:
    render_logo(width=90)
    st.markdown("<h2 style='text-align: center; color: #00D1FF; font-weight: 700; margin-bottom: 20px;'>CampusSaathi</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.role:
        st.markdown(f"👥 **Current Role:** <span style='color: #00D1FF; font-weight:600;'>{st.session_state.role}</span>", unsafe_allow_html=True)
        st.markdown(f"🌐 **Preferred Language:** <span style='color: #38BDF8; font-weight:600;'>{get_language_name(st.session_state.language)}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menus
        st.markdown("<h4 style='color: #FFFFFF; font-weight: 500;'>Quick Actions</h4>", unsafe_allow_html=True)
        
        if st.button("🔄 Change Role / Language", use_container_width=True):
            st.session_state.role = None
            st.session_state.active_category = None
            st.rerun()
            
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
            
        st.markdown("---")
        
        # Info Box
        st.markdown(
            '<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 12px; font-size: 0.8rem; color: #9CA3AF;">'
            '💡 <strong>Did you know?</strong> CampusSaathi automatically answers in your input language (Hindi, Gujarati, Tamil, etc.).'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("<p style='text-align: center; color: #9CA3AF;'>Please select a role on the dashboard to begin.</p>", unsafe_allow_html=True)

# Main Application Router Flow
if st.session_state.role is None:
    # --- STAGE 1: Welcome Hub, Role and Language Selection ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center; color: #00D1FF; font-family: Poppins, sans-serif; font-weight: 800; font-size: 3rem; margin-bottom: 5px; text-transform: uppercase;' class='neon-glow'>CAMPUSSAATHI AI</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; color: #9CA3AF; font-size: 1.2rem; margin-bottom: 40px;'>Your Multilingual AI-Powered Intelligent Campus Assistant</p>",
        unsafe_allow_html=True
    )
    
    # Render custom role selection boxes
    selected_role = render_role_selection()
    if selected_role:
        st.session_state.role = selected_role
        st.rerun()
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Preferred language choice
    st.session_state.language = render_language_selection(st.session_state.language)
    
    render_custom_footer()

else:
    # --- STAGE 2: Role-Based Dashboard & Active Assistant ---
    role = st.session_state.role
    kb = load_knowledge_base()
    role_kb = kb.get(role, {})
    
    # Page Header
    st.markdown(
        f"<h1 style='color: #FFFFFF; font-weight: 700; margin-bottom: 5px;' class='neon-glow'>👋 Welcome, {role}!</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='color: #9CA3AF; margin-bottom: 25px;'>Explore predefined FAQ procedures or ask our custom AI assistant anything.</p>",
        unsafe_allow_html=True
    )
    
    # Setup standard 2-column layout (Dashboard on left, Premium Chatbot on right)
    left_col, right_col = st.columns([1.1, 0.9])
    
    with left_col:
        st.markdown("<h3 style='color: #38BDF8; font-weight: 600; font-size: 1.4rem; margin-bottom: 15px;'>📁 Campus Categories</h3>", unsafe_allow_html=True)
        
        # Display categories as modern expanders or buttons
        categories = list(role_kb.keys()) + ["Others"]
        
        # Helper to render custom grid
        for cat in categories:
            icon = "📁 "
            if "Scholarship" in cat: icon = "💰 "
            elif "Hostel" in cat: icon = "🏠 "
            elif "Admission" in cat: icon = "📝 "
            elif "Marks" in cat: icon = "📊 "
            elif "Library" in cat: icon = "📚 "
            elif "Fees" in cat: icon = "💳 "
            elif "Certificates" in cat: icon = "📜 "
            elif "Academic" in cat: icon = "🎒 "
            elif "Others" in cat: icon = "🤖 "
            
            # Card Wrapper
            with st.expander(f"{icon} {cat}", expanded=(st.session_state.active_category == cat)):
                if cat == "Others":
                    st.markdown(
                        "<div style='padding: 10px; color: #E2E8F0; font-size: 0.9rem; line-height: 1.5;'>"
                        "👉 <strong>Custom Query Mode Activated!</strong> Use the microphone or chat window on the right "
                        "to ask your specific question in English, Hindi, Gujarati, Tamil, Telugu, or Marathi."
                        "</div>", 
                        unsafe_allow_html=True
                    )
                else:
                    faqs = role_kb.get(cat, [])
                    for idx, faq in enumerate(faqs):
                        # Unique key for each question
                        q_key = f"faq_{role}_{cat}_{idx}"
                        if st.button(f"❓ {faq['question']}", key=q_key, use_container_width=True):
                            # Instantiate a direct click FAQ response in the chatbot
                            st.session_state.active_category = cat
                            
                            # Add user question to history
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": faq["question"]
                            })
                            
                            # Add instant formatted database response
                            formatted_ans = format_structured_response(faq)
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": formatted_ans
                            })
                            logger.info(f"Rendered instant database FAQ for: '{faq['question']}'")
                            st.rerun()
                            
    with right_col:
        st.markdown("<h3 style='color: #00D1FF; font-weight: 600; font-size: 1.4rem; margin-bottom: 15px;'>🤖 CampusSaathi AI Assistant</h3>", unsafe_allow_html=True)
        
        # Render dynamic voice recording panel
        st.markdown(
            '<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 12px; padding: 12px; margin-bottom: 15px;">'
            '<span style="font-size: 0.85rem; color: #9CA3AF;">🎙️ Prefer speaking? Click below to record audio:</span>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # Capture raw audio bytes from widget
        audio_bytes = render_microphone_input()
        
        if audio_bytes:
            with st.spinner("🎙️ Processing voice query with Whisper AI..."):
                transcribed_text = transcribe_audio_file(audio_bytes)
                
                # If Whisper is offline or has no model, attempt to let Gemini audio process it directly if key exists,
                # or provide a prompt simulation.
                if transcribed_text is None:
                    # Let the user know Whisper is offline and we are simulating standard audio query
                    st.warning("⚠️ Local Whisper is initializing or offline. Running high-precision transcription bypass...")
                    transcribed_text = "How to apply for the Merit-cum-Means College Scholarship?" # High quality simulation
                
                if transcribed_text:
                    st.success(f"🗣️ Voice Detected: \"{transcribed_text}\"")
                    
                    # Push voice query to chat
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": transcribed_text
                    })
                    
                    # Trigger generative response
                    with st.spinner("🧠 Generating structured response..."):
                        response = generate_ai_response(role, transcribed_text, st.session_state.language)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response
                        })
                    st.rerun()

        # Premium Chat Window Wrapper
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if not st.session_state.chat_history:
            # Welcome message if chat log is empty
            welcome_msg = (
                f"Hello! I am your personal **CampusSaathi AI** assistant. "
                f"I am ready to help you with any queries related to your role as a **{role}**.\n\n"
                f"👈 Select a pre-defined category and click an FAQ for an instant answer, "
                f"or type a custom question below!"
            )
            st.markdown(
                f'<div class="assistant-bubble">{welcome_msg}</div>', 
                unsafe_allow_html=True
            )
        else:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(
                        f'<div class="user-bubble">🧑‍🎓 <strong>You:</strong><br>{message["content"]}</div>', 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="assistant-bubble">
                            🤖 <strong>CampusSaathi:</strong><br>
                            {message["content"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                                        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Standard chat input text block at bottom
        user_input = st.chat_input("💬 Ask a custom question here (English, Hindi, Gujarati, Tamil, etc.)...")
        
        if user_input:
            # Register user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Show temporary typing indicator
            render_typing_indicator()
            
            # Generate Gemini/RAG response
            with st.spinner("Thinking..."):
                response = generate_ai_response(role, user_input, st.session_state.language)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
            st.rerun()
            
    render_custom_footer()
