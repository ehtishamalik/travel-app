import sqlite3
import os


class MyDatabase:
    def __init__(self, db_name="database/my_database.db"):
        folder_path = os.path.dirname(db_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.db_name = db_name
        self.create_database()

    def create_database(self):
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table_message()
        self.create_table_destinations()

    def create_table_message(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS MESSAGES (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email CHAR(60),
        name CHAR(60),
        phone CHAR(15),
        message CHAR(400))
        """
        )
        self.connection.commit()

    def create_table_destinations(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS DESTINATIONS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name CHAR(30),
        description CHAR(400),
        image CHAR(40))
        """
        )
        self.connection.commit()

    def add_message(self, email, name, phone, message):
        try:
            self.cursor.execute(
                "INSERT INTO MESSAGES (email, name, phone, message) VALUES (?, ?, ?, ?)",
                (email, name, phone, message),
            )
            self.connection.commit()
            print("Data Added Successfully")
        except sqlite3.IntegrityError as e:
            print("ERROR", e)
            print("Data not added due to primary key violation.")
        except Exception as e:
            print("Error:", e)
            print("Data not added.")

    def add_destination(self, name, description, image):
        try:
            self.cursor.execute(
                "INSERT INTO DESTINATIONS (name, description, image) VALUES (?, ?, ?)",
                (name, description, image),
            )
            self.connection.commit()
            print("Data Added Successfully")
        except sqlite3.IntegrityError as e:
            print("ERROR", e)
            print("Data not added due to primary key violation.")
        except Exception as e:
            print("Error:", e)
            print("Data not added.")

    def get_all_messages(self):
        try:
            self.cursor.execute("SELECT * FROM MESSAGES")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"[ ERROR ] {e}")
            return []

    def get_all_destination(self):
        try:
            self.cursor.execute("SELECT * FROM DESTINATIONS")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"[ ERROR ] {e}")
            return []

    def close_connection(self):
        self.connection.close()


database = MyDatabase()
