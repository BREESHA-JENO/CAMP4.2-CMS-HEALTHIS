import pymysql
from db.db_connection import DBConnection
from models.admin_models.user import UserCredentials
from datetime import datetime
import bcrypt


class UserDAO:
    def login(self, username, password):
        conn = DBConnection().get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM user_credentials WHERE username=%s", (username,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row and bcrypt.checkpw(password.encode(), row["password"].encode()):
            return UserCredentials(
                user_id=row["user_id"],
                staff_id=row["staff_id"],
                username=row["username"],
                password=row["password"],
                created_at=row["created_at"]
            )
        return None

    def create_user(self, user: UserCredentials):
        try:
            conn = DBConnection().get_connection()
            cursor = conn.cursor()

            hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

            query = """
                INSERT INTO user_credentials (staff_id, username, password, created_at)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user.staff_id, user.username, hashed_password, user.created_at or datetime.now()))
            conn.commit()
            return True

        except Exception as e:
            print(f"Error occurred while creating user: {e}")  # Prefer logging in production
            return False

        finally:
            try:
                cursor.close()
                conn.close()
            except Exception as close_error:
                print(f"Error closing resources: {close_error}")