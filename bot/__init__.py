import config
import logging
import os
import telegram.ext as tg

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
updater = tg.Updater(token=config.token,use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
