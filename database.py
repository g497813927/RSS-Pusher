"""
Database module for the project
Author: Jiacheng Zhao (John)
Date: 11/12/22
"""
import sqlite3


class Database:

    def __init__(self, db_name: str) -> None:
        """
        Constructor for the class,
        used to connect to the database.
        Due to time constraints,
        this would only implement the sqlite way.
        """
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def is_database_empty(self) -> bool:
        """
        Check if the database do not have any data
        :return: True if the database is empty, False otherwise
        """
        return len(self.cursor.execute("SELECT COUNT(*) FROM sqlite_master").fetchall()) == 0

    def close(self) -> None:
        """
        Close the connection to the database
        :return: None
        """
        self.connection.close()

    def add_feed_list(self, feed_data) -> None:
        """
        Add the feed list to the database
        :param feed_data: list of the feed
        :return: None
        """
        # Check if the database is empty
        if self.is_database_empty():
            Database.init_db(self.db_name)
        else:
            # Add the data
            SQL = """
            INSERT INTO feed_list (feed_link, title, description, subscribers, last_update, refresh_rate, dump) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(SQL)

    @staticmethod
    def init_db(db_name: str) -> None:
        """
        Initialize the database
        :param db_name: Name of the database
        :return: None
        """
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE "feed_list" (
            "feed_link"	TEXT NOT NULL UNIQUE,
            "title"	TEXT NOT NULL,
            "description"	TEXT,
            "subscribers"   JSON NOT NULL,
            "last_update"   TIMESTAMP NOT NULL,
            "refresh_rate"  INTEGER NOT NULL,
            "dump"   JSON NOT NULL,
            PRIMARY KEY("feed_link")
        );
        """)
        cursor.execute("""
        CREATE TABLE "feed_data" (
            "feed_link"	TEXT NOT NULL,
            "title"	TEXT NOT NULL,
            "description"	TEXT,
            "link"	TEXT,
            "last_update"   TIMESTAMP NOT NULL,
            "dump"   JSON NOT NULL,
            FOREIGN KEY("feed_link") REFERENCES "feed_list"("feed_link")
            );
        """)
        cursor.execute("""
        CREATE TABLE "user_list" (
            "user_id"	TEXT NOT NULL UNIQUE,
            "use_email"	BOOL NOT NULL,
            "email"	TEXT,
            "use_sms"  BOOL NOT NULL,
            "phone_number"	TEXT,
            "subscribed_feeds"   JSON NOT NULL,
            PRIMARY KEY("user_id")
        );
        """)
        connection.commit()
        connection.close()
