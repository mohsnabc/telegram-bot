from telegram import Update
import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 لینک اینستاگرام را بفرست")

async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "instagram.com" in text:
        await update.message.reply_text("✅ لینک اینستاگرام دریافت شد")

def run_bot():
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_link))

    bot.run_polling(stop_signals=None)

threading.Thread(target=run_bot).start()

app.run(host="0.0.0.0", port=10000)
