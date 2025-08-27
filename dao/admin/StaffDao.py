from db.db_connection import DBConnection
from dao.admin.AbstractAdminDao import AdminDaoService
from models.admin_models.staff import Staff
from typing import List
from pymysql.cursors import DictCursor


class StaffDAO(AdminDaoService):
    'Implementation of abstract class AdminDaoService'

    ADD_STAFF = """
        INSERT INTO Staff (staff_id, staff_name, dob, gender, doj, blood_group, phone, email, address, role_id, isActive) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    DISPLAY_ALL = "SELECT * FROM Staff WHERE isActive = 'Y'"

    FIND_BY_ID = "SELECT * FROM Staff WHERE staff_id=%s"

    UPDATE_STAFF = """
    UPDATE Staff
    SET staff_name=%s, dob=%s, gender=%s, doj=%s, blood_group=%s, phone=%s,
        email=%s, address=%s, role_id=%s, isActive=%s
    WHERE staff_id=%s
"""

    DISABLE_STAFF = "UPDATE Staff SET isActive='N' WHERE staff_id=%s"


    def __init__(self):
        self.conn = DBConnection().get_connection()

    def generate_staff_id(self, role_name: str) -> str:
        try:
            cursor = self.conn.cursor()
            cursor.callproc('generate_staff_id', (role_name, '@new_id'))
            cursor.execute("SELECT @new_id")
            new_id = cursor.fetchone()[0]
            print(f"DEBUG generate_staff_id returned: {new_id}")
            return new_id
        except Exception as e:
            print("Error calling stored procedure generate_staff_id:", e)
            return None
        finally:
            cursor.close()


    def add_staff(self, staff: Staff) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.ADD_STAFF, (
                staff.staff_id,
                staff.staff_name,
                staff.dob,
                staff.gender,
                staff.doj,
                staff.blood_group,
                staff.phone,
                staff.email,
                staff.address,
                staff.role_id,
                staff.isActive
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error adding the staff:", e)
            return False
        finally:
            cursor.close()

    def view_all_staff(self) -> List[Staff]:
        staffs = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                staffs.append(Staff(
                    staff_id=row["staff_id"],
                    staff_name=row["staff_name"],
                    dob=row["dob"],
                    gender=row["gender"],
                    doj=row["doj"],
                    blood_group=row["blood_group"],
                    phone=row["phone"],
                    email=row["email"],
                    address=row["address"],
                    role_id=row["role_id"],
                    isActive=row["isActive"]
                ))
        except Exception as e:
            print("Error fetching staff details:", e)
        finally:
            cursor.close()
        return staffs

    def find_by_staff_id(self, staff_id: str):
        staff = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_ID, (staff_id,))
            row = cursor.fetchone()
            if row:
                staff = Staff(
                    staff_id=row["staff_id"],
                    staff_name=row["staff_name"],
                    dob=row["dob"],
                    gender=row["gender"],
                    doj=row["doj"],
                    blood_group=row["blood_group"],
                    phone=row["phone"],
                    email=row["email"],
                    address=row["address"],
                    role_id=row["role_id"],
                    isActive=row["isActive"]
                )
        except Exception as e:
            print("Error fetching staff:", e)
        finally:
            cursor.close()
        return staff

    
    def update_staff(self, staff: Staff) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.UPDATE_STAFF, (
                staff.staff_name,
                staff.dob,
                staff.gender,
                staff.doj,
                staff.blood_group,
                staff.phone,
                staff.email,
                staff.address,
                staff.role_id,
                staff.isActive,
                staff.staff_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating staff:", e)
            return False
        finally:
            cursor.close()

    def disable_staff(self, staff_id: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.DISABLE_STAFF, (staff_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error disabling staff:", e)
            return False
        finally:
            cursor.close()
