import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
# client.username_pw_set("102773003", "102773003")  # Set username and password
# Connect to the broker
client.connect("localhost", 1883, 60)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("102773003/Messageboard")  # Subscribe to required topics
        client.subscribe("temperature")
        client.subscribe("user")
        client.subscribe("light")
        print("Subscribed debuggggggggggging")
    else:
        print("Connection failed with result code:", rc)

# Message callback
def on_message(client, userdata, msg):
    print("Received:", msg.topic, "Message:", msg.payload.decode())

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Start the client loop
client.loop_start()

# Publish a test message
client.publish("Messageboard", "This is a test message")

time.sleep(60)
