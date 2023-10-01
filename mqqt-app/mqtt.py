import paho.mqtt.client as mqtt
import json
import datetime
import database


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("climate")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf8'))
    now = datetime.datetime.now()
    temp = str.replace(data['temperature'], 'C', '')
    hum = str.replace(data['humidity'], '%', '')
    pres = str.replace(data['pressure'], 'hPa', '')
    print(client)
    database.insert(temp, pres, hum, now.strftime("%Y-%m-%d %H:%M:%S"))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("admin", "secretpass")
client.connect("172.21.1.56", 1883, 60)
