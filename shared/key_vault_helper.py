import os
import logging
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError


def get_key_vault_secret(secret_name: str) -> str:

    key_vault_uri = os.getenv("KEY_VAULT_URI")

    logging.info(f"Getting secret {secret_name} from {key_vault_uri}")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    logging.info(f"Starting secret retrival")
    try:
        secret = client.get_secret(secret_name)
        value = secret.value
    except ResourceNotFoundError:
        value = None
        logging.info(f"{secret_name} not found in {key_vault_uri}")

    logging.info(f"Returning secret data")
    return value


def set_key_vault_secret(secret_name: str, secret_value: str) -> None:

    key_vault_uri = os.getenv("KEY_VAULT_URI")

    logging.info(f"Getting secret {secret_name} from {key_vault_uri}")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    logging.info(f"Starting secret retrival")
    client.set_secret(secret_name, secret_value)
