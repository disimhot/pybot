import os
import telebot
from flask import Flask, request

TOKEN = '2056386592:AAEiRiW355BIOejoKAkvJKQN4hTK4aVlHMk'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)


# Если строка на входе непустая, то бот повторит ее
@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
	bot.send_message(message.chat.id, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url='https://ees-bot.herokuapp.com/' + TOKEN)  #
	return "!", 200


if __name__ == "__main__":
	server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))