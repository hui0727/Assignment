import paho.mqtt.client as mqtt

status = "off"

def on_message(client, userdata, message):
    global status

    if message.topic == "public/temperature":
        temperature = float(message.payload)
        if temperature >= 26:
            status = "on"
            client.publish("public/status", "on")
    elif message.topic == "public/airq":
        air_quality = float(message.payload)
        if air_quality > 1000:
            status = "on"
            client.publish("public/status", "on")
    elif message.topic == "public/status":
        status = str(message.payload.decode("utf-8").strip())
        if status == "on":
            client.publish("user3/control", "on")
            client.publish("user3/control", "off", qos=1, retain=True)  # Set status back to off after 1 hour

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("public/temperature")
client.subscribe("public/airq")
client.subscribe("public/status")

client.loop_forever()
