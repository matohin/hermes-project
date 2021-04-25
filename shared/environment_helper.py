from os import environ
from shared.key_vault_helper import get_key_vault_secret

# Dictonary format {"ENVIRONMENT VARIABLE NAME": "nameOfSecretInKeyVault"}
KEVAULT_ENV_VARS = {"TELEGRAM_API_TOKEN": "telegramBotToken", "CHAT_ID": "ChatId"}


def verify_key_vault_parameters(parameters: dict) -> None:

    for parameter, secret_name in parameters.items():

        if not environ.get(parameter):

            environ[parameter] = get_key_vault_secret(secret_name)