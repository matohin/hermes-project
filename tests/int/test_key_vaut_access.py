import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

if not os.getenv("KEY_VAULT_URI"):
    os.environ["KEY_VAULT_URI"] = "https://kv-hermes-proj.vault.azure.net/"


def test_keyvault_access():

    key_vault_uri = os.environ["KEY_VAULT_URI"]

    credential = DefaultAzureCredential()
    print(credential)

    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    print(client)

    client.set_secret("secretName", "secretValue")

    # print(" done.")

    # print(f"Retrieving your secret from {keyVaultName}.")

    # retrieved_secret = client.get_secret(secretName)

    # print(f"Your secret is '{retrieved_secret.value}'.")
    # print(f"Deleting your secret from {keyVaultName} ...")

    # poller = client.begin_delete_secret(secretName)
    # deleted_secret = poller.result()

    # print(" done.")