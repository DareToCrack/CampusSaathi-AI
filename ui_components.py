import os
import streamlit as st
import base64

# Define paths to asset files relative to this folder
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
AVATAR_PATH = os.path.join(os.path.dirname(__file__), "assets", "avatar.png")
STYLE_PATH = os.path.join(os.path.dirname(__file__), "assets", "styles.css")

def get_base64_image(image_path: str) -> str:
    """
    Converts a local image file into a base64 string for direct HTML embedding.
    """
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

def inject_custom_styles():
    """
    Reads the assets/styles.css file and injects it directly into Streamlit to customize
    backgrounds, fonts, buttons, cards, and animations.
    """
    if os.path.exists(STYLE_PATH):
        with open(STYLE_PATH, "r") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Fallback CSS in case the external sheet is missing
        st.markdown("""
            <style>
                html, body, [data-testid="stAppViewContainer"] {
                    background: #0B0F19 !important;
                    color: #FFFFFF !important;
                    font-family: sans-serif;
                }
            </style>
        """, unsafe_allow_html=True)

    # Hide default Streamlit elements to achieve a fully custom production look
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}
        </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

def render_logo(width=80):
    """
    Renders the premium campus logo in HTML.
    """
    base64_logo = get_base64_image(LOGO_PATH)
    if base64_logo:
        st.markdown(
            f'<div style="text-align: center; margin-bottom: 15px;">'
            f'<img src="{base64_logo}" width="{width}" style="border-radius: 12px; filter: drop-shadow(0px 0px 8px rgba(0, 209, 255, 0.4));">'
            f'</div>',
            unsafe_allow_html=True
        )

def render_role_selection():
    """
    Renders custom HTML boxes for selecting the Student, Staff, or Parent roles.
    Returns the selected role or None (state is managed by caller).
    """
    st.markdown("<h3 style='text-align: center; color: #FFFFFF; font-weight: 600; margin-bottom: 25px;'>WHO ARE YOU REGISTERING AS?</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            '<div class="role-box">'
            '<div class="role-icon">🎓</div>'
            '<h4 style="color: #FFFFFF; margin: 0; font-weight: 600;">Student</h4>'
            '<p style="color: #9CA3AF; font-size: 0.85rem; margin-top: 8px;">Access academic, hostel, and fee assistance.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Access as Student", key="role_student", use_container_width=True):
            return "Student"
            
    with col2:
        st.markdown(
            '<div class="role-box">'
            '<div class="role-icon">👨‍🏫</div>'
            '<h4 style="color: #FFFFFF; margin: 0; font-weight: 600;">Teacher/Staff</h4>'
            '<p style="color: #9CA3AF; font-size: 0.85rem; margin-top: 8px;">Access departments, timetables, and offices.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Access as Teacher/Staff", key="role_staff", use_container_width=True):
            return "Teacher/Staff"
            
    with col3:
        st.markdown(
            '<div class="role-box">'
            '<div class="role-icon">👪</div>'
            '<h4 style="color: #FFFFFF; margin: 0; font-weight: 600;">Parent</h4>'
            '<p style="color: #9CA3AF; font-size: 0.85rem; margin-top: 8px;">Track academic reports, hostels, and visits.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Access as Parent", key="role_parent", use_container_width=True):
            return "Parent"
            
    return None

def render_language_selection(current_lang="en"):
    """
    Renders custom HTML chips showing language options.
    Returns the selected language code.
    """
    st.markdown("<h4 style='color: #38BDF8; font-weight: 500; font-size: 1.1rem; margin-top: 20px; margin-bottom: 10px;'>Preferred Language / preferred भाषा:</h4>", unsafe_allow_html=True)
    
    languages = [
        {"code": "en", "name": "English"},
        {"code": "hi", "name": "हिन्दी (Hindi)"},
        {"code": "gu", "name": "ગુજરાતી (Gujarati)"},
        {"code": "ta", "name": "தமிழ் (Tamil)"},
        {"code": "te", "name": "తెలుగు (Telugu)"},
        {"code": "mr", "name": "मराठी (Marathi)"}
    ]
    
    # We display these as interactive Streamlit buttons side by side
    cols = st.columns(6)
    selected_lang = current_lang
    
    for idx, lang in enumerate(languages):
        with cols[idx]:
            is_active = (lang["code"] == current_lang)
            button_style = "✨ " + lang["name"] if is_active else lang["name"]
            
            # Show a smaller, custom styled button
            if st.button(button_style, key=f"lang_{lang['code']}", use_container_width=True):
                selected_lang = lang["code"]
                
    return selected_lang

def render_typing_indicator():
    """
    Renders a glowing, animated three-dot typing indicator.
    """
    st.markdown(
        '<div class="assistant-bubble">'
        '<div style="display: flex; align-items: center; gap: 8px;">'
        '<span style="color: #38BDF8; font-weight: 500; font-size: 0.9rem;">CampusSaathi AI is typing</span>'
        '<div style="display: flex; gap: 3px; align-items: center; margin-top: 2px;">'
        '<span class="typing-dot"></span>'
        '<span class="typing-dot"></span>'
        '<span class="typing-dot"></span>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

def render_custom_footer():
    """
    Renders a premium enterprise-grade footer for deployment.
    """
    st.markdown(
        '<div class="footer-text">'
        'CampusSaathi AI • Multilingual Academic LMS Integration Platform<br>'
        'Designed & Secured for College Deployments • All Rights Reserved'
        '</div>',
        unsafe_allow_html=True
    )
