import json
import os
import logging
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Import our custom language detector
from language_detector import detect_input_language, get_multilingual_system_prompt, get_language_name

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure the Gemini API if key is available
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("Google Gemini API successfully configured.")
    except Exception as e:
        logger.error(f"Failed to configure Google Gemini API: {e}")
else:
    logger.warning("GEMINI_API_KEY not found in environment. Running in Local Intelligent Fallback Mode.")

@st.cache_data
def load_knowledge_base():
    """
    Loads and caches the structured JSON knowledge base.
    """
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load knowledge_base.json: {e}")
        return {}

def format_structured_response(faq_item: dict) -> str:
    """
    Clean professional formatted FAQ response.
    """

    documents = "\n".join(
        [f"• {doc}" for doc in faq_item.get("required_documents", ["None"])]
    )

    procedure_steps = faq_item.get("procedure", "").split("\n")

    procedure = "\n".join(
        [f"{step}" for step in procedure_steps if step.strip()]
    )

    response = f"""
📋 Actionable Procedure Overview

{faq_item.get('answer', '')}

📍 Location / Office:
{faq_item.get('location', 'N/A')}

⏰ Timings:
{faq_item.get('timings', 'N/A')}

✍️ Approval Authority:
{faq_item.get('approval_authority', 'N/A')}

⏳ Processing Time:
{faq_item.get('processing_time', 'N/A')}

⚠️ Deadlines:
{faq_item.get('deadlines', 'N/A')}

📎 Required Documents:
{documents}

🛠️ Procedure:
{procedure}
"""

    if faq_item.get("additional_instructions"):
        response += f"""

💡 Additional Instructions:
{faq_item.get('additional_instructions')}
"""

    response = response.replace("\n", "<br>")

    return response

def get_fuzzy_local_match(role: str, query: str) -> dict:
    """
    A lightweight search engine that queries the local JSON knowledge base to find
    the closest matching question using simple keyword overlapping (Fuzzy matching fallback).
    """
    kb = load_knowledge_base()
    role_data = kb.get(role, {})
    
    best_match = None
    max_overlap = 0
    query_words = set(query.lower().split())
    
    for category, faqs in role_data.items():
        for faq in faqs:
            q_words = set(faq["question"].lower().replace("?", "").replace(",", "").split())
            overlap = len(query_words.intersection(q_words))
            
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = faq
                
    # Return best match if we got a substantial keyword match (at least 2 overlapping words)
    if max_overlap >= 2:
        return best_match
    return None

