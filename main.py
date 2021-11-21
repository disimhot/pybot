import config
import os
import telebot
import json
from bs4 import BeautifulSoup
from flask import Flask, request
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from bot.helper.bot_commands import BotCommands
from bot.messages import *
from bot.search import *
from bot import dispatcher, updater, LOGGER
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

server = Flask(__name__)


def start(update, context):
    start_string = f"""
Привет, {update.message.chat.first_name}! Я помогаю разработчикам и отвечаю на вопросы.
Я очень постараюсь найти для тебя всю информацию на StackOverflow.
Если нужна помощь, нажми /{BotCommands.HelpCommand}
Если хочешь задать вопрос, то прошу нажать /{BotCommands.SearchCommand}
    """
    sendMessage(start_string, context.bot, update)


def help(update, context):
    help_string = f'''
/{BotCommands.StartCommand}: Начать работу
/{BotCommands.HelpCommand}: Справка по командам бота
/{BotCommands.SearchCommand}: Искать вопрос на StackOverflow
/{BotCommands.StopCommand}: Остановить бота
/{BotCommands.CancelCommand}: Остановить беседу
'''
    sendMessage(help_string, context.bot, update)

def main():
    start_handler = CommandHandler(BotCommands.StartCommand, start)
    help_handler = CommandHandler(BotCommands.HelpCommand, help)
    stop_handler = CommandHandler(BotCommands.StopCommand, stop)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stop_handler)
    LOGGER.info('START bot')
    updater.start_polling()
    updater.idle()


def stop():
    updater.stop()


if __name__ == '__main__':
    main()
