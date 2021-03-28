import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def test_service_bus_access():

    connection_string = os.getenv("AzureWebJobsAzureSBConnection")
    queue_name = "sbq-telegram-otput"

    with ServiceBusClient.from_connection_string(connection_string) as client:

        with client.get_queue_sender(queue_name):

            expected = "Single message"

            message = ServiceBusMessage(expected)
            queue_sender.send(message)

        with client.get_queue_receiver(queue_name) as receiver:

            for msg in receiver:

                actual = str(msg)

                assert actual == expected

                msg.complete()