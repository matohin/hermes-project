import logging
import azure.functions as func
import urllib3
import json
import requests

TELEGRAM_API_TOKEN = "845789670:AAEf2dmacBxiVSLtmpLIMpks2J_o-_XznQA"


def main(msg: func.ServiceBusMessage):

    logging.info(msg.get_body().decode("utf-8"))

    method = "sendMessage"
    data = {"chat_id": "55033450", "text": "ffdfd"}

    response = call_telegram_api(method, data)


def set_callback_webhook(url):

    method = "setWebhook"
    data = {"url": url}

    response = call_telegram_api(method, data)


def call_telegram_api(method, data):

    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/{method}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)

    return response
