import logging
import os
import time
from functools import partial

import requests
import telegram
from dotenv import load_dotenv

from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from parser_commands import create_parser
from dialogflow import detect_intent_text
from telegram_log import TelegramLogsHandler

logger = logging.getLogger('Logger')


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def send_message(update: Update, context: CallbackContext, project):
    chat_id = update.message['chat']['id']
    project_id = project
    answer_message = detect_intent_text(project_id, chat_id,
                                        update.message.text, 'ru')
    update.message.reply_text(answer_message)


def start_bot(tg_token, project_id):
    logger.info('Telegram bot TECH ADVICER advicer is started')
    while True:
        try:
            updater = Updater(token=tg_token)
            dispatcher = updater.dispatcher
            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(
                MessageHandler(Filters.text & ~Filters.command,
                               partial(send_message, project=project_id)
                               )
            )
            updater.start_polling()
            updater.idle()
        except requests.exceptions.ConnectionError:
            time.sleep(60)
        except Exception:
            logger.exception('Telegram bot TECH ADVICER is failed')


if __name__ == '__main__':
    load_dotenv()

    tg_log_token = os.getenv('TELEGRAM_LOG_TOKEN')
    tg_log_chat_id = os.getenv('TELEGRAM_LOG_CHAT_ID')
    tg_bot = telegram.Bot(token=tg_log_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_log_chat_id))

    tg_token = os.getenv('TELEGRAM_TOKEN')
    project_id = os.getenv('GOOGLE_PROJECK_ID')

    parser = create_parser(project_id)
    args = parser.parse_args()
    project = args.project

    start_bot(tg_token, project)
