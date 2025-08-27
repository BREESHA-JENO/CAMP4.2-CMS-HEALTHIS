import pymysql
from pymysql.err import MySQLError

class DBConnection:
    """Singleton MySQL DB connection for CMS Pharmacist project."""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DBConnection, cls).__new__(cls)
            cls.__instance.__initialize()
        return cls.__instance

    def __initialize(self):
        try:
            self.connection = pymysql.connect(
                host="localhost",
                user="root",
                password="faith",
                database="cms",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            print("✅ Connected to MySQL (singleton).")
        except MySQLError as e:
            print(f"DB connection error: {e}")
            self.connection = None

    def get_connection(self):
        return self.connection
