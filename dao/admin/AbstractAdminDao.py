from db.db_connection import get_db_connection
from models.admin_models.admin import Admin

class AdminDAO:
    def get_admin_by_id(self, staff_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT staff_id, staff_name, email, role_id FROM Staff WHERE staff_id = %s", (staff_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Admin(row["staff_id"], row["staff_name"], row["email"], row["role_id"])
        return None
