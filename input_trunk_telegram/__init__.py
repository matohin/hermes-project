import logging
import argparse
import shlex
import os

import azure.functions as func

from shared.environment_helper import verify_key_vault_parameters, KEVAULT_ENV_VARS
from shared.service_bus_helper import send_to_telegram_output
from shared.key_vault_helper import set_key_vault_secret


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Telegram update recived via webhook, parsing reuest body")

    body = req.get_json()

    logging.info(body)

    event_router(body)

    return func.HttpResponse()


def id_checker(chat_id: int) -> bool:

    verify_key_vault_parameters(KEVAULT_ENV_VARS)
    authorized_chat_id = os.getenv("CHAT_ID")

    if int(authorized_chat_id) == int(chat_id):
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

    chat_id = message_body["message"]["chat"]["id"]

    execution_allowed = id_checker(chat_id)

    if args.command == chat_auth:
        execution_allowed = True
        text.append(chat_id)

    if not execution_allowed:
        send_to_telegram_output(
            "This chat is not authorized to send commands. \nPlease authenticate with /chat_auth chat_key command", chat_id
        )
    elif not args.command:
        send_to_telegram_output("Input doesn't conatan a valid command", chat_id)
    else:
        args.command(text)


def not_implemented(additional_input: list) -> None:

    logging.warning("Command is not implemented")

    to = os.getenv("CHAT_ID")

    send_to_telegram_output("This command is not implemented yet", to)


def chat_auth(additional_input: list) -> None:

    logging.warning(f"Starting chat athentication")

    verify_key_vault_parameters(KEVAULT_ENV_VARS)

    incoming_chat_id = additional_input[-1]

    if additional_input[0] == os.getenv("CHAT_AUTH_KEY"):

        set_key_vault_secret("chatAuthKey", incoming_chat_id)

        os.environ["CHAT_ID"] = incoming_chat_id

        send_to_telegram_output(
            "Authentication succesfull. Please, remove key from the chat.",
            incoming_chat_id,
        )

    else:

        send_to_telegram_output(
            "Key doesn't match. Please, try again.",
            incoming_chat_id,
        )


def echo(additional_input: list) -> None:

    logging.warning("Sending additional input as echo")

    msg = " ".join(additional_input)
    to = os.getenv("CHAT_ID")

    send_to_telegram_output(msg, to)
