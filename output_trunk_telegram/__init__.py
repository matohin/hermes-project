import logging
import azure.functions as func
import json
import requests

from shared.key_vault_helper import get_key_vault_secret


def verify_global_parameters():

    if "TELEGRAM_API_TOKEN" not in globals():

        global TELEGRAM_API_TOKEN
        TELEGRAM_API_TOKEN = get_key_vault_secret("telegramBotToken")

    if "CHAT_ID" not in globals():

        global CHAT_ID
        CHAT_ID = 55033450


def call_telegram_api(method, data):

    verify_global_parameters()

    logging.info(f"Calling Telegram API method {method}, request body below")
    logging.info(data)

    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/{method}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)

    logging.info("Recived API response")
    logging.info(response)

    return response


def main(msg: func.ServiceBusMessage) -> None:

    logging.info("Sending message to Telegram")
    msg_text = msg.get_body().decode("utf-8")
    logging.info(msg_text)

    method = "sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg_text}

    call_telegram_api(method, data)


def set_callback_webhook(url: str) -> None:

    logging.info("Starting `setWebhook` operation on Telagram API")

    method = "setWebhook"
    data = {"url": url}

    response = call_telegram_api(method, data)

    logging.info(response)
