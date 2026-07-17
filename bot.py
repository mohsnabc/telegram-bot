import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 ربات فعال شد")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot is running...")

app.run_polling()
