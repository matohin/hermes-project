import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from secrets import choice
import string

if not os.getenv("KEY_VAULT_URI"):

    os.environ["KEY_VAULT_URI"] = "https://kv-hermes-proj.vault.azure.net/"


def test_keyvault_access():

    key_vault_uri = os.environ["KEY_VAULT_URI"]

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    random_source = string.ascii_letters + string.digits + string.punctuation
    test_secret_name = "test-" + "".join(choice(string.digits) for i in range(8))
    test_secret_value = "".join(choice(random_source) for i in range(20))

    client.set_secret(test_secret_name, test_secret_value)
    actual = client.get_secret(test_secret_name)

    assert actual.value == test_secret_value

    poller = client.begin_delete_secret(test_secret_name)
    deleted_secret = poller.result()

    assert deleted_secret.id == actual.id
