import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 ربات فعال شد")

async def main():
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()

asyncio.run(main())

app.run(host="0.0.0.0", port=10000)
