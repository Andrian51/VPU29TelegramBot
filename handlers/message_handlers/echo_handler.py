from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

from handlers.base_handler import BaseHandler


class EchoHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(MessageHandler(filters.Regex(r"^echo\s+(.*)$"), cls.callback))

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(update.message.text)