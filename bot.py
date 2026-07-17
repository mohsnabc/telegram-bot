import os
import threading
import requests
import yt_dlp

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


TOKEN = os.getenv("TOKEN")
AUDD_TOKEN = os.getenv("AUDD_TOKEN")

app = Flask(__name__)


@app.route("/")
def home():
    return "OK"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "لینک اینستاگرام یا یوتیوب را بفرست تا آهنگ را پیدا کنم 🎵"
    )


async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if "instagram.com" in text or "youtube.com" in text or "youtu.be" in text:

        processing_msg = await update.message.reply_text(
            "⏳ در حال بررسی آهنگ..."
        )

        try:

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "song.%(ext)s",
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


            with open(filename, "rb") as audio:

                response = requests.post(
                    "https://api.audd.io/",
                    data={
                        "api_token": AUDD_TOKEN,
                        "return": "spotify"
                    },
                    files={
                        "file": audio
                    }
                )


            result = response.json()


            # حذف پیام پردازش
            try:
                await processing_msg.delete()
            except:
                pass


            if result.get("result"):

                song = result["result"]

                title = song.get("title", "نامشخص")
                artist = song.get("artist", "نامشخص")


                await update.message.reply_text(
                    f"🎵 آهنگ پیدا شد:\n\n"
                    f"نام: {title}\n"
                    f"خواننده: {artist}"
                )

            else:

                await update.message.reply_text(
                    "❌ آهنگ تشخیص داده نشد"
                )


            await update.message.reply_audio(
                audio=open(filename, "rb"),
                title=info.get("title", "Audio")
            )


        except Exception as e:

            try:
                await processing_msg.delete()
            except:
                pass

            await update.message.reply_text(
                "❌ خطا:\n" + str(e)
            )


def run_bot():

    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(
        CommandHandler("start", start)
    )

    bot.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            check_link
        )
    )

    bot.run_polling(stop_signals=None)


threading.Thread(
    target=run_bot
).start()


app.run(
    host="0.0.0.0",
    port=10000
)
