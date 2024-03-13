"""
prob-mqtt.py: Creates a mqtt test client that can publish and receive messages on a specified topic
"""

__author__ = "Tim Rietdijk"
__email__ = "tim.is@live.nl"
__status__ = "Development"

# First party imports:
import json
import logging
import random
import time
from typing import NoReturn

# Third-party imports:
from paho.mqtt import client as mqtt_client

# python 3.10

"""
Set global variables:
"""
BROKER: str = 'c407834b.ala.asia-southeast1.emqxsl.com'
PORT: int = 8883
TOPIC: str = "python-mqtt/tcp"

CLIENT_ID: str = f'python-mqtt-tcp-pub-sub-{random.randint(0, 1000)}'
USERNAME: str = 'localAuth'
PASSWORD: str = 'Nietvergeten223'

FIRST_RECONNECT_DELAY: int = 1
RECONNECT_RATE: int = 2
MAX_RECONNECT_COUNT: int = 12
MAX_RECONNECT_DELAY: int = 60


def on_connect(client: mqtt_client.Client, userdata, flags, rc: int) -> NoReturn:
    """
    New implementation of the MQTT Client function 'on_connect'.
    Log the connection status in the console and subscribe to the global Topic

    :param client: self
    :param userdata: n/a
    :param flags: n/a
    :param rc: return code representation as an integer
    :return: None
    """
    if rc == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f'Failed to connect, return code {rc}')


def on_disconnect(client: mqtt_client.Client, userdata, rc: int) -> NoReturn:
    """
    New implementation of the MQTT Client function 'on_disconnect'.
    Log the connection status in the console and disable reconnect.

    :param client: self
    :param userdata: n/a
    :param rc: return code representation as an integer
    :return: None
    """
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    global FLAG_EXIT
    FLAG_EXIT = True


def on_message(client: mqtt_client.Client, userdata, msg: mqtt_client.MQTTMessage) -> NoReturn:
    """
    logs the received message in the console.

    :param client: self
    :param userdata: n/a
    :param msg: received message as a ByteString
    :return: None
    """
    print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')


def connect_mqtt() -> mqtt_client.Client:
    """
    This function creates a mqtt client and will try to connect it to the globally defined broker

    :return: Created mqtt client
    """
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(ca_certs='./emqxsl-ca.crt')
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=3)
    client.on_disconnect = on_disconnect
    return client


def publish(client: mqtt_client.Client) -> NoReturn:
    """
    Publishes a message to the broker on the globally defined topic.

    :param client: self
    :return: None
    """
    msg: str = json.dumps({'msg': 'hi'})
    if not client.is_connected():
        logging.error("publish: MQTT client is not connected!")
    result: mqtt_client.MQTTMessageInfo = client.publish(TOPIC, msg)
    status: int = result[0]
    if status == 0:
        logging.info(f"publish: '{msg}' - was successfully sent")
    else:
        logging.error(f"publish: '{msg}' - failed to send")


def mqttRun() -> NoReturn:
    """
    Run the mqtt client test application.

    :return: None
    """
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    client: mqtt_client.Client = connect_mqtt()
    if client.is_connected():
        print('publishing now')
        publish(client=client)


