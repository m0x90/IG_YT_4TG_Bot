import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send me an Instagram or YouTube link!')

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    download_api = f"https://api.savefrom.net/api/convert?url={url}"
    response = requests.get(download_api)
    data = response.json()

    if 'url' in data:
        video_link = data['url']
        await update.message.reply_video(video_link, caption=f"Downloaded from {url}")
    else:
        await update.message.reply_text("Failed to download. Try another link.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

app.run_polling()
