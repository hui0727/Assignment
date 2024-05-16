import paho.mqtt.client as mqtt
import random
import time

client = mqtt.Client()
client.connect("localhost", 1883)

status = "off"
last_temp = None  # Initialize last_temp

def on_message(client, userdata, message):
    global last_temp  # Add last_temp to the global variables
    if message.topic == "public/temp":
        last_temp = float(message.payload.decode().split(": ")[1].split("°")[0])  # Extract the temperature value from the message payload
        print(f"Received temperature: {last_temp}°C")  # Include the unit of measurement

client.on_message = on_message
client.subscribe("public/temp")

client.loop_start()  # Start the loop in a separate thread

while True:
    air_quality = random.randint(400, 1500)
    client.publish("public/airq", f"Air Quality: {air_quality} ppm")
    if last_temp is not None:  # Make sure last_temp is not None before publishing
        client.publish("public/data", f"Temperature: {last_temp:.2f}°C, Air Quality: {air_quality} ppm")
    time.sleep(10)  # Sleep for 10 seconds

client.loop_stop()
