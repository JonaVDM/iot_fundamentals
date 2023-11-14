import pkg.ai as ai
import pkg.database as database
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timedelta

load_dotenv()

model = ai.AI()

db_host = getenv('DB_HOST', '')
db_user = getenv('DB_USER', '')
db_pass = getenv('DB_PASS', '')
db_name = getenv('DB_NAME', '')
db = database.Database(db_host, db_user, db_pass, db_name)

now = datetime.now()
yesterday = datetime.now() - timedelta(days=1)
entries = db.get_data(yesterday, now)
entry = entries[0]
print(model.perdict(entry))
