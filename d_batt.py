import paho.mqtt.client as mqtt

# Create a client instance
client = mqtt.Client()
client.connect("localhost", 1883, 60)

client.subscribe("102775313/temp/battery")

# Define warning_msg as a global variable
warning_msg = ""

def on_message(client, userdata, msg):
    global warning_msg  # Declare warning_msg as global
    battery = msg.payload.decode()
    if "%" in battery:
        battery_level = int(battery.split(": ")[1].split()[0].strip('%'))  # Extract the battery level as an integer
        if battery_level == 20:
            warning_msg = "\n\tBattery level: CRITICAL\n"
            client.publish("102775313/temp/battery", "CRITICAL battery level")
        elif battery_level == 0:
            warning_msg = "\n\tBattery level: Replace battery immediately"
            client.publish("102775313/temp/battery", "Replace battery immediately")
        else:
            warning_msg = f"\n\tBattery Level: {battery_level}%\n"
        print(warning_msg)

client.on_message = on_message

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()
