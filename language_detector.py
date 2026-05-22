import logging
from langdetect import detect

# Set up simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported languages mapping
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'gu': 'Gujarati',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi'
}

# Default language to fall back on
DEFAULT_LANGUAGE = 'en'

def detect_input_language(text: str) -> str:
    """
    Detects the ISO-639 language code for a given text query.
    If detection fails or detects a language not explicitly supported, 
    falls back to English.
    """
    if not text or not text.strip():
        return DEFAULT_LANGUAGE
    
    try:
        # Perform language detection
        detected_iso = detect(text.strip())
        logger.info(f"Detected ISO code: {detected_iso} for text snippet.")
        
        # If detected code is in supported languages, return it
        if detected_iso in SUPPORTED_LANGUAGES:
            return detected_iso
        
        # Additional checks for similar language families or fallback
        return DEFAULT_LANGUAGE
    except Exception as e:
        logger.warning(f"Language detection failed: {e}. Defaulting to '{DEFAULT_LANGUAGE}'")
        return DEFAULT_LANGUAGE

def get_language_name(lang_code: str) -> str:
    """
    Returns the human-readable language name for a given ISO code.
    """
    return SUPPORTED_LANGUAGES.get(lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE])

def get_multilingual_system_prompt(lang_code: str) -> str:
    """
    Generates a prompt injection text instructing Gemini to respond in the selected language.
    """
    lang_name = get_language_name(lang_code)
    return (
        f"\n[CRITICAL DIRECTIVE]\n"
        f"You must compose your entire answer in the {lang_name} language. "
        f"Use native script for writing (e.g. Hindi script for Hindi, Gujarati script for Gujarati). "
        f"Do not mix languages except for core technical term names or office names if absolutely necessary. "
        f"Your response language must perfectly align with {lang_name}."
    )
