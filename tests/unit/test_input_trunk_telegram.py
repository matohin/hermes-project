import azure.functions as func
from input_trunk_telegram import main


def test_input_trunk_telegram():

    body = b"""{
        "update_id": 612015913,
        "message": {
            "message_id": 13,
            "from": {
                "id": 55033450,
                "is_bot": false,
                "first_name": "Evgeniy",
                "last_name": "Matohin",
                "username": "matohin",
                "language_code": "en",
            },
            "chat": {
                "id": 55033450,
                "first_name": "Evgeniy",
                "last_name": "Matohin",
                "username": "matohin",
                "type": "private",
            },
            "date": 1615635247,
            "text": "TEST",
        }
    }"""

    incoming_http_request = func.HttpRequest(method="POST", url="local", body=body)

    result = main(incoming_http_request)
    actual = result.get_body()

    # expected = b"Hello, Test. This HTTP triggered function executed successfully."
    # assert actual == expected

