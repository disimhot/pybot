import config
import os
import telebot
import json
from bs4 import BeautifulSoup
from flask import Flask, request
from telegram.ext import CommandHandler, MessageHandler, Filters
from bot.helper.bot_commands import BotCommands
from bot import dispatcher, updater, LOGGER
import requests

server = Flask(__name__)

# @bot.message_handler(func=lambda msg: msg.text is not None)
# def reply_to_message(message):
#     # r = requests.get('https://stackoverflow.com/oauth?client_id=21284')
#     print('message', message.text)
#     l = f'https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={message.text}&site=sqa'
#     print(l)
#     response = requests.get(l)
#     data = response.json()
#     items = data['items']
#     markup = f'<i>{items[:2]}</i>'
#     print(markup)
#     bot.send_message(message.chat.id, markup, parse_mode='html')


def start():
    pass


def bot_help(update, context):
    help_string = f'''
/{BotCommands.HelpCommand}: Справка по командам бота
/{BotCommands.SearchCommand}: Искать вопрос на StackOverflow
'''
    context.bot.sendMessage(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=help_string, parse_mode='HTMl')
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def main():
    start_handler = CommandHandler(BotCommands.StartCommand, start)
    help_handler = CommandHandler(BotCommands.HelpCommand, bot_help)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    LOGGER.info('START bot')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


# bot.infinity_polling()

# @server.route('/' + config.token, methods=['POST'])
# def getMessage():
#     bot.process_new_updates(
#         [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200


# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://ees-bot.herokuapp.com/' + config.token)  #
#     return "!", 200


# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
