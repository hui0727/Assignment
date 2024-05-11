# python 3.11
import random
import time

from paho.mqtt import client as mqtt_client


broker = '192.168.12.100'
port = 1883
topic = "102776866/python/mqtt"
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

    #client = mqtt_client.Client(client_id)
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    #msg_count = 1
    while True:
        time.sleep(5)
        temperature = random.uniform(20, 30)  # Random temperature between 20 and 30
        humidity = random.uniform(40, 60)  # Random humidity between 40 and 60

        # Create JSON payload
        payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'
        client.publish(topic, payload)
        print(f"Published: {payload}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()

if __name__ == '__main__':
    run()
