import paho.mqtt.client as mqtt
import database
import datetime
import json


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
    db.insert(temp, pres, hum, now.strftime("%Y-%m-%d %H:%M:%S"), 'thing')


db = database.Database("localhost", "maria",  "secret", "climate")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("admin", "secretpass")
client.connect("172.21.1.56", 1883, 60)

client.loop_forever()
