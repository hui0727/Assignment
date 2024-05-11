#Temperature Monitoring System
#The client who subscribes to the topic and receives data send from publisher

import paho.mqtt.client as mqtt

# Connection callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        # Subscribe to the necessary topics
        client.subscribe("102773003/home/temperature")  # Subscribe to temperature topic
        client.subscribe("public/#")  # Subscribe to public channel
    else:
        print("Connection failed with result code:", rc)

# Message callback
def on_message(client, userdata, msg):
    # Print received message with topic information
    print("Received message from topic", msg.topic, ":", msg.payload.decode())

# Create the MQTT client
client = mqtt.Client()
# client.username_pw_set("102773003", "102773003")  # Set credentials

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect("localhost", 1883, 60)  # Connect with timeout

# Start the client loop to handle messages
client.loop_forever()  # Keep the client running indefinitely