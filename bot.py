import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

async def start(update, context):
    await update.message.reply_text("سلام 👋 ربات فعال شد")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling(stop_signals=None)

threading.Thread(target=run_bot).start()

app.run(host="0.0.0.0", port=10000)
