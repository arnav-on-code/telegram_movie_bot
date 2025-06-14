# from flask import Flask, request, jsonify
# from telegram import Update
# import requests
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     ContextTypes,
#     TypeHandler,
# )
# from movies_db import FILE_DATABASE
# import os

# app = Flask(__name__)

# # Load environment variables
# BOT_TOKEN = os.environ.get('BOT_TOKEN')
# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN environment variable is not set.")

# # Build application
# application = Application.builder().token(BOT_TOKEN).build()

# # Register handlers
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     movie_code = update.message.text.split()[1] if len(update.message.text.split()) > 1 else None
#     if movie_code and movie_code in FILE_DATABASE:
#         for file_info in FILE_DATABASE[movie_code]:
#             await context.bot.send_document(
#                 chat_id=update.effective_chat.id,
#                 document=file_info["file_id"],
#                 caption=f"{movie_code} ({file_info['resolution']})"
#             )
#     else:
#         await update.message.reply_text("Invalid request.")

# application.add_handler(CommandHandler("start", start))

# # Process updates
# async def process_update(update: Update, _):
#     await application.process_update(update)

# application.add_handler(TypeHandler(Update, process_update))

# # Webhook endpoint
# @app.post('/webhook')
# async def webhook():
#     try:
#         print("Raw request data:", request.data)  # Debugging line
#         json_data = request.get_json()
#         print("Parsed JSON:", json_data)  # Debugging line
        
#         if not json_data:
#             return jsonify({"error": "No JSON data received"}), 400
            
#         update = Update.de_json(json_data, application.bot)
#         if not update:
#             return jsonify({"error": "Invalid update object"}), 400
            
#         await application.process_update(update)
#         return jsonify({"status": "ok"})
        
#     except Exception as e:
#         print("Error:", e)  # Debugging line
#         return jsonify({"error": str(e)}), 500

# def setwebhook():
#     TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
#     WEBHOOK_URL = "https://telegram-movie-bot-sigma.vercel.app/api/webhook"
#     s = requests.post(
#         f"{TELEGRAM_URL}/setWebhook",
#         json={"url": WEBHOOK_URL}
#     )
#     print("Webhook setup response:", s.status_code, s.text)  # Debugging line
#     return "Success" if s.status_code == 200 else "Fail"

# if __name__ == '__main__':
#     setwebhook()
#     app.run(port=8000)

from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, TypeHandler
import os
import asyncio
import sys
import requests

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from movies_db import FILE_DATABASE  # <-- Make sure the filename matches exactly!
app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set.")

# Build application
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

# Initialize the application at startup
async def initialize_app():
    await application.initialize()

# Run the initialization once when the app starts
asyncio.run(initialize_app())

@app.post('/webhook')
async def webhook():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No JSON data received"}), 400
        update = Update.de_json(json_data, application.bot)
        if not update:
            return jsonify({"error": "Invalid update object"}), 400
        await application.process_update(update)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def setwebhook():
    TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
    WEBHOOK_URL = "https://telegram-movie-bot-sigma.vercel.app/api/webhook"
    s = requests.post(
        f"{TELEGRAM_URL}/setWebhook",
        json={"url": WEBHOOK_URL}
    )
    print("Webhook setup response:", s.status_code, s.text)  # Debugging line
    return "Success" if s.status_code == 200 else "Fail"
setwebhook()
# if __name__ == '__main__':
#     setwebhook()

#     app.run(port=8000)
