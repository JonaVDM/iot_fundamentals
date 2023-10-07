import json
import datetime
import paho.mqtt.client as paho
from pkg.cloud import Cloud
from pkg.database import Database, Entry


class Mqtt:
    topic = ''
    db: Database
    client: paho.Client
    cloud: Cloud
    sendData: bool

    def __init__(self, host: str, port: int, username: str, password: str, topic: str, database: Database, cloud: Cloud, sendData: bool):
        """
        Create a new instance of the mqtt client

        :param host: The host address of the mqtt server
        :param port: The port that is begin used
        :param username: The usernmae
        :param password: The passsword
        :param topic: The topic to subscribe to
        :param database: Instance of the database
        :param cloud: Instane of the azure instance
        """
        self.topic = topic
        self.db = database
        self.cloud = cloud
        self.client = paho.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connection
        self.client.username_pw_set(username, password)
        self.client.connect(host, port, 60)
        self.sendData = sendData

    def on_connection(self, client, userdata, flags, rc):
        """
        Create the connection to the mqtt server
        """
        print("Connected with result code "+str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        """
        Called whenever a message is received
        """
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

            if self.sendData != 0:
                print("sending data to azure")
                self.cloud.send_data(obj)

        except Exception:
            print("wel shit man, iets ging mis")

    def loop(self):
        """
        Keeps the mqtt client running
        """
        self.client.loop_forever()
