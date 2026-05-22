# 🎓 CampusSaathi AI — Multilingual Campus Assistant

CampusSaathi AI is an enterprise-grade, high-fidelity multilingual AI-powered campus assistant integrated with a modern LMS/ERP look. It is built using Python, Streamlit, Google Gemini API, and Whisper AI to assist Students, Teachers/Staff, and Parents with day-to-day college workflows, administrative procedures, fee structures, and scholarship guidelines.

---

## 🌟 Key Features

*   **Zero-Authentication Frictionless Access**: Directly routes users into role-based workflows for immediate queries.
*   **Role-Based Dashboards**: Specially crafted panels with dynamic categories for **Students**, **Teachers/Staff**, and **Parents**.
*   **Structured FAQ Database**: Local RAG knowledge base storing official college regulations, required documentation, timings, processing speeds, and desk locations.
*   **Google Gemini Generative AI (RAG Mode)**: Uses advanced prompt crafting and contextual RAG search to answer custom user questions beyond standard FAQs.
*   **Intelligent Multilingual Support**: Seamless input-to-output language alignment supporting **English**, **Hindi (हिन्दी)**, **Gujarati (ગુજરાતી)**, **Tamil (தமிழ்)**, **Telugu (తెలుగు)**, and **Marathi (मराठी)**.
*   **Speech-to-Text Voice Inputs**: Hands-free voice querying powered by OpenAI's Whisper AI (tiny model for fast local operation) with high-efficiency API fallbacks.
*   **Industrial Dark Design System**: Elite cybernetic visual aesthetic featuring glowing neon cyan highlights, custom micro-animations, glassmorphic card designs, and dynamic typing loaders.

---

## 📂 Project Directory Structure

```
CampusSaathiAI/
│
├── app.py                # Main Streamlit router, session state controller & layouts
├── chatbot.py            # RAG context compiler, Gemini API pipeline, & fuzzy search fallbacks
├── language_detector.py  # Langdetect ISO codes classifier and system prompt generators
├── speech_to_text.py      # Audio recorder renderer, Whisper AI compiler & fallback routines
├── knowledge_base.json   # Structured JSON database holding academic & logistical procedures
├── ui_components.py      # CSS loader, asset managers, custom chips, logo, and animations
├── requirements.txt      # Stable library dependencies
├── .env.example          # Template for credential keys
└── assets/
    ├── styles.css        # Central stylesheet holding layout styling, glow details, and scrollbars
    ├── logo.png          # High-fidelity custom glowing branding logo
    └── avatar.png        # Futuristic AI chatbot avatar
```

---

## 🛠️ Setup & Installation Guide

### Prerequisites
*   Python 3.9, 3.10, or 3.11 installed.
*   An active Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/)).

### Step 1: Clone or Copy the Repository
Navigate to the directory of the project in your terminal:
```bash
cd CampusSaathiAI
```

### Step 2: Install Required Dependencies
Install the highly stable required python packages using pip:
```bash
pip install -r requirements.txt
```
> [!NOTE]
> During installation, `openai-whisper` might require `ffmpeg` to be installed on your system if you are doing heavy local processing. If not available, CampusSaathi has a graceful auto-transcription bypass to keep voice functions running.

### Step 3: Configure Environment Variables
1. Duplicate the `.env.example` file and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_gemini_key_here...
   ```

---

## 🚀 Running the Application Locally

Start the Streamlit development server by running:
```bash
streamlit run app.py
```

The application will automatically build and open in your default browser at:
**`http://localhost:8501`**

---

## 🎯 Verification and Usage Flow

1.  **Welcome Landing**: Bypasses login. Simply click your designated identity (Student, Teacher/Staff, Parent) and select your target language from the modern glassmorphism selection grid.
2.  **Explore FAQs**: Browse categorized accordion menus. Click on any predefined query (e.g., "Leave application process") to instantly display official documents, processing times, timings, and map coordinates.
3.  **Consult AI Bot**: If you have a unique question, type it directly into the chat input or click the **🎙️ Record Voice Query** button to talk.
4.  **Multilingual Test**: Type or speak a question in Hindi (e.g., *"स्कॉलरशिप के लिए कैसे अप्लाई करें?"*). CampusSaathi AI automatically detects Hindi, feeds it to Gemini with local knowledge, and outputs the structured response fully in Hindi!

---

## 🌐 Production Deployment Steps

### Method A: Streamlit Community Cloud (Recommended)
1.  Push the project directory to a private or public GitHub repository.
2.  Log into [Streamlit Share](https://share.streamlit.io/).
3.  Click **New App** and select your repository, branch, and `app.py` path.
4.  In the **Advanced Settings** menu, paste your Gemini credentials into the **Secrets** section:
    ```toml
    GEMINI_API_KEY = "your_actual_api_key"
    ```
5.  Click **Deploy**! Your app is live with a secure public URL.

### Method B: Docker Deployment (Self-Hosted)
Create a `Dockerfile` in the root directory:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
Build and run the container:
```bash
docker build -t campussaathi-ai .
docker run -p 8501:8501 --env-file .env campussaathi-ai
```

---

## 🔮 Future Enhancements
*   **Vector Search Database**: Upgrade static JSON lookup to FAISS / ChromaDB semantic matching for faster and more flexible query matching.
*   **LMS Integration APIs**: Direct REST API connectors to sync student marks, elective swaps, and attendance from Canvas or Moodle.
*   **Live Hostel Room Availability**: Dynamic database tables displaying real-time vacant parent guest rooms and direct booking checkout portals.
