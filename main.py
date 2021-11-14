import config
import os
from operator import attrgetter
import telebot
import json
from bs4 import BeautifulSoup
from flask import Flask, request
import requests

bot = telebot.TeleBot(config.token)
server = Flask(__name__)


@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
    # r = requests.get('https://stackoverflow.com/oauth?client_id=21284')
    print('message', message.text)
    l = f'https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={message.text}&site=sqa'
    print(l)
    response = requests.get(l)
    data = response.json()
    items = data['items']
    markup = f'<i>{items[:2]}</i>'
    print(markup)
    bot.send_message(message.chat.id, markup, parse_mode='html')


# bot.infinity_polling()
@server.route('/' + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ees-bot.herokuapp.com/' + config.token)  #
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
