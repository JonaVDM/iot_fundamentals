from pkg.database import Database
from flask import Flask, request
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timedelta

# Make database connnection
db_host = getenv('DB_HOST', '')
db_user = getenv('DB_USER', '')
db_pass = getenv('DB_PASS', '')
db_name = getenv('DB_NAME', '')
db = Database(db_host, db_user, db_pass, db_name)

load_dotenv()

app = Flask(__name__)


@app.route("/api/data")
def get_day():
    """
    Get data from `start` to `end`.
    Defaults to the last 24 hours.
    """

    now = datetime.now()
    yesterday = datetime.now() - timedelta(days=1)

    end = request.args.get('end', default=now)
    start = request.args.get('start', default=yesterday)

    return {
        "data": db.get_data(start, end),
        "start": start,
        "end": end,
    }
