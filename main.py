import pymysql
import time
from db.db_connection import DBConnection
from Menudriven.admin_menu import admin_menu
from Menudriven.labtest_menu import lab_menu
from Menudriven.pharma_menu import run_pharma_menu
import bcrypt
from validation.admin_val.user_validation import validate_login


# ---------- First Time Setup ----------
def first_time_setup():
    conn = DBConnection().get_connection()
    cursor = conn.cursor()

    # Insert all required roles if not present
    cursor.execute("""
        INSERT INTO Roles (role_id, role_name) VALUES
        (1, 'Admin'),
        (2, 'Receptionist'),
        (3, 'Doctor'),
        (4, 'Lab Technician'),
        (5, 'Pharmacist')
        ON DUPLICATE KEY UPDATE role_name = VALUES(role_name)
    """)

    # Check if super admin exists
    cursor.execute("SELECT COUNT(*) FROM user_credentials")
    count = cursor.fetchone()[0]

    if count == 0:
        print("⚠ No users found. Creating Super Admin...")
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Create staff record
        cursor.execute("""
            INSERT INTO Staff (staff_id, staff_name, role_id, dob, gender, doj, blood_group, phone, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE staff_name='Super Admin'
        """, ("AD001", "Super Admin", 1, "1980-01-01", "Male", "2025-08-01", "O+", "9999999999", "admin@cliniccare.com"))

        # Create credentials with lockout columns initialized
        cursor.execute("""
            INSERT INTO user_credentials (staff_id, username, password, created_at, failed_attempts, last_attempt_time)
            VALUES (%s, %s, %s, NOW(), 0, NULL)
            ON DUPLICATE KEY UPDATE username=%s, password=%s
        """, ("AD001", username, hashed_password, username, hashed_password))

        conn.commit()
        print("Super Admin created successfully")

    cursor.close()


# ---------- Login Function ----------
def login(username, password):
    db = DBConnection()
    conn = db.get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT u.staff_id, u.password, s.role_id, r.role_name,
               u.failed_attempts, u.last_attempt_time
        FROM user_credentials u
        JOIN Staff s ON u.staff_id = s.staff_id
        JOIN Roles r ON s.role_id = r.role_id
        WHERE u.username=%s
    """, (username,))
    user = cursor.fetchone()

    if not user:
        print("Invalid credentials (user not found)")
        cursor.close()
        return None

    # ⏳ Check lockout
    if user["failed_attempts"] >= 3 and user["last_attempt_time"]:
        elapsed = time.time() - user["last_attempt_time"].timestamp()
        if elapsed < 30:
            print(f"⏳ Account locked. Try again after {int(30 - elapsed)} seconds.")
            cursor.close()
            return None
        else:
            # Reset after lockout period
            cursor2 = conn.cursor()
            cursor2.execute("""
                UPDATE user_credentials
                SET failed_attempts=0, last_attempt_time=NULL
                WHERE username=%s
            """, (username,))
            conn.commit()
            cursor2.close()
            user["failed_attempts"] = 0

    # Verify password
    if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        print(f"Login successful! Role: {user['role_name']}")
        # Reset attempts
        cursor2 = conn.cursor()
        cursor2.execute("""
            UPDATE user_credentials
            SET failed_attempts=0, last_attempt_time=NULL
            WHERE username=%s
        """, (username,))
        conn.commit()
        cursor2.close()
        cursor.close()
        return user
    else:
        print("Invalid credentials")
        # Increment attempts
        cursor2 = conn.cursor()
        cursor2.execute("""
            UPDATE user_credentials
            SET failed_attempts=failed_attempts+1, last_attempt_time=NOW()
            WHERE username=%s
        """, (username,))
        conn.commit()
        cursor2.close()
        cursor.close()
        return None


# ---------- Navigation ----------
def navigate(user):
    role = user["role_name"].lower()
    if role == "admin":
        print('''
              \t\t\t\t\t➡ Navigating to Admin menu...
              \t\t\t\t\t----------------------------\t\t''')
        admin_menu()
    elif role == "doctor":
        print('''
              \t\t\t\t\t➡ Navigating to Doctor menu...
              \t\t\t\t\t-------------------------------\t\t''')
    elif role == "receptionist":
        print('''
              \t\t\t\t\t➡ Navigating to Receptionist menu...
              \t\t\t\t\t------------------------------------\t\t''')
    elif role == "lab technician":
        print('''
              \t\t\t\t\t➡ Navigating to Lab Technician menu...
              \t\t\t\t\t-------------------------------------\t\t''')
        #lab_menu()
    elif role == "pharmacist":
        print('''
              \t\t\t\t\t➡ Navigating to Pharmacist menu...
              \t\t\t\t\t----------------------------------\t\t''')
        run_pharma_menu()
    else:
        print("Unknown role, exiting...")


# ---------- Main ----------
def main():
    first_time_setup()
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        validate_login(username, password)
    except ValueError as ve:
        print("Input validation error:", ve)
        return

    user = login(username, password)
    if user:
        navigate(user)


if __name__ == "__main__":
    main()
