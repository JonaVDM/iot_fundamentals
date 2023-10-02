import json
import datetime
import database
import paho.mqtt.client as paho


class Mqtt():
    topic = ''
    db: database.Database
    client: paho.Client

    def __init__(self, host, port, username, password, topic, database):
        self.topic = topic
        self.db = database
        self.client = paho.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connection
        self.client.username_pw_set(username, password)
        self.client.connect(host, port, 60)

    def on_connection(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode('utf8'))

        now = datetime.datetime.now()
        temp = str.replace(data['temperature'], 'C', '')
        hum = str.replace(data['humidity'], '%', '')
        pres = str.replace(data['pressure'], 'hPa', '')
        client = data['client']

        print(data)

        self.db.insert(temp, pres, hum, now, client)

    def loop(self):
        self.client.loop_forever()
