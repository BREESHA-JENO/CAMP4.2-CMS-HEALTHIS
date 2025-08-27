from dao.doctor.AbstractDoctorDao import DoctorDaoService
from db.db_connection import DBConnection
from models.doctor_models.doctor import Doctor
from typing import List
from pymysql.cursors import DictCursor
class DoctorDaoImplementation(DoctorDaoService):
    view_appointments='select * from appointments where staff_id=%s'

    
    
    def _init_(self):
        self.conn=DBConnection().get_connection()

    def view_all_appointments(self):
        try:
            appointments=[]
            cursor=self.conn.cursor()
            cursor.execute(self.view_appointments)
            rows=cursor.fetchall()
            for row in rows:
                appointments.append(appointments(appointment_id=row['appointment_id'],
                                                patient_id=row['patient_id'],
                                                staff_id=row['staff_id'],
                                                date=row['date'],
                                                time=row['time'],
                                                isActive=row['isActive'],                    
                                                created_date=row['created_date']))           
        except Exception as e:
            print('error while displaying appointments ',e)
        finally:
            cursor.close()
        return appointments
            

    