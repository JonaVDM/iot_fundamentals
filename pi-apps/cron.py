import database
from cloud import Cloud
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Make database connnection
db_host = getenv('DB_HOST', '')
db_user = getenv('DB_USER', '')
db_pass = getenv('DB_PASS', '')
db_name = getenv('DB_NAME', '')
db = database.Database(db_host, db_user, db_pass, db_name)

# Make azure connection
az_connection = getenv('AZURE_CONNECTION', '')
cloud = Cloud(az_connection, db)

items = db.get_not_send()
if len(items) == 0:
    print("No items to send")
else:
    for item in db.get_not_send():
        cloud.send_data(item)
    print("Send" + len(items) + "items")
