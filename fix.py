import bcrypt
from datetime import datetime
from db.db_connection import DBConnection
from dao.admin.StaffDao import StaffDAO


def create_default_user_credentials(staff_id, username, conn):
    cursor = conn.cursor()
    default_password = "Temp@123"  # You can change this or generate dynamically
    hashed_password = bcrypt.hashpw(default_password.encode(), bcrypt.gensalt()).decode()

    query = """
    INSERT INTO user_credentials (staff_id, username, password, created_at)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (staff_id, username, hashed_password, datetime.now()))
    conn.commit()
    cursor.close()
    print(f"Created user credentials for staff_id: {staff_id} with username: {username}, default password: {default_password}")


def fix_missing_staff_ids_and_users():
    staff_dao = StaffDAO()
    conn = staff_dao.conn
    cursor = conn.cursor()

    # Select staff with NULL or empty staff_id
    cursor.execute("""
        SELECT staff_name, role_id, dob, gender, doj, blood_group, phone, email, address, isActive 
        FROM Staff WHERE staff_id IS NULL OR staff_id = ''
    """)
    rows = cursor.fetchall()

    for row in rows:
        staff_name, role_id, dob, gender, doj, blood_group, phone, email, address, isActive = row

        role_map = {
            1: "Admin",
            2: "Receptionist",
            3: "Doctor",
            4: "Lab Technician",
            5: "Pharmacist"
        }
        role_name = role_map.get(role_id, "Staff")

        new_staff_id = staff_dao.generate_staff_id(role_name)
        print(f"Assigning new staff_id {new_staff_id} to staff {staff_name}")

        # Update Staff with new staff_id
        update_query = """
            UPDATE Staff SET staff_id = %s WHERE phone = %s AND email = %s
        """
        cursor.execute(update_query, (new_staff_id, phone, email))
        conn.commit()

        # Check if user credentials exist for this staff (by phone or email can be better keyed by staff_id but we fixed just now)
        cursor.execute("SELECT 1 FROM user_credentials WHERE staff_id=%s", (new_staff_id,))
        if not cursor.fetchone():
            # Create default username (use email prefix or staff name)
            default_username = email.split('@')[0] if email else f'user_{new_staff_id.lower()}'
            create_default_user_credentials(new_staff_id, default_username, conn)

    cursor.close()
    print("Staff IDs and user credentials update completed.")


if __name__ == "__main__":
    fix_missing_staff_ids_and_users()
