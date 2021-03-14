import sys
import json
import logging

import requests
import msal

config = {
    'authority': 'https://login.microsoftonline.com/common',
    'client_id': '5fbf6ac1-437f-4ea3-a64b-e8c3287bff57',
    'scope': ['Tasks.ReadWrite', 'User.Read'],
    'secret': 'XhP~_76-1~h_3owuUS_Q74ot4m2NsFPy3~',
    'endpoint': 'https://graph.microsoft.com/v1.0/me'
}

code = None
code='M.R3_BAY.1bc52a0a-d1fe-d0b9-8d6b-cebfeab94c27'

app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"],
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.readthedocs.io/en/latest/#msal.SerializableTokenCache
    )

if not code:
    authorization_url = app.get_authorization_request_url(config['scope'])
    print(authorization_url)
else:
    result = app.acquire_token_by_authorization_code(code, scopes=config["scope"])
    print(result)