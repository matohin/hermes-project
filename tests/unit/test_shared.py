from secrets import choice
import string

from shared.key_vault_helper import get_key_vault_secret
from shared.environment_helper import verify_key_vault_parameters
from shared.service_bus_helper import send_to_telegram_output


def test_get_key_vault_secret(mocker):

    random_source = string.ascii_letters + string.digits + string.punctuation

    secret_name = "test-" + "".join(choice(string.digits) for i in range(8))
    key_vault_uri = "".join(choice(string.digits) for i in range(10))
    secret_value = "".join(choice(random_source) for i in range(20))

    mocker.patch("os.getenv", return_value=key_vault_uri)

    credentials = "".join(choice(random_source) for i in range(20))
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


def test_verify_key_vault_parameters(mocker):

    random_source = string.ascii_letters + string.digits + string.punctuation

    key1 = "".join(choice(string.ascii_letters) for i in range(20))
    key2 = "".join(choice(string.ascii_letters) for i in range(20))

    value1 = "".join(choice(random_source) for i in range(20))
    value2 = "".join(choice(random_source) for i in range(20))

    parameters = {key1: value1, key2: value2}

    mock_env = mocker.patch("shared.environment_helper.environ")
    mock_env.get.return_value = None

    mocker.patch(
        "shared.environment_helper.get_key_vault_secret", side_effect=[value1, value2]
    )

    verify_key_vault_parameters(parameters)

    mock_env.get.assert_any_call(key1)
    mock_env.get.assert_called_with(key2)

    mock_env.__setitem__.assert_any_call(key1, value1)
    mock_env.__setitem__.assert_called_with(key2, value2)


def test_send_service_bus_message(mocker):

    random_source = string.ascii_letters + string.digits + string.punctuation
    connection_string = "".join(choice(random_source) for i in range(20))
    msg = "".join(choice(random_source) for i in range(20))
    queue_name = "".join(choice(random_source) for i in range(20))

    mocker.patch("shared.service_bus_helper.os.getenv", return_value=connection_string)

    service_bus_client_mock = mocker.patch(
        "shared.service_bus_helper.ServiceBusClient.from_connection_string"
    )

    service_bus_message_object = "".join(choice(random_source) for i in range(20))
    service_bus_message_mock = mocker.patch(
        "shared.service_bus_helper.ServiceBusMessage",
        return_value=service_bus_message_object,
    )

    send_service_bus_message(msg, queue_name)

    service_bus_client_mock.assert_called_with(connection_string)

    client_mock = service_bus_client_mock.return_value.__enter__.return_value

    client_mock.get_queue_sender.assert_called_with(queue_name)

    sender_mock = client_mock.get_queue_sender.return_value.__enter__.return_value

    service_bus_message_mock.assert_called_with(msg)

    sender_mock.send_messages.assert_called_with(service_bus_message_object)
