from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler

BRAWLER_PICK, SHOWDOWN_OR_GEMGRAB, SHOWDOWN, BUSH, POWERCUBE, GEMGRAB = range(6)


class AdventureHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('startgame', cls.startgame)],
            states={
                BRAWLER_PICK: [MessageHandler(filters.Regex('^(Bo|Fang)$'), cls.brawler_pick)],
                SHOWDOWN_OR_GEMGRAB: [MessageHandler(filters.Regex('^(Showdown|Gemgrab)$'),
                                                       cls.showdown_or_gemgrab)],
                SHOWDOWN: [MessageHandler(filters.Regex('^(Bush|Powercube)$'), cls.showdown)],
                GEMGRAB: [MessageHandler(filters.Regex('^(do not take heme|run with gems at the enemy)$'), cls.gemgrab)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Bo'), KeyboardButton('Fang')],
            [KeyboardButton('/exit'), KeyboardButton('/startgame')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            f'Привіт {update.effective_user.first_name}! Якого персонажа ти вибереш?',
            reply_markup=reply_markup)

        return BRAWLER_PICK

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Ви вийшли з розмови.')

        return ConversationHandler.END

    @staticmethod
    async def brawler_pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Showdown'), KeyboardButton('Gemgrab')],
            [KeyboardButton('/exit'), KeyboardButton('/startgame')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            f'Який режим вибирете?',
            reply_markup=reply_markup)

        brawler_pick = update.message.text
        context.user_data['brawler_pick'] = brawler_pick

        return SHOWDOWN_OR_GEMGRAB

    @staticmethod
    async def showdown_or_gemgrab(update: Update, context: ContextTypes.DEFAULT_TYPE):

        showdown_or_gemgrab = update.message.text
        context.user_data['showdown_or_gemgrab'] = showdown_or_gemgrab

        if update.message.text == 'Showdown':
            keyboard = [
                [KeyboardButton('Bush'), KeyboardButton('Powercube')],
                [KeyboardButton('/exit'), KeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(text=f"Вітаю {update.effective_user.first_name}!"
                                                 f" Ви вибрали {context.user_data['showdown_or_gemgrab']}!"
                                                 f" І йдете туда за {context.user_data['brawler_pick']}",
                                                 reply_markup=reply_markup)

            showdown_or_gemgrab = update.message.text
            context.user_data['showdown_or_gemgrab'] = showdown_or_gemgrab

            return SHOWDOWN

        else:
            keyboard = [
                [KeyboardButton('do not take heme'), KeyboardButton('run with gems at the enemy')],
                [KeyboardButton('/exit'), KeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(text=f"Вітаю ти почав ігру!"
                                                 f" Ти вибрав {context.user_data['showdown_or_gemgrab']}!"
                                                 f" І ідеш туда за {context.user_data['brawler_pick']}",
                                                 reply_markup=reply_markup)

            showdown_or_gemgrab = update.message.text
            context.user_data['showdown_or_gemgrab'] = showdown_or_gemgrab

            return GEMGRAB

    @staticmethod
    async def showdown(update: Update, context: ContextTypes.DEFAULT_TYPE):

        if update.message.text == 'Bush':
            keyboard = [
                [KeyboardButton('/exit'), KeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'Ех блін {update.effective_user.first_name}!:( Ви вирішили просидіти у кущах всю ігру.'
                f' Під кінець ігри у вас не було КубівСили і вас вбили.',
                reply_markup=reply_markup)

            return ConversationHandler.END

        else:
            keyboard = [
                [KeyboardButton('/exit'), KeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'Це погано. Ви вирішили получити КубикиСили но вас вбила Amber яка була у сусідніх кущах',
                reply_markup=reply_markup)

            return ConversationHandler.END

    @staticmethod
    async def gemgrab(update: Update, context: ContextTypes.DEFAULT_TYPE):

        if update.message.text == 'do not take heme':
            keyboard = [
                [KeyboardButton('/exit'), KeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f' Ви вирішили самі забрати собі геми!'
                f' і лишитися на базі : {context.user_data["brawler_pick"]} ваша  команда перемогла!',
                reply_markup=reply_markup)

            return ConversationHandler.END

        else:
            keyboard = [
                [KeyboardButton('/exit'), KeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'ви вирішили побігти з гемами на базу противника,'
                f' противники відібрали кристали і забрали всі кристали у синьої команди. Ви програли',
                reply_markup=reply_markup)

            return ConversationHandler.END




