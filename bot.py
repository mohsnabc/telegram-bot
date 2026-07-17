import os
import threading
import instaloader
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "لینک اینستاگرام را بفرست تا بررسی کنم."
    )

async def instagram_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "instagram.com" in url:
        await update.message.reply_text("⏳ در حال پردازش لینک اینستاگرام...")

        # فعلاً تست اتصال است
        await update.message.reply_text(
            "✅ لینک اینستاگرام دریافت شد.\n"
            "مرحله دانلود را بعداً کامل می‌کنیم."
        )

async def run_bot():
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, instagram_download)
    )

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()

def start_bot():
    import asyncio
    asyncio.run(run_bot())

threading.Thread(target=start_bot).start()

app.run(host="0.0.0.0", port=10000)
