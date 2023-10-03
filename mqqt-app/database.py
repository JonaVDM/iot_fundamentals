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


class Database:
    connection: pymysql.Connection

    def __init__(self, host, user, password, database):
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
