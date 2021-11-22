import math
from telegram_bot_pagination import InlineKeyboardPaginator
from bot import dispatcher, LOGGER
from bot.messages import *
from bot.helper.bot_commands import BotCommands
from bot.search import ConversationHandler

PER_PAGE = 10


def show_results(start_page, items, context, update):
    responses_list = []
    context.chat_data['items'] = items
    page_count = math.ceil(len(items) / PER_PAGE)
    max_pages_len = (PER_PAGE * (1 + start_page))
    end_page = len(items) if len(items) < max_pages_len  else max_pages_len

    for s in range(start_page, end_page):
        if items[s]["title"]:
            responses_list.append("Q: {} \n {} \n".format(
                items[s]["title"], items[s]["link"]))
    responses = "".join(responses_list)
    paginator = InlineKeyboardPaginator(
        page_count,
        current_page=1,
        data_pattern='page#{page}'
    )
    sendMarkupWithPagination(responses, paginator.markup, context.bot, update)


def characters_page_callback(update, context):
    items = context.chat_data['items']
    query = update.callback_query
    query.answer()
    chosen_page = (int(query.data.split('#')[1]) - 1)
    start_page = chosen_page * PER_PAGE
    pages_len = (chosen_page + 1) * PER_PAGE
    end_page = pages_len if pages_len < len(items) else len(items)
    page_count = math.ceil(len(items) / PER_PAGE)

    responses_list = []
    for s in range(start_page, end_page):
        if items[s] and items[s]["title"]:
            responses_list.append("Q: {} \n {}.\n".format(
                items[s]["title"], items[s]["link"]))
    responses = "".join(responses_list)

    paginator = InlineKeyboardPaginator(
        page_count,
        current_page=(chosen_page+1),
        data_pattern='page#{page}'
    )
    query.edit_message_text(
        text=responses,
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
