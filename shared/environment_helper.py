from os import environ
from shared.key_vault_helper import get_key_vault_secret


def verify_key_vault_parameters(parameters: dict) -> None:

    for parameter, secret_name in parameters.items():

        if not environ.get(parameter):

            environ[parameter] = get_key_vault_secret(secret_name)