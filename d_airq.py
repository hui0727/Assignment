import paho.mqtt.client as mqtt
import random
import time

client = mqtt.Client()
client.connect("localhost", 1883)

status = "off"

# def on_message(client, userdata, message):
    # print(f"Received message: {message.payload.decode()}")

def on_message(client, userdata, message):
    if message.topic == "public/temp":
        print(f"Received message from public/airq: {message.payload.decode()}")

client.on_message = on_message
client.subscribe("public/temp")

client.loop_forever()

while True:
    air_quality = random.randint(400, 1500)
    
    if air_quality > 1000 and status == "off":
        client.publish("public/airq", f"Air Quality: {air_quality} ppm")
        client.publish("public/status", "on")
        status = "on"
        time.sleep(3600)  # Stay on for 1 hour
    else:
        client.publish("public/airq", f"Air Quality: {air_quality} ppm")
        time.sleep(5)


