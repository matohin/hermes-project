import string
from random import choice


import azure.functions as func
from output_trunk_telegram import main, call_telegram_api
from shared.environment_helper import verify_key_vault_parameters


def test_call_telegram_api(mocker):

    random_source = string.ascii_letters + string.digits + string.punctuation

    method = "".join(choice(random_source) for i in range(20))
    data = "".join(choice(random_source) for i in range(20))
    token = "".join(choice(random_source) for i in range(20))

    response = mocker.Mock()

    mocker.patch("output_trunk_telegram.environ.get", side_effect=[token, method])
    mock_requests = mocker.patch("output_trunk_telegram.requests")
    mock_requests.post.return_value = response

    call_telegram_api(method, data)

    mock_requests.post.assert_called_once_with(
        f"https://api.telegram.org/bot{token}/{method}",
        headers={"Content-Type": "application/json"},
        json=data,
    )

    response.raise_for_status.assert_called_once_with()


def test_output_trunk_telegram_main(mocker):

    random_source = string.ascii_letters + string.digits + string.punctuation
    chat_id = "".join(choice(random_source) for i in range(20))
    msg_text = "".join(choice(random_source) for i in range(20))

    mock_call_telegram_api = mocker.patch(
        "output_trunk_telegram.call_telegram_api", return_value=chat_id
    )

    incoming_service_bus_msg = func.servicebus.ServiceBusMessage(
        body=bytes(msg_text, "utf-8"),
        message_id="id123",
        user_properties={"user1": "description1"},
        to=chat_id,
    )

    main(incoming_service_bus_msg)

    mock_call_telegram_api.assert_called_once_with(
        "sendMessage", {"chat_id": chat_id, "text": msg_text}
    )
