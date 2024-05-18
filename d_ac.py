import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("localhost", 1883)

client.subscribe("public/temperature")
client.subscribe("public/airq")
client.subscribe("public/status")
client.subscribe("public/data")
client.subscribe("public/shutdown")

status = "off"
last_temp = None
last_airq = None
last_on_time = None
last_off_time = None  # Record the time when status changed to "off"
running = True  # Flag to control the main loop

def print_status():
    global status, last_temp
    if status == "off":
        print("\n\tStatus: off\n\tSMARTO is now turned off\n")
        client.publish("public/status", "off")  # Publish "off" to "public/status" when status is "off"
        print("*\t" * 10)

    else:
        print(f"\n\tStatus: {status}")
        print("\n\tSMARTO is now turned on\n")
        if last_temp and last_airq is not None:
            print(f"\tLast temperature that turned it on: {last_temp}°C")  # Include the unit of measurement
            print(f"\n\tLast air quality that turned it on: {last_airq} ppm\n")  # Include the unit of measurement
            print("*\t" * 10)

print_status()  # Print the initial status

def on_message(client, userdata, message):
    global status, last_temp, last_airq, last_on_time, last_off_time, running

    try:
        if message.topic == "public/temperature":
            last_temp = float(message.payload.decode().split(": ")[1].strip())
            last_temp = round(last_temp, 2)  # Round the temperature value to two decimal places
        elif message.topic == "public/airq":
            last_airq = float(message.payload.decode().split(": ")[1].split()[0])
        elif message.topic == "public/data":
            # Handle the data from "public/data" here
            data = message.payload.decode().split(", ")
            last_temp = round(float(data[0].split(": ")[1].strip("°C")), 2)
            last_airq = float(data[1].split(": ")[1].strip(" ppm"))
            if status == "on":  # Only print the data if the status is "on"
                print(f"\t\tData received from 'public/data': \n\t\tTemperature: {last_temp}°C, \n\t\tAir Quality: {last_airq} ppm\n")
                print("*\t" * 10)
        elif message.topic == "public/shutdown":
            shutdown_message = message.payload.decode()
            if shutdown_message == "System down":
                print("No battery...System down")
                print()
                client.loop_stop()
                running = False  # Set the running flag to False to exit the loop
        if last_temp is not None and last_airq is not None:
            if last_temp >= 26 and last_airq > 1000 and status == "off" and (last_off_time is None or time.time() - last_off_time >= 30):
                status = "on"
                last_on_time = time.time()  # Record the time when status changed to "on"
                client.publish("public/status", "on")
                print_status()
  
    except Exception as e:
        print(f"An error occurred: {e}")

client.on_message = on_message

client.loop_start()  # Start the loop in a separate thread

while running:  # Check the running flag to control the loop
    if status == "on" and last_on_time is not None and time.time() - last_on_time >= 30:
        status = "off"
        last_off_time = time.time()  # Record the time when status changed to "off"
        print_status()
    time.sleep(1)  # Sleep for a short time to prevent high CPU usage
    
client.loop_stop()
