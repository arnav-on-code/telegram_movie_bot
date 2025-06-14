# api/webhook.py
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from movies_db import FILE_DATABASE  # or movies_db, depending on your filename


BOT_TOKEN = os.environ.get('BOT_TOKEN')
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_code = update.message.text.split()[1] if len(update.message.text.split()) > 1 else None
    if movie_code and movie_code in FILE_DATABASE:
        for file_info in FILE_DATABASE[movie_code]:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_info["file_id"],
                caption=f"{movie_code} ({file_info['resolution']})"
            )
    else:
        await update.message.reply_text("Invalid request.")

application.add_handler(CommandHandler("start", start))

async def main(request):
    await application.initialize()
    body = await request.json()
    update = Update.de_json(body, application.bot)
    await application.process_update(update)
    return {'statusCode': 200}
