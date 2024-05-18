import paho.mqtt.client as mqtt
import random
import time

client = mqtt.Client()
client.connect("localhost", 1883)

status = "running"  # Initialize system status
last_temp = None

def on_message(client, userdata, message):
    global status, last_temp
    if message.topic == "public/temp":
        last_temp = float(message.payload.decode().split(": ")[1].split("°")[0])
        print(f"Received temperature: {last_temp}°C")
    elif message.topic == "public/shutdown":
        shutdown_message = message.payload.decode()
        if shutdown_message == "System down":
            print("No battery...System down")
            print()
            status = "down"  # Update system status
            client.loop_stop()

client.on_message = on_message
client.subscribe("public/temp")
client.subscribe("public/shutdown")

client.loop_start()

try:
    while status == "running":  # Check system status before publishing air quality data
        air_quality = random.randint(400, 1500)
        client.publish("public/airq", f"Air Quality: {air_quality} ppm")
        if last_temp is not None:
            client.publish("public/data", f"Temperature: {last_temp:.2f}°C, Air Quality: {air_quality} ppm")
        time.sleep(10)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