def generate_ai_response(role: str, query: str, active_language: str = None) -> str:
    """
    Executes the main RAG chatbot flow:
    1. Detects input language.
    2. Gathers the active role's FAQ knowledge base context.
    3. Queries Google Gemini API (incorporating strict output format instructions).
    4. Handles API absence gracefully using local fuzzy intelligence search.
    """
    # Detect query language if not explicitly locked
    detected_lang = detect_input_language(query)
    lang_name = get_language_name(detected_lang)
    
    # 1. Compile localized knowledge base context
    kb = load_knowledge_base()
    role_kb = kb.get(role, {})
    
    kb_context_str = ""
    for category, faqs in role_kb.items():
        kb_context_str += f"\n--- Category: {category} ---\n"
        for faq in faqs:
            kb_context_str += (
                f"Question: {faq['question']}\n"
                f"Answer: {faq['answer']}\n"
                f"Required Documents: {', '.join(faq['required_documents'])}\n"
                f"Location: {faq['location']}\n"
                f"Timings: {faq['timings']}\n"
                f"Procedure:\n{faq['procedure']}\n"
                f"Approval Authority: {faq['approval_authority']}\n"
                f"Deadlines: {faq['deadlines']}\n"
                f"Processing Time: {faq['processing_time']}\n"
                f"Additional Instructions: {faq.get('additional_instructions', 'None')}\n\n"
            )

    # 2. Call Google Gemini if key exists
    if GEMINI_API_KEY:
        try:
            logger.info("Connecting to Google Gemini API (gemini-1.5-flash)...")
            
            # System prompt for structured RAG output
            system_prompt = (
                f"You are CampusSaathi AI, the elite, extremely polite, and helpful multilingual university assistant.\n"
                f"You are talking to a {role}.\n\n"
                f"Here is the OFFICIAL UNIVERSITY KNOWLEDGE BASE CONTEXT you must strictly rely on:\n"
                f"{kb_context_str}\n\n"
                f"TASK INSTRUCTIONS:\n"
                f"IMPORTANT: Never generate HTML, CSS, <div>, <table>, <p>, inline styles, markdown tables, or code blocks. "
                f"Return only clean plain formatted text using headings, bullet points, and numbered lists.\n\n"
                f"IMPORTANT: Never return raw HTML tags like <div>, <table>, <p>, <ul>, or inline CSS. "
                f"Return clean formatted plain text only using headings, bullet points, and numbered lists.\n\n"
                f"1. You must answer the user's question clearly, professionally, and in full detail.\n"
                f"2. Your answer MUST be structured EXACTLY in this format:\n\n"
                f"Required Documents:\n"
                f"* [Document Name]\n"
                f"* [Document Name]\n\n"
                f"Location/Room:\n"
                f"* [Office details and Room Number]\n\n"
                f"Timings:\n"
                f"* [Office Working Hours]\n\n"
                f"Procedure:\n"
                f"1. [Step 1]\n"
                f"2. [Step 2]\n\n"
                f"Approval Authority:\n"
                f"* [Designation / Authority name]\n\n"
                f"Deadlines:\n"
                f"* [Deadlines or 'No deadline' if none]\n\n"
                f"Processing Time:\n"
                f"* [Time it takes to process]\n\n"
                f"Additional Instructions:\n"
                f"* [Any precautions, links or guidance]\n\n"
                f"3. If the query is NOT present in the official knowledge base context, answer the query based on standard academic general knowledge, but maintain the EXACT structured layout above. Use logical mock locations and documents suitable for an Indian/Global college, but add a brief note that this is standard guidance.\n"
                f"{get_multilingual_system_prompt(detected_lang)}"
                 )
            
            # Setup the model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash"
            )
            # Request response
            response = model.generate_content(
                contents=[
                    {"role": "user", "parts": [f"System Instruction: {system_prompt}\n\nUser Question: {query}"]}
                ]
            )
            
            clean_response = response.text

            # Remove accidental HTML generation
            clean_response = clean_response.replace("<", "&lt;")
            clean_response = clean_response.replace(">", "&gt;")

            # Convert line breaks nicely
            clean_response = clean_response.replace("\n", "<br>")

            return f"""
            <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(56,189,248,0.15);
            border-radius: 12px;
            padding: 20px;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            color: #E2E8F0;
            line-height: 1.7;
            font-size: 0.95rem;
            ">
            {clean_response}
            </div>
            """                
        except Exception as e:
            logger.error(f"Gemini API execution failed: {e}. Falling back to local fuzzy match.")
            # Fall back to fuzzy logic matching
    
    # 3. Local Intelligent Fallback (if API is absent or fails)
    local_match = get_fuzzy_local_match(role, query)
    if local_match:
        logger.info(f"Successful local fuzzy match for query: '{query}'")
        intro_text = (
            f"[⚠️ Running in offline Mode - Displaying nearest match from Campus database]\n\n"
            if not GEMINI_API_KEY else "[⚠️ API Error - Fetching local backup records]\n\n"
        )
        return format_structured_response(local_match)
        
    # Standard dynamic error message if no match found locally either
    fallback_response = (
        f"ℹ️ **CampusSaathi Offline Support**\n\n"
        f"I detected your query in **{lang_name}**, but the AI Server (Google Gemini) is currently offline, "
        f"and I could not find a direct matching FAQ in the local knowledge base.\n\n"
        f"**To activate full generative AI responses:**\n"
        f"Please create a `.env` file in the project folder and paste your `GEMINI_API_KEY=your_key_here` as described in the README."
    )
    return fallback_response
