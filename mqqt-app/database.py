import pymysql.cursors
import pymysql


class Database:
    connection: pymysql.Connection

    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          database=database,
                                          cursorclass=pymysql.cursors.DictCursor)

    def insert(self, temperature, pressure, humidity, time, device):
        sql = "INSERT INTO `climate` (`id`, `humidity`, `pressure`, `temperature`, `time`, `uploaded`, `device_id`) VALUES (NULL, %s, %s, %s, %s, '0', %s);"
        cursor = self.connection.cursor()
        cursor.execute(sql, (humidity, pressure, temperature, time, device))
        self.connection.commit()
