from db.db_connection import DBConnection
from models.admin_models.doctor_details import Doctor_details

class DoctorDAO:
    ADD_DOCTOR = """
        INSERT INTO doctor_details (staff_id, specialization, consultation_fee, working_days, working_hours)
        VALUES (%s, %s, %s, %s, %s)
    """

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_doctor(self, doctor: Doctor_details) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.ADD_DOCTOR, (
                doctor.staff_id,
                doctor.specialization,
                doctor.consultation_fee,
                doctor.working_days,
                doctor.working_hours
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error adding doctor details:", e)
            return False
        finally:
            cursor.close()
