import os
import string
from secrets import choice
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def test_service_bus_access():

    connection_string = os.getenv("AzureWebJobsAzureSBConnection")
    queue_name = "sbq-integration-test"

    random_source = string.ascii_letters + string.digits + string.punctuation
    expected = "".join(choice(random_source) for i in range(20))

    with ServiceBusClient.from_connection_string(connection_string) as client:

        with client.get_queue_sender(queue_name) as sender:

            single_message = ServiceBusMessage(expected)
            sender.send_messages(single_message)

        with client.get_queue_receiver(queue_name, max_wait_time=30) as receiver:

            msg = receiver.next()
            actual = str(msg)

            assert actual == expected

            receiver.complete_message(msg)
