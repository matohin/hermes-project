import azure.functions as func
from input_trunk_telegram import main, event_router, echo, not_implemented
import json
import pytest


def test_input_trunk_telegram(mocker):

    body = b'{"message": { "text": "test" } }'
    incoming_http_request = func.HttpRequest(method="POST", url="local", body=body)

    event_router_mock = mocker.patch("input_trunk_telegram.event_router")

    result = main(incoming_http_request)

    event_router_mock.assert_called_with(json.loads(body))


def test_event_router_echo(mocker):

    echo_mock = mocker.patch("input_trunk_telegram.echo")

    body = {"message": {"text": "/echo some text"}}

    event_router(body)

    echo_mock.assert_called_with(["some", "text"])


@pytest.mark.parametrize(
    "telegram_input,expected_function,expected_parameter",
    [
        ("/echo some text", "echo", ["some", "text"]),
        ("/graph_auth other stuff", "not_implemented", ["other", "stuff"]),
    ],
)
def test_event_router(telegram_input, expected_function, expected_parameter, mocker):

    echo_mock = mocker.patch("input_trunk_telegram.{}".format(expected_function))

    body = {"message": {"text": telegram_input}}

    event_router(body)

    echo_mock.assert_called_with(expected_parameter)
