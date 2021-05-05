from os import environ
from shared.key_vault_helper import get_key_vault_secret

# Dictonary format {"ENVIRONMENT_VARIABLE_NAME": "nameOfSecretInKeyVault"}
KEVAULT_ENV_VARS = {
    "TELEGRAM_API_TOKEN": "telegramBotToken",
    "CHAT_ID": "ChatId",
    "CHAT_AUTH_KEY": "chatAuthKey",
}


def verify_key_vault_parameters(parameters: dict) -> None:

    for parameter, secret_name in parameters.items():

        if not environ.get(parameter):

            secret_value = get_key_vault_secret(secret_name)

            if secret_value:

                environ[parameter] = secret_value

            else:

                environ[parameter] = "NOT DEFINED"
