# Temperature Monitoring System
# The client who publishes the temperature and reacts to incoming messages
# Subscribe to'1027xxxxx/home/command' to receive command to adjust its behavior

import paho.mqtt.client as mqtt
import time
import random

# Create an MQTT client
client = mqtt.Client()
# client.username_pw_set("102773003", "102773003")  # Set credentials

# Connection callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("102773003/home/command")  # Subscribe to a command topic
        client.subscribe("public/#")  # Subscribe to all public messages
    else:
        print("Connection failed with result code:", rc)

# Message callback
def on_message(client, userdata, msg):
    # React to incoming messages
    print("Received command from topic:", msg.topic, "-", msg.payload.decode())
    
    if msg.topic == "102773003/home/command":
        command = msg.payload.decode()
        if command == "report_temperature":
            temperature = random.uniform(15.0, 25.0)  # Generate random temperature
            client.publish("102773003/home/temperature", f"{temperature:.2f}")  # Publish temperature
            print(f"Published temperature: {temperature:.2f}")  # Output to terminal

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("localhost", 1883, 60)  # Ensure correct broker address and port

# Start the client loop to handle messages
client.loop_start()  # Keeps the client running to process messages

# Publish temperature data every 5 seconds and print it
while True:
    temperature = random.uniform(15.0, 25.0)  # Generate random temperature
    client.publish("102773003/home/temperature", f"{temperature:.2f}")  # Publish temperature
    print(f"Sent temperature: {temperature:.2f}")  # Output to terminal
    time.sleep(5)  # Wait 5 seconds before publishing the next reading
