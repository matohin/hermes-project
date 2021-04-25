import logging
import argparse
import shlex
import os

import azure.functions as func

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from shared.environment_helper import verify_key_vault_parameters, KEVAULT_ENV_VARS
from shared.service_bus_helper import send_to_telegram_output


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Telegram update recived via webhook, parsing reuest body")

    body = req.get_json()

    logging.info(body)

    event_router(body)

    return func.HttpResponse()


def id_checker(chat_id: int) -> None:

    verify_key_vault_parameters(KEVAULT_ENV_VARS)

    if os.getenv("CHAT_ID") == chat_id:
        return True

    else:
        return False


def event_router(message_body: dict) -> None:

    message_text = message_body["message"]["text"]

    logging.info(f"Incoming message text: {message_text}")

    parser = argparse.ArgumentParser(prefix_chars="/")
    group = parser.add_mutually_exclusive_group()
    split_message_text = shlex.split(message_text)
    group.add_argument("/echo", action="store_const", const=echo, dest="command")
    group.add_argument(
        "/graph_auth", action="store_const", const=not_implemented, dest="command"
    )
    group.add_argument(
        "/chat_auth", action="store_const", const=chat_auth, dest="command"
    )

    args, text = parser.parse_known_args(split_message_text)

    execution_allowed = id_checker(message_body["message"]["chat"]["id"])

    if args.command == chat_auth:
        execution_allowed = True

    if not execution_allowed:
        send_to_telegram_output(
            "This chat is not authorized to send commands. \nPlease authenticate with /chat_auth chat_key command"
        )
    elif not args.command:
        send_to_telegram_output("Input doesn't conatan a valid command")
    else:
        args.command(text)


def not_implemented(additionalInput: list) -> None:

    logging.warning(f"Command is not implemented")
    send_to_telegram_output(
        "This command is not implemented yet",
    )


def chat_auth(additionalInput: list) -> None:

    logging.warning(f"Starting chat athentication")


def echo(extra_aruments: list) -> None:

    msg = " ".join(list1)

    send_service_bus_message(msg, "sbq-telegram-otput")
