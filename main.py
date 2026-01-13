import os
import uvicorn
import tempfile
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from ears import process_audio
from brain import ask_ayodeji, digest_pdf

# Constants
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()
ptb_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("How far! I be Ayodeji, your Course Rep. I dey hear English, Pidgin, Yoruba, Igbo, and Hausa. Send VN, PDF, or just ask question.")

async def privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oga, I dey keep your secret safe. I no dey share your number with anybody. Read our full policy here: https://your-website.com/privacy")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # RAG Response
    response = ask_ayodeji(user_text)
    await update.message.reply_text(response)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    file_id = voice.file_id
    new_file = await context.bot.get_file(file_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
        tmp_path = tmp.name
    await new_file.download_to_drive(tmp_path)
    
    try:
        text = process_audio(tmp_path)
        response = ask_ayodeji(text)
        await update.message.reply_text(f"🎤 {text}\n\n🤖 {response}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    mime_type = doc.mime_type
    
    if "pdf" in mime_type:
        file_id = doc.file_id
        new_file = await context.bot.get_file(file_id)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp_path = tmp.name
        
        await new_file.download_to_drive(tmp_path)
        
        try:
            response = digest_pdf(tmp_path)
            await update.message.reply_text(response)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    else:
        await update.message.reply_text("Abeg send only PDF. I no dey read this one.")

# Add Handlers
ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(CommandHandler("privacy", privacy))
ptb_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
ptb_app.add_handler(MessageHandler(filters.VOICE, handle_voice))
ptb_app.add_handler(MessageHandler(filters.Document.PDF, handle_document))


# --- FastAPI Routes ---

@app.on_event("startup")
async def startup_check():
    required_vars = ["TELEGRAM_BOT_TOKEN", "GEMINI_API_KEY", "GROQ_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"CRITICAL: Missing environment variables: {', '.join(missing)}")
    else:
        print("Ayodeji is ready!")
        print(f"Token present: {bool(TOKEN)}")
        print(f"Webhook URL: {WEBHOOK_URL}")

    await ptb_app.initialize()
    await ptb_app.start()
    
    if WEBHOOK_URL and TOKEN:
        webhook_endpoint = f"{WEBHOOK_URL}/webhook"
        print(f"Attempting to set webhook to: {webhook_endpoint}")
        try:
            await ptb_app.bot.set_webhook(webhook_endpoint)
            print("Webhook set successfully!")
        except Exception as e:
            print(f"Failed to set webhook: {e}")

@app.on_event("shutdown")
async def shutdown():
    await ptb_app.stop()
    await ptb_app.shutdown()

@app.get("/")
def home():
    return {"message": "Ayodeji is online on Telegram!"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Handle incoming Telegram updates
    """
    try:
        data = await request.json()
        print(f"Received Webhook Data: {data}") # DEBUG LOG
        update = Update.de_json(data, ptb_app.bot)
        await ptb_app.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        print(f"Error handling update: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
