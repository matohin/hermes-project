import azure.functions as func
from output_trunk_telegram import main, set_callback_webhook


def test_output_trunk_telegram():

    incoming_service_bus_msg = func.servicebus.ServiceBusMessage(
        body=b"{}", message_id="id123", user_properties={"user1": "description1"}
    )

    result = main(incoming_service_bus_msg)

    set_callback_webhook(
        "https://func11.azurewebsites.net/api/input_trunk_telegram?code=UYKRY7CDM/X1vJm9lmc5R3GE6uvtQnaUDCFUCkQaB0aAuGEQIWCp4A=="
    )
