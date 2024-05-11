# python 3.11
import random
import time

from paho.mqtt import client as mqtt_client

broker = '192.168.12.100'
port = 1883
topic = "102776866/python/mqtt"
topic1 = "public/"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username = '102776866'
password = '102776866'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, parameter):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        time.sleep(1)
        temperature = random.uniform(20, 30)  # Random temperature between 20 and 30
        humidity = random.uniform(40, 60)  # Random humidity between 40 and 60

        # Create JSON payload
        payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'
        client.publish(topic, payload)
        print(f"Published: {payload}")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.subscribe(topic1)
    client.on_message = on_message

def trigger_data(client):
    input("Press Enter to generate and publish data..")
    temperature = random.uniform(20, 30)  # Random temperature between 20 and 30
    humidity = random.uniform(40, 60)  # Random humidity between 40 and 60

    # Create JSON payload
    payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'
    client.publish(topic, payload)
    print(f"Published: {payload}")

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    
    while True:
        trigger_data(client)
        time.sleep(1)


if __name__ == '__main__':
    run()
