# import pymysql
# from db.db_connection import DBConnection
# from Menudriven.admin_menu import admin_menu
# import bcrypt
# from Menudriven.pharma_menu import run_pharma_menu
# from validation.admin_val.user_validation import validate_login



# # ---------- First Time Setup ----------
# def first_time_setup():
#     conn = DBConnection().get_connection()
#     cursor = conn.cursor()

#     # Insert all required roles if not present
#     cursor.execute("""
#         INSERT INTO Roles (role_id, role_name) VALUES
#         (1, 'Admin'),
#         (2, 'Receptionist'),
#         (3, 'Doctor'),
#         (4, 'Lab Technician'),
#         (5, 'Pharmacist')
#         ON DUPLICATE KEY UPDATE role_name = VALUES(role_name)
#     """)

#     # Rest of your existing first_time_setup code for super admin creation...
#     cursor.execute("SELECT COUNT(*) FROM user_credentials")
#     count = cursor.fetchone()[0]

#     if count == 0:
#         print("⚠ No users found. Creating Super Admin...")
#         username = input("Enter admin username: ")
#         password = input("Enter admin password: ")

#         hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

#         cursor.execute("""
#             INSERT INTO Staff (staff_id, staff_name, role_id, dob, gender, doj, blood_group, phone, email)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#             ON DUPLICATE KEY UPDATE staff_name='Super Admin'
#         """, ("AD001", "Super Admin", 1, "1980-01-01", "Male", "2025-08-01", "O+", "9999999999", "admin@cliniccare.com"))

#         cursor.execute("""
#             INSERT INTO user_credentials (staff_id, username, password, created_at)
#             VALUES (%s, %s, %s, NOW())
#             ON DUPLICATE KEY UPDATE username=%s, password=%s
#         """, ("AD001", username, hashed_password, username, hashed_password))

#         conn.commit()
#         print("Super Admin created successfully")

#     cursor.close()


# # ---------- Login Function ----------
# def login(username, password):
#     db = DBConnection()
#     conn = db.get_connection()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)  # Dict-like results

#     cursor.execute("""
#         SELECT u.staff_id, u.password, s.role_id, r.role_name 
#         FROM user_credentials u
#         JOIN Staff s ON u.staff_id = s.staff_id
#         JOIN Roles r ON s.role_id = r.role_id
#         WHERE u.username=%s
#     """, (username,))

#     user = cursor.fetchone()
#     cursor.close()
#     # Do NOT close the singleton connection here either

#     if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
#         print(f"Login successful! Role: {user['role_name']}")
#         return user
#     else:
#         print("Invalid credentials")
#         return None


# # ---------- Navigation ----------
# def navigate(user):
#     role = user["role_name"].lower()
#     if role == "admin":
#         print("➡ Navigating to Admin menu...")
#         admin_menu()
#     elif role == "doctor":
#         print("➡ Navigating to Doctor menu...")
#     elif role == "receptionist":
#         print("➡ Navigating to Receptionist menu...")
#     elif role == "lab technician":
#         print("➡ Navigating to Lab Technician menu...")
#     elif role == "pharmacist":
#         print("➡ Navigating to Pharmacist menu...")
#         run_pharma_menu()
#     else:
#         print("Unknown role, exiting...")


# # ---------- Main ----------
# def main():
#     first_time_setup()
    
#     username = input("Enter username: ")
#     password = input("Enter password: ")

#     try:
#         validate_login(username, password)
#     except ValueError as ve:
#         print("Input validation error:", ve)
#         return  # Or loop back to re-prompt if you want

#     user = login(username, password)
#     if user:
#         navigate(user)


# if __name__ == "__main__":
#     main()
