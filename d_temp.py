import paho.mqtt.client as mqtt
import random
import time

client = mqtt.Client()
client.connect("localhost", 1883)

status = "off"
battery = 100  # Initial battery level

def on_message(client, userdata, message):
    if message.topic == "public/airq":
        print(f"Received message from public/airq: {message.payload.decode()}")

client.on_message = on_message
client.subscribe("public/airq")

client.loop_start()  # Start the loop in a separate thread

while True:
    temperature = random.uniform(22, 28)
    
    # Publish battery level to private topic
    if battery != 0 :
        client.publish("102773003/temp/battery", f"Battery Level: {battery}%")
        # Decrement battery level by 1 every 5 seconds
        battery -= 1
        time.sleep(30)
    
    if temperature > 26 and status == "off":
        client.publish("public/temp", "Temperature: {:.2f}°C".format(temperature))
        # client.publish("public/status", "on")
        status = "on"
        time.sleep(10)  # Stay on for 1 hour(3600)
    else:
        client.publish("public/temp", "Temperature: {:.2f}°C".format(temperature))
        time.sleep(5)
