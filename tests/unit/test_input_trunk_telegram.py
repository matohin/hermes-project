import azure.functions as func
from input_trunk_telegram import (
    main,
    event_router,
    echo,
    not_implemented,
    id_checker,
    chat_auth,
)

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
    "telegram_input, expected_function, expected_parameter, chat_id_check_result",
    [
        ("/echo some text", "echo", ["some", "text"], True),
        ("/graph_auth other stuff", "not_implemented", ["other", "stuff"], True),
        ("/graph_auth", "not_implemented", [], True),
        (
            "invalid commnd",
            "send_to_telegram_output",
            "Input doesn't conatan a valid command",
            True,
        ),
        (
            "/graph_auth",
            "send_to_telegram_output",
            "This chat is not authorized to send commands. \nPlease authenticate with /chat_auth chat_key command",
            False,
        ),
        ("/chat_auth secret", "chat_auth", ["secret", "123456"], False),
    ],
)
def test_event_router(
    telegram_input, expected_function, expected_parameter, chat_id_check_result, mocker
):

    chat_id = "123456"

    function_mock = mocker.patch(f"input_trunk_telegram.{expected_function}")
    mock_id_checker = mocker.patch(
        "input_trunk_telegram.id_checker", return_value=chat_id_check_result
    )

    body = {"message": {"text": telegram_input, "chat": {"id": chat_id}}}

    event_router(body)

    mock_id_checker.assert_called_once_with(chat_id)

    function_mock.assert_called_with(expected_parameter)


@pytest.mark.parametrize(
    "chat_id_env, chat_id_input, expected",
    [
        (123456, 123456, True),
        (123456, "123456", True),
        ("123456", 123456, True),
        ("123456", "123456", True),
        (123456, 654321, False),
    ],
)
def test_id_checker_false(chat_id_env, chat_id_input, expected, mocker):

    mocker.patch("input_trunk_telegram.verify_key_vault_parameters")
    mocker.patch("input_trunk_telegram.os.getenv", return_value=chat_id_env)

    actual = id_checker(chat_id_input)

    assert actual == expected


def test_chat_auth_granted(mocker):

    random_source = string.ascii_letters + string.digits + string.punctuation

    chat_id = "".join(choice(string.digits) for i in range(6))
    chat_auth_key = "".join(choice(random_source) for i in range(20))

    mocker.patch("input_trunk_telegram.verify_key_vault_parameters")
    mocker.patch("input_trunk_telegram.os.getenv", return_value=chat_auth_key)
    mock_set_key_vault_secret = mocker.patch(
        "input_trunk_telegram.set_key_vault_secret"
    )

    chat_auth([chat_auth_key, chat_id])
    mock_set_key_vault_secret.assert_called_once_with("chatAuthKey", chat_id)


def test_chat_auth_regected(mocker):

    random_source = string.ascii_letters + string.digits + string.punctuation

    chat_id = "".join(choice(string.digits) for i in range(6))
    chat_auth_key_expected = "".join(choice(random_source) for i in range(20))
    chat_auth_key_provided = "".join(choice(random_source) for i in range(20))

    mocker.patch("input_trunk_telegram.verify_key_vault_parameters")
    mocker.patch("input_trunk_telegram.os.getenv", return_value=chat_auth_key_expected)
    mock_set_key_vault_secret = mocker.patch(
        "input_trunk_telegram.set_key_vault_secret"
    )

    chat_auth([chat_auth_key_provided, chat_id])
    mock_set_key_vault_secret.assert_not_called()