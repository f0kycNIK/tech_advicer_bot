import logging
import os
import random
import time

import requests
import telegram
import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from parser_commands import create_parser
from dialogflow import detect_intent_text
from telegram_log import TelegramLogsHandler

logger = logging.getLogger('Logger')


def get_answer(message, project_id, user_id):
    answer_message, intent_flg = detect_intent_text(project_id, user_id,
                                                    message, 'ru')
    if not intent_flg:
        return answer_message


def send_message(vk_api, event, message):
    if event.from_user:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )
    elif event.from_chat:
        vk_api.messages.send(
            chat_id=event.chat_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


def start_bot(longpoll, vk_api, project_id):
    logger.info('VK bot TECH ADVICER is started')
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    message = event.message
                    answer_message = get_answer(message, project_id,
                                                event.user_id)
                    if answer_message:
                        send_message(vk_api, event, answer_message)
        except requests.exceptions.ConnectionError:
            time.sleep(60)
        except Exception:
            logger.exception('VK bot TECH ADVICER is failed')


if __name__ == "__main__":
    load_dotenv()

    tg_log_token = os.getenv('TELEGRAM_LOG_TOKEN')
    tg_log_chat_id = os.getenv('TELEGRAM_LOG_CHAT_ID')
    tg_bot = telegram.Bot(token=tg_log_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_log_chat_id))

    parser = create_parser()
    args = parser.parse_args()
    project = args.project

    vk_token = os.getenv('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    start_bot(longpoll, vk_api, project)
