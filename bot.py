from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from movies_db import FILE_DATABASE  # <-- Import here

from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.environ['BOT_TOKEN'] if 'BOT_TOKEN' in os.environ else None


from movies_db import FILE_DATABASE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_code = context.args[0] if context.args else None
    if movie_code and movie_code in FILE_DATABASE:
        for file_info in FILE_DATABASE[movie_code]:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_info["file_id"],
                caption=f"{movie_code} ({file_info['resolution']})"
            )
    else:
        await update.message.reply_text("Invalid request.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
