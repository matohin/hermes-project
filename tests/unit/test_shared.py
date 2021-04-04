from secrets import choice
import string

from shared.key_vault_helper import get_key_vault_secret


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
