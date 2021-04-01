import azure.functions as func
from input_trunk_telegram import main, event_router, echo, not_implemented
from azure.servicebus import ServiceBusClient, ServiceBusMessage

import json
import pytest
import string
from random import choice


def test_input_trunk_telegram(mocker):

    body = b'{"message": { "text": "test" } }'
    incoming_http_request = func.HttpRequest(method="POST", url="local", body=body)

    event_router_mock = mocker.patch("input_trunk_telegram.event_router")

    result = main(incoming_http_request)

    event_router_mock.assert_called_with(json.loads(body))

    assert type(result) is func.HttpResponse


@pytest.mark.parametrize(
    "telegram_input, expected_function, expected_parameter",
    [
        ("/echo some text", "echo", ["some", "text"]),
        ("/graph_auth other stuff", "not_implemented", ["other", "stuff"]),
        ("/graph_auth", "not_implemented", []),
        (
            "invalid commnd",
            "echo",
            ["Input", "doesn't", "conatan", "a", "valid", "command"],
        ),
    ],
)
def test_event_router(telegram_input, expected_function, expected_parameter, mocker):

    function_mock = mocker.patch(f"input_trunk_telegram.{expected_function}")

    body = {"message": {"text": telegram_input}}

    event_router(body)

    function_mock.assert_called_with(expected_parameter)


def test_echo(mocker):

    random_source = string.ascii_letters + string.digits + string.punctuation
    connection_string = "".join(choice(random_source) for i in range(20))

    getenv_mock = mocker.patch(
        "input_trunk_telegram.os.getenv", return_value=connection_string
    )

    service_bus_client_mock = mocker.patch(
        "input_trunk_telegram.ServiceBusClient.from_connection_string",
    )

    service_bus_message_object = "".join(choice(random_source) for i in range(20))
    service_bus_message_mock = mocker.patch(
        "input_trunk_telegram.ServiceBusMessage",
        return_value=service_bus_message_object,
    )

    echo(["a", "b"])

    service_bus_client_mock.assert_called_with(connection_string)

    client_mock = service_bus_client_mock.return_value.__enter__.return_value

    client_mock.get_queue_sender.assert_called_with("sbq-telegram-otput")

    sender_mock = client_mock.get_queue_sender.return_value.__enter__.return_value

    service_bus_message_mock.assert_called_with("a b")

    sender_mock.send_messages.assert_called_with(service_bus_message_object)
