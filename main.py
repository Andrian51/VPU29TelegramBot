import os
import logging

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton('/start'), KeyboardButton('/hello')],
        [KeyboardButton('/author'), KeyboardButton('/Bye')],
        [KeyboardButton('Share location', request_location=True)]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        f'Привіт {update.effective_user.first_name}',
        reply_markup=reply_markup)


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Мене робили Diduh Andrian і Gado Bogdan")


async def Bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="прощавай")


async def location(update: Update, context: ContextTypes.DEFEAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.latitude

    await update.message.reply_text(f'lat = {lat}, lon = {lon}')


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("author", author))
app.add_handler(CommandHandler("bye", Bye))

location_hendler = (MessageHandler(filters.LOCATION, location))
app.add_handler(location_hendler)


app.run_polling()
