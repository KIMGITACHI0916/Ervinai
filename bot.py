import os
import logging
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils.config import BOT_TOKEN, MAX_FILE_MB
from utils.logger import setup_logging
from pipeline import handle_pipeline

setup_logging()
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Private AI Mod Bot running. Send a file or use /code <instructions>")

async def handle_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only accept documents
    document = update.message.document
    if not document:
        await update.message.reply_text("Please send a document (file).")
        return

    file_size_mb = (document.file_size or 0) / (1024*1024)
    if file_size_mb > MAX_FILE_MB:
        await update.message.reply_text(f"File too large: {file_size_mb:.2f} MB (limit {MAX_FILE_MB} MB)")
        return

    await update.message.reply_text(f"Downloading: {document.file_name} ({file_size_mb:.2f} MB)...")

    try:
        file_obj = await context.bot.get_file(document.file_id)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_path = tmp.name
            await file_obj.download_to_drive(custom_path=temp_path)

        # Orchestrate pipeline: returns path to processed file
        processed_path = await handle_pipeline(temp_path, filename=document.file_name, user_instructions=update.message.caption)

        if processed_path and os.path.exists(processed_path):
            await update.message.reply_document(document=open(processed_path, "rb"), filename=os.path.basename(processed_path))
        else:
            await update.message.reply_text("Processing completed but no output file was produced.")

    except Exception as e:
        logger.exception("Error handling document")
        await update.message.reply_text(f"Error: {e}")

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_request = " ".join(context.args).strip()
    if not user_request:
        await update.message.reply_text("Usage: /code <instructions>")
        return
    await update.message.reply_text("Processing code request...")
    try:
        processed = await handle_pipeline(None, filename=None, user_instructions=user_request, mode='code')
        # If the pipeline returns text, send as code block; else if file path, send file
        if isinstance(processed, str) and os.path.exists(processed):
            await update.message.reply_document(document=open(processed, 'rb'), filename=os.path.basename(processed))
        else:
            # send as text
            text = processed or "(no response)"
            # Telegram markdown escaping is handled in pipeline
            await update.message.reply_text(f"```\n{text}\n```", parse_mode="MarkdownV2")
    except Exception as e:
        logger.exception("Error in /code")
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("code", code_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_doc))
    logging.getLogger("httpx").setLevel(logging.WARNING)
    app.run_polling()

if __name__ == '__main__':
    main()
