import logging
import azure.functions as func
import json
import requests

from shared.key_vault_helper import get_key_vault_secret

if not TELEGRAM_API_TOKEN:

    TELEGRAM_API_TOKEN = get_key_vault_secret("telegramBotToken")

CHAT_ID = 55033450


def call_telegram_api(method, data):

    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/{method}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)

    return response


def main(msg: func.ServiceBusMessage) -> None:

    msg_text = msg.get_body().decode("utf-8")
    logging.info(msg_text)

    method = "sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg_text}

    response = call_telegram_api(method, data)

    logging.info(response)


def set_callback_webhook(url: str) -> None:

    logging.info("Starting `setWebhook` operation on Telagram API")

    method = "setWebhook"
    data = {"url": url}

    response = call_telegram_api(method, data)

    logging.info(response)
