from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os


def send_service_bus_message(message: str, queue_name: str, to: int = None) -> None:

    connection_string = os.getenv("AzureWebJobsAzureSBConnection")

    with ServiceBusClient.from_connection_string(connection_string) as client:

        with client.get_queue_sender(queue_name) as sender:

            service_bus_message = ServiceBusMessage(message)
            service_bus_message.to = to
            sender.send_messages(service_bus_message)


def send_to_telegram_output(msg: str, to: int) -> None:

    send_service_bus_message(msg, "sbq-telegram-otput", to)
