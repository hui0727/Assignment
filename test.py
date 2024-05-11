import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Messageboard")
    client.subscribe("temperature")
    client.subscribe("user")
    client.subscribe("light")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))

client = mqtt.Client()
client.username_pw_set("102773003", "102773003") 
client.on_connect = on_connect
client.on_message = on_message

# client.connect("localhost", 1883, 60)  # Connect to the broker
client.connect("192.168.12.100", 1883, 60)

# Start the loop
client.loop_start()

# Publish messages to the topics
time.sleep(1)
client.publish("Messageboard", "This is a test message for bulk messages")
client.publish("temperature", "22.5")
client.publish("user", "User1")
client.publish("light", "ON")
client.publish("temperature", "30")
client.publish("user", "User2")
client.publish("light", "OFF")
client.publish("temperature", "33")
client.publish("user", "User3")
client.publish("light", "ON")

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = client.loop()
print("rc: " + str(rc))
