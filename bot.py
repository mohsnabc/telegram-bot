import os
import threading
import requests
import yt_dlp

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("TOKEN")
AUDD_TOKEN = os.getenv("AUDD_TOKEN")

app = Flask(__name__)


@app.route("/")
def home():
    return "OK"


def main_menu():

    keyboard = [
        [
            InlineKeyboardButton("🎬 اینستاگرام", callback_data="instagram"),
            InlineKeyboardButton("▶️ یوتیوب", callback_data="youtube")
        ],
        [
            InlineKeyboardButton("🎵 MP3", callback_data="mp3"),
            InlineKeyboardButton("🎥 ویدیو", callback_data="video")
        ],
        [
            InlineKeyboardButton("ℹ️ راهنما", callback_data="help")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def back_button():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 برگشت", callback_data="back")
        ]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "سلام محسن 👋\n\n"
        "به ربات دانلودر خوش آمدی.\n"
        "گزینه مورد نظر را انتخاب کن:",
        reply_markup=main_menu()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "back":

        await query.message.edit_text(
            "منوی اصلی:",
            reply_markup=main_menu()
        )


    elif query.data == "instagram":

        await query.message.edit_text(
            "🎬 لینک اینستاگرام را بفرست.",
            reply_markup=back_button()
        )


    elif query.data == "youtube":

        await query.message.edit_text(
            "▶️ لینک یوتیوب را بفرست.",
            reply_markup=back_button()
        )


    elif query.data == "mp3":

        await query.message.edit_text(
            "🎵 لینک را بفرست تا MP3 دریافت کنی.",
            reply_markup=back_button()
        )


    elif query.data == "video":

        await query.message.edit_text(
            "🎥 لینک را بفرست تا ویدیو دریافت کنی.",
            reply_markup=back_button()
        )


    elif query.data == "help":

        await query.message.edit_text(
            "راهنما:\n\n"
            "لینک اینستا یا یوتیوب را ارسال کن.\n"
            "ربات فایل را آماده می‌کند.",
            reply_markup=back_button()
        )


async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if "instagram.com" not in text and "youtube.com" not in text and "youtu.be" not in text:
        return


    processing = await update.message.reply_text(
        "⏳ در حال پردازش..."
    )


    try:

        ydl_opts = {
            "format": "best",
            "outtmpl": "file.%(ext)s"
        }


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                text,
                download=True
            )

            filename = ydl.prepare_filename(info)



        try:
            await processing.delete()
        except:
            pass



        await update.message.reply_video(
            video=open(filename, "rb"),
            caption="✅ آماده شد"
        )


    except Exception as e:

        try:
            await processing.delete()
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
        CallbackQueryHandler(button_handler)
    )


    bot.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            check_link
        )
    )


    bot.run_polling(
        stop_signals=None
    )



threading.Thread(
    target=run_bot
).start()


app.run(
    host="0.0.0.0",
    port=10000
)
