import logging
import azure.functions as func
import json
import requests
from os import environ

from shared.key_vault_helper import get_key_vault_secret


def verify_key_vault_parameters(parameters: dict) -> None:

    for parameter, secret_name in parameters.items():

        if not environ.get(parameter):

            environ[parameter] = get_key_vault_secret(secret_name)


def call_telegram_api(method: str, data: dict) -> requests.Response:

    logging.info(f"Calling Telegram API method {method}")

    telegram_api_token = environ.get("TELEGRAM_API_TOKEN")
    url = f"https://api.telegram.org/bot{telegram_api_token}/{method}"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=data)

    logging.info("Recived API response")
    logging.info(response)

    response.raise_for_status()


def main(msg: func.ServiceBusMessage) -> None:

    parameters = {"TELEGRAM_API_TOKEN": "telegramBotToken", "CHAT_ID": "ChatId"}

    verify_key_vault_parameters(parameters)

    logging.info("Sending message to Telegram")
    msg_text = msg.get_body().decode("utf-8")
    logging.info(msg_text)

    chat_id = environ.get("CHAT_ID")

    method = "sendMessage"
    data = {"chat_id": chat_id, "text": msg_text}

    call_telegram_api(method, data)
