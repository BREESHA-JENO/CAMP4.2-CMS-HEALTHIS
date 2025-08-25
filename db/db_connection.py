import configparser
import pymysql
from pymysql.err import MySQLError

class DBConnection:
    """Singleton DB Connection"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DBConnection, cls).__new__(cls)
            cls.__instance.__initialize()
        return cls.__instance

    def __initialize(self):
        try:
            config = configparser.ConfigParser()
            config.read("db_config.ini")
            self.connection = pymysql.connect(
                host=config.get("mysql", "host"),
                user=config.get("mysql", "user"),
                password=config.get("mysql", "password"),
                database=config.get("mysql", "database")
            )
            print("✅ Connected to MySQL")
        except MySQLError as e:
            print(f"DB Connection Error: {e}")
            self.connection = None

    def get_connection(self):
        return self.connection
