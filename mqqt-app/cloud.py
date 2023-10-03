from azure.iot.device import IoTHubDeviceClient, Message
from database import Database, Entry


class Cloud:
    connection: IoTHubDeviceClient
    db: Database

    def __init__(self, connectionString: str, db: Database):
        """
        Create a new object that connects to the azure and sends data

        :param connectionString: The device connection string from azure
        :param db: Database object to update the entries
        """
        self.connection = IoTHubDeviceClient.create_from_connection_string(connectionString, connection_retry=False)
        self.connection.connect()
        self.db = db

    def send_data(self, entry: Entry):
        """
        Send data to the cloud

        :param entry: The object with data to send
        """
        if not self.connection.connected:
            pass

        msg = Message(entry.json())
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"

        try:
            self.connection.send_message(msg)
            self.db.mark_as_send([entry.id])
        except Exception:
            print("Failed to send data")
