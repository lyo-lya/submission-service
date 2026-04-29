import os
import json
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()

CONNECTION_STR = os.getenv("SERVICE_BUS_CONNECTION_SEND")
QUEUE_NAME = "volhaplatnitskaya"


def send_message(data: dict):
    with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
        sender = client.get_queue_sender(queue_name=QUEUE_NAME)

        with sender:
            message = ServiceBusMessage(json.dumps(data))
            sender.send_messages(message)

    print("Message sent to Azure Service Bus")