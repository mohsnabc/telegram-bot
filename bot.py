import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "لینک اینستاگرام یا یوتیوب را بفرست."
    )

async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "instagram.com" in text or "youtube.com" in text or "youtu.be" in text:
        await update.message.reply_text("⏳ در حال پردازش...")

        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "audio.%(ext)s",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)
                filename = filename.rsplit(".", 1)[0] + ".mp3"

            await update.message.reply_audio(
                audio=open(filename, "rb"),
                title=info.get("title", "Audio")
            )

        except Exception as e:
            await update.message.reply_text(
                "❌ خطا در دریافت آهنگ:\n" + str(e)
            )

def run_bot():
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_link)
    )

    bot.run_polling(stop_signals=None)

threading.Thread(target=run_bot).start()

app.run(host="0.0.0.0", port=10000)
