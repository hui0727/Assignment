#Temperature Monitoring System
#The client who publishes the temperature
#send data to private topic

import paho.mqtt.client as mqtt
import time
import random

# MQTT client for temperature sensor
client = mqtt.Client()
# client.username_pw_set("102773003", "102773003")  # Set credentials

# Connect to the broker
client.connect("localhost", 1883, 60)  # 60-second timeout

# Start the client loop to maintain connection
client.loop_start()

# Publish temperature readings to a private topic
while True:
    temperature = random.uniform(15.0, 25.0)  # Generate a random temperature
    client.publish("102773003/home/temperature", f"{temperature:.2f}")  # Publish to the topic
    print(f"Published temperature: {temperature:.2f}")
    time.sleep(5)  # Wait 5 seconds before publishing the next reading
