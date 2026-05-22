import os
import tempfile
import logging
import streamlit as st
from faster_whisper import WhisperModel

# ---------------------------------------------------
# Logging Configuration
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------
# Load Faster Whisper Model
# ---------------------------------------------------
@st.cache_resource(show_spinner="Loading Speech Recognition Engine...")
def load_whisper_model():
    """
    Loads and caches the Faster Whisper model.

    tiny model:
    - lightweight
    - CPU friendly
    - fast inference
    """

    try:
        logger.info("Loading Faster Whisper tiny model...")

        model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

        logger.info("Faster Whisper model loaded successfully.")

        return model

    except Exception as e:
        logger.error(f"Error loading Faster Whisper model: {e}")
        return None


# ---------------------------------------------------
# Audio Transcription Function
# ---------------------------------------------------
def transcribe_audio_file(audio_bytes: bytes) -> str:
    """
    Converts recorded audio bytes into text.

    Steps:
    1. Save temporary audio file
    2. Transcribe using Faster Whisper
    3. Return extracted text
    """

    if not audio_bytes:
        return ""

    temp_file_path = None

    try:
        # ---------------------------------------------
        # Save audio temporarily
        # ---------------------------------------------
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_audio:

            temp_audio.write(audio_bytes)
            temp_file_path = temp_audio.name

        logger.info(f"Temporary audio file saved: {temp_file_path}")

        # ---------------------------------------------
        # Load Whisper Model
        # ---------------------------------------------
        whisper_model = load_whisper_model()

        if whisper_model is None:
            logger.error("Whisper model failed to load.")
            return ""

        logger.info("Starting transcription process...")

        # ---------------------------------------------
        # Transcription
        # ---------------------------------------------
        segments, info = whisper_model.transcribe(
            temp_file_path,
            beam_size=5,
            multilingual=True
        )
        logger.info(f"Detected language: {info.language}")

        # ---------------------------------------------
        # Combine text segments
        # ---------------------------------------------
        text = " ".join(
            [segment.text for segment in segments]
        ).strip()

        logger.info(f"Transcription Result: {text}")

        return text

    except Exception as e:
        logger.error(f"Transcription Error: {e}")
        return ""

    finally:
        # ---------------------------------------------
        # Cleanup temporary file
        # ---------------------------------------------
        if temp_file_path and os.path.exists(temp_file_path):

            try:
                os.remove(temp_file_path)
                logger.info("Temporary audio file deleted.")

            except Exception as cleanup_error:
                logger.warning(
                    f"Failed to delete temp file: {cleanup_error}"
                )


# ---------------------------------------------------
# Microphone Input Widget
# ---------------------------------------------------
def render_microphone_input():
    """
    Renders microphone recorder widget.

    Returns:
        audio bytes if recorded
        otherwise None
    """

    try:
        from streamlit_mic_recorder import mic_recorder

        st.markdown(
            """
            <div style="margin-top:10px;margin-bottom:10px;">
            """,
            unsafe_allow_html=True
        )

        audio_record = mic_recorder(
            start_prompt="🎙️ Click to Record Voice Query",
            stop_prompt="🛑 Stop Recording",
            just_once=True,
            use_container_width=True,
            key="mic_widget"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        if audio_record:

            logger.info("Audio recorded successfully.")

            return audio_record.get("bytes")

        return None

    except ImportError:

        st.warning(
            "streamlit-mic-recorder package is missing."
        )

        return None

    except Exception as e:

        logger.error(f"Microphone Error: {e}")

        st.error("Microphone initialization failed.")

        return None