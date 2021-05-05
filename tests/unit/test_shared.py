from secrets import choice
import string

from shared.key_vault_helper import get_key_vault_secret
from shared.key_vault_helper import set_key_vault_secret
from shared.environment_helper import verify_key_vault_parameters
from shared.service_bus_helper import send_to_telegram_output
from shared.service_bus_helper import send_service_bus_message


def test_get_key_vault_secret(mocker, generate_int, generate_string):

    secret_name = generate_int()
    key_vault_uri = generate_string()
    secret_value = generate_string()

    mocker.patch("os.getenv", return_value=key_vault_uri)

    credentials = generate_string()
    mocker.patch(
        "shared.key_vault_helper.DefaultAzureCredential", return_value=credentials
    )

    secret = mocker.MagicMock()
    secret.value = secret_value
    key_vault_client = mocker.MagicMock()
    key_vault_client.get_secret = mocker.MagicMock(return_value=secret)
    secret_client = mocker.patch(
        "shared.key_vault_helper.SecretClient", return_value=key_vault_client
    )

    actual = get_key_vault_secret(secret_name)

    secret_client.assert_called_with(vault_url=key_vault_uri, credential=credentials)
    key_vault_client.get_secret.assert_called_with(secret_name)

    assert actual == secret_value


def test_set_key_vault_secret(mocker, generate_string):

    secret_name = generate_string(16, True)
    secret_value = generate_string()

    mock_client = mocker.Mock()
    mocker.patch("shared.key_vault_helper.os.getenv")
    mocker.patch("shared.key_vault_helper.DefaultAzureCredential")
    mocker.patch("shared.key_vault_helper.SecretClient", return_value=mock_client)

    set_key_vault_secret(secret_name, secret_value)

    mock_client.set_secret.assert_called_once_with(secret_name, secret_value)


def test_verify_key_vault_parameters(mocker, generate_string):

    key1 = generate_string(20, True)
    key2 = generate_string(20, True)
    key3 = generate_string(20, True)

    value1 = generate_string(20)
    value2 = generate_string(20)
    value3 = generate_string(20)

    parameters = {key1: value1, key2: value2, key3: value3}

    mock_env = mocker.patch("shared.environment_helper.environ")
    mock_env.get.return_value = None

    mocker.patch(
        "shared.environment_helper.get_key_vault_secret",
        side_effect=[value1, value2, None],
    )

    verify_key_vault_parameters(parameters)

    mock_env.get.assert_any_call(key1)
    mock_env.get.assert_any_call(key2)
    mock_env.get.assert_called_with(key3)

    mock_env.__setitem__.assert_any_call(key1, value1)
    mock_env.__setitem__.assert_any_call(key2, value2)
    mock_env.__setitem__.assert_called_with(key3, "NOT DEFINED")


def test_send_service_bus_message(mocker, generate_string, generate_int):

    connection_string = generate_string()
    msg = generate_string()
    queue_name = generate_string()
    to = generate_int()

    mocker.patch("shared.service_bus_helper.os.getenv", return_value=connection_string)

    service_bus_client_mock = mocker.patch(
        "shared.service_bus_helper.ServiceBusClient.from_connection_string"
    )

    service_bus_message_object = mocker.Mock()

    service_bus_message_mock = mocker.patch(
        "shared.service_bus_helper.ServiceBusMessage",
        return_value=service_bus_message_object,
    )

    send_service_bus_message(msg, queue_name, to)

    service_bus_client_mock.assert_called_with(connection_string)

    client_mock = service_bus_client_mock.return_value.__enter__.return_value

    client_mock.get_queue_sender.assert_called_with(queue_name)

    sender_mock = client_mock.get_queue_sender.return_value.__enter__.return_value

    service_bus_message_mock.assert_called_with(msg)

    assert service_bus_message_object.to == to

    sender_mock.send_messages.assert_called_with(service_bus_message_object)


def test_send_to_telegram_output(mocker, generate_string):

    msg = generate_string()
    to = generate_string()

    mock_send_service_bus_message = mocker.patch(
        "shared.service_bus_helper.send_service_bus_message"
    )

    send_to_telegram_output(msg, to)
    mock_send_service_bus_message.assert_called_once_with(msg, "sbq-telegram-otput", to)
