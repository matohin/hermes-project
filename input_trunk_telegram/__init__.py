import logging
import argparse
import shlex
import os

import azure.functions as func

from azure.servicebus import ServiceBusClient, ServiceBusMessage


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

    if not args.command:
        echo(f"Input doesn't conatan a valid command".split())
    else:
        args.command(text)


def not_implemented(additionalInput: list) -> None:

    logging.warning(f"Command {additionalInput} is not implemented")


def echo(extra_parameters: list) -> None:

    connection_string = os.getenv("AzureWebJobsAzureSBConnection")
    queue_name = "sbq-telegram-otput"

    message = " ".join(extra_parameters)

    with ServiceBusClient.from_connection_string(connection_string) as client:

        with client.get_queue_sender(queue_name) as sender:

            service_bus_message = ServiceBusMessage(message)
            sender.send_messages(service_bus_message)
