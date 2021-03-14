import requests
import msal
import json

config = {
    "authority": "https://login.microsoftonline.com/common",
    "client_id": "5fbf6ac1-437f-4ea3-a64b-e8c3287bff57",
    "scope": ["Tasks.ReadWrite", "User.Read"],
    "endpoint": "https://graph.microsoft.com/v1.0/me",
}

app = msal.PublicClientApplication(config["client_id"], authority=config["authority"])

flow = app.initiate_device_flow(scopes=config["scope"])

print(flow)

result = app.acquire_token_by_device_flow(flow)

print(result)

print("==========")

print(app)
