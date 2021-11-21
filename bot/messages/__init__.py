from telegram import InlineKeyboardMarkup
from telegram.message import Message
from telegram.update import Update
from bot import LOGGER


def sendMessage(text, bot, update):
    try:
        return bot.send_message(update.message.chat_id,
                                text=text, parse_mode='HTMl')
    except Exception as e:
        LOGGER.error(str(e))


def sendMarkup(markup, bot, update):
    try:
        return bot.send_message(update.message.chat_id,
                                text=markup, parse_mode='HTMl',
                                disable_web_page_preview=True)
    except Exception as e:
        LOGGER.error(str(e))


def sendMarkupWithPagination(text, markup, bot, update):
    try:
        return bot.send_message(
            update.message.chat_id,
            text=text,
            reply_markup=markup,
        )
    except Exception as e:
        LOGGER.error(str(e))
