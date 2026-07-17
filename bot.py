import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 لینک اینستاگرام را بفرست")

async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import yt_dlp

    text = update.message.text

    if "instagram.com" in text:
        await update.message.reply_text("⏳ در حال دانلود ویدیو...")

        try:
            ydl_opts = {
                "format": "best",
                "outtmpl": "video.%(ext)s"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)

            await update.message.reply_video(
                video=open(filename, "rb"),
                caption="✅ دانلود شد"
            )

        except Exception as e:
            await update.message.reply_text(
                "❌ دانلود نشد\n" + str(e)
            )

def run_bot():
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_link))

    bot.run_polling(stop_signals=None)

threading.Thread(target=run_bot).start()

app.run(host="0.0.0.0", port=10000)
