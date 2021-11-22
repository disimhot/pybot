import math
from telegram_bot_pagination import InlineKeyboardPaginator
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, message
from bot.helper.bot_commands import BotCommands
from bot import dispatcher, LOGGER
from bot.helper.section_types import SectionTypes
from bot.messages import *
from bot.handle_result import *
import requests

START_PAGE = 0


def search(update, context):
    custom_keyboard = [[sect[0]] for sect in SectionTypes.list()]
    search_string = f"""
Выберите раздел
    """
    # print('search \n')
    reply_markup = ReplyKeyboardMarkup(
        custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(update.message.chat_id,
                             text=search_string,
                             reply_markup=reply_markup)
    return URL


def url_handler(update, context):
    url = [sect[1] for sect in SectionTypes.list() if sect[0] ==
           update.message.text]
    context.chat_data['url'] = url[0]
    request_string = """
Введи, пожалуйста, свой вопрос
    """
    context.bot.send_message(update.message.chat_id,
                             text=request_string,
                             reply_markup=ReplyKeyboardRemove())
    return QUERY


def query_handler(update, context):
    try:
        message = f'''
Минуту... я ищу ответы. Ты всегда можешь остановить беседу с помощью команды /{BotCommands.CancelCommand}      
        '''
        update.message.reply_text(message)
        url = context.chat_data['url']
        uri = f"{url}&intitle={update.message.text}"
        # print(f'URI {uri}')
        response = requests.get(uri)
        data = response.json()
        items = data['items']
        if len(items) > 0:
            show_results(START_PAGE, items, context, update)
            return RESULT
        else:
            no_found_string = f'''
Ничего не нашлось по твоему запросу.
Пожалуйста, попробуй использовать /{BotCommands.SearchCommand} снова
            '''
            sendMessage(no_found_string,
                        context.bot, update)
            return ConversationHandler.END
    except Exception as e:
        LOGGER.warning('Update "%s" caused error "%s"' % (update, e))


def cancel(update, context):
    cancel_string = f'''
Спасибо за классные вопросы!
Задавай их при помощи команды /{BotCommands.SearchCommand}
            '''
    sendMessage(cancel_string,
                context.bot, update)
    return ConversationHandler.END


URL, QUERY, RESULT = range(3)

search_handler = ConversationHandler(
    entry_points=[
        CommandHandler(BotCommands.SearchCommand, search),
    ],
    states={
        URL: [MessageHandler(Filters.regex('(Section|раздел)'), url_handler)],
        QUERY: [MessageHandler(Filters.text & ~Filters.command, query_handler)],
        RESULT: [
            CallbackQueryHandler(characters_page_callback, pattern='^page#'),
            MessageHandler(Filters.text & ~Filters.command, query_handler),
            CommandHandler(BotCommands.SearchCommand, search),
        ],
    },
    fallbacks=[CommandHandler(BotCommands.CancelCommand, cancel)],
    run_async=True
)

dispatcher.add_handler(search_handler)
