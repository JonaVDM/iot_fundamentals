import json
import datetime
import paho.mqtt.client as paho
from cloud import Cloud
from database import Database, Entry


class Mqtt:
    topic = ''
    db: Database
    client: paho.Client
    cloud: Cloud

    def __init__(self, host, port, username, password, topic, database: Database, cloud: Cloud):
        self.topic = topic
        self.db = database
        self.cloud = cloud
        self.client = paho.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connection
        self.client.username_pw_set(username, password)
        self.client.connect(host, port, 60)

    def on_connection(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode('utf8'))
            print("Got some data")

            obj = Entry(
                -1,
                float(str.replace(data['pressure'], 'hPa', '')),
                float(str.replace(data['temperature'], 'C', '')),
                float(str.replace(data['humidity'], '%', '')),
                datetime.datetime.now(),
                False,
                data['client'],
            )

            obj = self.db.insert(obj)
            print(obj)
            self.cloud.send_data(obj)

        except Exception:
            print("wel shit man, iets ging mis")

    def loop(self):
        self.client.loop_forever()
