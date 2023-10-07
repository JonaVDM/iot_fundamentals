from pkg.cloud import Cloud
from pkg.mqtt import Mqtt
from pkg.database import Database
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Make database connnection
db_host = getenv('DB_HOST', '')
db_user = getenv('DB_USER', '')
db_pass = getenv('DB_PASS', '')
db_name = getenv('DB_NAME', '')
db = Database(db_host, db_user, db_pass, db_name)

# Make azure connection
az_connection = getenv('AZURE_CONNECTION', '')
cloud = Cloud(az_connection, db)

# Make connection to mqtt server
mt_host = getenv('MQTT_HOST', '')
mt_port = getenv('MQTT_PORT', 1883)
mt_user = getenv('MQTT_USER', '')
mt_pass = getenv('MQTT_PASS', '')
mt_topic = getenv('MQTT_TOPIC', 'climate')

mqtt = Mqtt(mt_host, int(mt_port), mt_user, mt_pass, mt_topic, db, cloud)
mqtt.loop()
