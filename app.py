
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world"

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8414363077:AAFiflBPXEBqI08IlsHhfcvuhiHwrbaCZ2Q"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a video page URL, and I will extract video URLs for you (no downloading).")

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("Extracting video URLs. Please wait...")

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            urls = [f['url'] for f in formats if f.get('url')]
            if urls:
                response = "Found video URLs:\n" + "\n".join(urls[:10])  # limiting to first 10 URLs
            else:
                response = "No video URLs found."
    except Exception as e:
        response = f"Error occurred: {e}"

    await update.message.reply_text(response)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    print("Bot is polling...")
    app.run_polling()


if __name__ == '__main__':
    main()
