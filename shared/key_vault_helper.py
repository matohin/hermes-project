import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def get_key_vault_secret(secret_name: str) -> str:

    key_vault_uri = os.getenv("KEY_VAULT_URI")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    secret = client.get_secret(test_secret_name)

    return secret
