import os
import logging
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def get_key_vault_secret(secret_name: str) -> str:

    key_vault_uri = os.getenv("KEY_VAULT_URI")

    logging.info(f"Getting secret {secret_name} from {key_vault_uri}")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    logging.info(f"Starting secret retrival")
    secret = client.get_secret(secret_name)

    logging.info(f"Returning secret data")
    return secret.value


def set_key_vault_secret(secret_name: str, secret_value: str) -> None:

    key_vault_uri = os.getenv("KEY_VAULT_URI")

    logging.info(f"Getting secret {secret_name} from {key_vault_uri}")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    logging.info(f"Starting secret retrival")
    client.set_secret(secret_name, secret_value)
