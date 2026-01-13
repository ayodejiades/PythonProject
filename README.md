# Ayodeji - Multimodal AI Telegram Bot

Ayodeji is a "Digital Course Rep" bot for Nigerian students, built with FastAPI, LangChain, and Google Gemini. He speaks Clean Pidgin, English, Yoruba, Igbo, and Hausa.

## Features
- **Platform**: Telegram (via `python-telegram-bot`).
- **Multilingual**: Auto-detects and speaks 5 languages.
- **Features**: Answers text questions, transcribes voice notes, and creates knowledge from PDFs.

## Tech Stack
- **Framework**: FastAPI + Python Telegram Bot
- **Database**: PostgreSQL (SQLAlchemy)
- **Vector Store**: ChromaDB
- **LLM**: Google Gemini Pro
- **Audio**: Groq API (Whisper-v3)

## Setup

### Environment Variables
- `TELEGRAM_BOT_TOKEN`: From @BotFather
- `WEBHOOK_URL`: HTTPS URL of your Render app (e.g. `https://ayodeji.onrender.com`)
- `GEMINI_API_KEY`: Google AI Studio Key
- `GROQ_API_KEY`: Groq Cloud API Key
- `DATABASE_URL`: PostgreSQL Connection String

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   uvicorn main:app --reload
   ```
3. Use ngrok to tunnel: `ngrok http 8000`
4. Set Webhook:
   ```bash
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<YOUR_NGROK_URL>/webhook"
   ```

### Deployment (Render)
1. Deploy to Render as a Web Service (Docker).
2. Set Environment Variables.
3. The app attempts to set the webhook on startup if `WEBHOOK_URL` is present.
