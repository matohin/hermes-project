import logging
import azure.functions as func
import json
import requests
from os import environ

from shared.environment_helper import verify_key_vault_parameters, KEVAULT_ENV_VARS


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

    verify_key_vault_parameters(KEVAULT_ENV_VARS)

    logging.info("Sending message to Telegram")
    msg_text = msg.get_body().decode("utf-8")
    logging.info(msg_text)

    chat_id = environ.get("CHAT_ID")

    method = "sendMessage"
    data = {"chat_id": chat_id, "text": msg_text}

    call_telegram_api(method, data)
