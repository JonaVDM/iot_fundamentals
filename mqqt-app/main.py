import paho.mqtt.client as mqtt
import database
import datetime
import json
from dotenv import load_dotenv
from os import getenv


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("climate")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf8'))

    now = datetime.datetime.now()
    temp = str.replace(data['temperature'], 'C', '')
    hum = str.replace(data['humidity'], '%', '')
    pres = str.replace(data['pressure'], 'hPa', '')
    client = data['client']

    db.insert(temp, pres, hum, now, client)


load_dotenv()

# Make database connnection
db_host = getenv('DB_HOST', '')
db_user = getenv('DB_USER', '')
db_pass = getenv('DB_PASS', '')
db_name = getenv('DB_NAME', '')
db = database.Database(db_host, db_user, db_pass, db_name)


# Make connection to mqtt server
mt_host = getenv('MQTT_HOST', '')
mt_port = getenv('MQTT_PORT', 1883)
mt_user = getenv('MQTT_USER', '')
mt_pass = getenv('MQTT_PASS', '')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(mt_user, mt_pass)
client.connect(mt_host, int(mt_port), 60)

client.loop_forever()
