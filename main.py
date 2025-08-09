import os
import logging
import tempfile
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# ======== CONFIG ========
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")  # Set in Railway ENV
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set in Railway ENV
client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)

# ======== COMMANDS ========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! Send me a file or message and I'll process it with my AI brain.")

# ======== FILE HANDLING ========
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.audio or update.message.video
    if not file:
        await update.message.reply_text("❌ Unsupported file type.")
        return

    file_id = file.file_id
    file_obj = await context.bot.get_file(file_id)

    # Download large files safely to temp
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file_path = tmp.name
        await file_obj.download_to_drive(file_path)

    await update.message.reply_text(f"✅ File received: {file.file_name}\nSize: {file.file_size / 1024 / 1024:.2f} MB")
    
    # Optional: AI processing for text/code files
    if file.mime_type.startswith("text") or file.file_name.endswith((".py", ".txt", ".md")):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(2000)  # limit preview
        ai_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI file assistant."},
                {"role": "user", "content": f"Here is the start of a file:\n{content}\nSummarize it."}
            ]
        )
        await update.message.reply_text(f"📄 AI Summary:\n{ai_resp.choices[0].message.content}")

# ======== TEXT (AI BRAIN) ========
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    ai_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an advanced AI bot with high accuracy."},
            {"role": "user", "content": user_text}
        ]
    )
    await update.message.reply_text(ai_resp.choices[0].message.content)

# ======== MAIN APP ========
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL | filters.Audio.ALL | filters.Video.ALL, handle_file))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    app.run_polling()
