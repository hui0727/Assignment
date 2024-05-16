import paho.mqtt.client as mqtt
import random
import time

client = mqtt.Client()
client.connect("localhost", 1883)

battery = 100  # Initial battery level
last_airq = None  # Initialize last_airq
warning_msg = ""  # Initialize warning_msg

def on_message(client, userdata, message):
    global last_airq  # Add last_airq to the global variables
    global warning_msg  # Add warning_msg to the global variables
    if message.topic == "public/airq":
        last_airq = int(message.payload.decode().split(": ")[1].split()[0])  # Extract the air quality value from the message payload and convert it to an integer
        print(f"Received air quality: {last_airq} ppm")  # Include the unit of measurement
    elif message.topic == "102775313/temp/battery":
        battery = message.payload.decode()
        if "CRITICAL battery level" in battery or "Replace battery immediately" in battery:
            warning_msg = f"\n\t{battery}"
            print(warning_msg)

client.on_message = on_message
client.subscribe("public/airq")
client.subscribe("102775313/temp/battery")  # Subscribe to "102775313/temp/battery"

client.loop_start()  # Start the loop in a separate thread

while battery > 0:  # Only publish temperature readings if battery > 0
    temperature = random.uniform(22, 28)
    
    # Publish battery level to private topic
    client.publish("102775313/temp/battery", f"Battery Level: {battery}%")
    # Decrement battery level by 10 every 30 seconds
    battery -= 10
    time.sleep(1)
    
    client.publish("public/temp", "Temperature: {:.2f}°C".format(temperature))
    if last_airq is not None:  # Make sure last_airq is not None before publishing
        client.publish("public/data", f"Temperature: {temperature}, Air Quality: {last_airq} ppm")  # Include the unit of measurement
    time.sleep(5)  # Sleep for 5 seconds

if battery <= 0:
    warning_msg = "\n\tBattery level: Replace battery immediately"
    client.publish("102775313/temp/battery",f"Battery level: {battery}%\n {warning_msg}")
    print(warning_msg)
    time.sleep(5)

client.loop_stop()
