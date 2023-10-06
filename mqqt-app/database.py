import pymysql.cursors
import pymysql
import datetime
from dataclasses import dataclass, asdict
import json


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
        return cls(
            data['id'],
            data['pressure'],
            data['temperature'],
            data['humidity'],
            data['time'],
            data['uploaded'],
            data['device_id']
        )


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
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          database=database,
                                          cursorclass=pymysql.cursors.DictCursor)

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
