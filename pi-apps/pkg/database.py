import pymysql.cursors
import pymysql
import datetime
from dataclasses import dataclass, asdict
import json
import time


@dataclass
class Entry:
    id: int
    pressure: float
    temperature: float
    humidity: float
    time: datetime.datetime
    uploaded: bool
    device_id: str

    def json(self):
        obj = asdict(self)
        obj['time'] = int(self.time.timestamp() * 1000)
        return json.dumps(obj)

    @classmethod
    def from_json(cls, data):
        obj = cls(
            data['id'],
            data['pressure'],
            data['temperature'],
            data['humidity'],
            data['time'],
            data['uploaded'],
            data['device_id']
        )

        local_timezone = datetime.timezone(datetime.datetime.now(
            datetime.timezone.utc).astimezone().utcoffset())

        obj.time = obj.time.astimezone(local_timezone)

        return obj


class Database:
    connection: pymysql.Connection

    def __init__(self, host: str, user: str, password: str, database: str):
        """
        Create a new instance

        :param host: The host address of the database
        :param user: The username
        :param password: The password
        :param database: The name of the database
        """
        retires = 5

        while retires > 0:
            try:
                self.connection = pymysql.connect(host=host,
                                                  user=user,
                                                  password=password,
                                                  database=database,
                                                  cursorclass=pymysql.cursors.DictCursor)
                break
            except Exception:
                print("Failing to connect")
                retires -= 1
                time.sleep(5)

        if retires == 0:
            print("Out of retries, giving up")
            exit(1)

    def insert(self, entry: Entry) -> Entry:
        """
        Insert a new cliamte entry to the database

        :param entry: The entry to insert
        :return: a new entry with the id inserted
        """
        sql = """
            INSERT INTO `climate` (`humidity`, `pressure`, `temperature`, `time`, `uploaded`, `device_id`)
            VALUES (%s, %s, %s, %s, '0', %s);
        """

        cursor = self.connection.cursor()
        cursor.execute(sql, (
            entry.humidity,
            entry.pressure,
            entry.temperature,
            entry.time,
            entry.device_id
        ))
        self.connection.commit()
        entry.id = cursor.lastrowid
        return entry

    def mark_as_send(self, ids: list[int]):
        """
        Mark an entry as send in the database

        :param ids: The list of ids to mark as send
        """
        try:
            sql = """
                UPDATE climate
                SET uploaded=1
                WHERE id in (%s);
            """
            cursor = self.connection.cursor()
            cursor.execute(sql, (
                ','.join(str(x) for x in ids)
            ))
            self.connection.commit()

        except Exception:
            print("Database update failed!")

    def get_not_send(self) -> list[Entry]:
        """
        Get a list of all the entries that not have been uploaded yet

        :return: The list of entries that have not been uploaded yet
        """
        sql = """
                SELECT * FROM climate
                WHERE not uploaded;
            """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        items = cursor.fetchall()
        return [Entry.from_json(item) for item in items]

    def get_data(self, start: str, end: str) -> list[Entry]:
        """
        Returns a list of entry points between start and end
        """
        sql = """
                SELECT * FROM climate
                WHERE time >= %s AND time <= %s
                ORDER BY time DESC
                LIMIT 500
            """
        cursor = self.connection.cursor()
        cursor.execute(sql, (start, end))
        items = cursor.fetchall()
        self.connection.commit()
        return [Entry.from_json(item) for item in items]

    def get_latest(self) -> Entry:
        """
        Returns the last entry point made
        """
        sql = """
                SELECT * FROM climate
                ORDER BY time DESC
                LIMIT 1
            """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        item = cursor.fetchone()
        self.connection.commit()
        return Entry.from_json(item)
