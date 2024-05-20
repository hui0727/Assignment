import paho.mqtt.client as mqtt
import random
import time
import sys

# MQTT Broker settings
broker = "192.168.12.100"
# broker = "localhost"
port = 1883
username = "102775313"  # Replace with your student ID
password = "102775313"  # Replace with your student ID

# Initialize variables
battery = 100  # Initial battery level
last_airq = None  # Initialize last_airq
warning_msg = ""  # Initialize warning_msg

# MQTT callback when a message is received
def on_message(client, userdata, message):
    global last_airq, warning_msg
    if message.topic == "public/airq":
        last_airq = int(message.payload.decode().split(": ")[1].split()[0])  # Extract the air quality value
        print(f"Received air quality: {last_airq} ppm")
    elif message.topic == "102775313/temp/battery":
        battery_msg = message.payload.decode()
        if "CRITICAL battery level" in battery_msg or "Replace battery immediately" in battery_msg:
            warning_msg = f"\n\t{battery_msg}"
            print(warning_msg)

# Set up the MQTT client
client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker, port)

client.on_message = on_message
client.subscribe("public/airq")
client.subscribe("102775313/temp/battery")

client.loop_start()  # Start the loop in a separate thread

try:
    while battery > 0:
        temperature = random.uniform(22, 28)
        
        # Publish battery level to private topic
        client.publish("102775313/temp/battery", f"Battery Level: {battery}%")
        battery -= 10  # Decrement battery level by 10 every 30 seconds
        
        client.publish("public/temp", f"Temperature: {temperature:.2f}°C")
        if last_airq is not None:
            client.publish("public/data", f"Temperature: {temperature:.2f}°C, Air Quality: {last_airq} ppm")

        time.sleep(30)  # Sleep for 30 seconds

    # When battery is <= 0, publish the shutdown message
    warning_msg = "\n\tBattery level low.. Replace battery immediately!"
    client.publish("102775313/temp/battery", f"Battery level: {battery}%\n{warning_msg}")
    client.publish("public/shutdown", "System down")
    print("No battery...System down")

    time.sleep(5)  # Wait for a few seconds before quitting

except KeyboardInterrupt:
    print("\nInterrupted by user")

finally:
    client.loop_stop()  # Stop the loop
    client.disconnect()  # Disconnect from the broker
    sys.exit()  # Exit the program
