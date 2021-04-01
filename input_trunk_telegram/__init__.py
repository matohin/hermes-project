import logging

import argparse
import shlex


import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Telegram update recived via webhook, parsing reuest body")

    body = req.get_json()

    logging.info(body)

    event_router(body)

    return func.HttpResponse()


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
    args, text = parser.parse_known_args(split_message_text)

    args.command(text)


def not_implemented(additionalInput: list) -> None:

    logging.error(f"Command {additionalInput} is notimplemented")


def echo(additionalInput: list) -> None:

    logging.error(f"Command {additionalInput} is notimplemented")
