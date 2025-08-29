from dao.doctor.AbstractDoctorDao import DoctorDaoService
from db.db_connection import DBConnection
from models.doctor_models.doctor import Doctor
from models.doctor_models.appointment import Appointment
from pymysql.cursors import DictCursor

class DoctorDaoImplementation(DoctorDaoService):

    view_appointments = "SELECT appointment_id, staff_id, patient_id, date, time, status, created_at FROM appointments WHERE staff_id=%s AND date=CURDATE()"
    view_appointments_date = "SELECT appointment_id, staff_id, patient_id, date, time, status, created_at FROM appointments WHERE staff_id=%s AND date=%s"
    check_app_id = "SELECT patient_id FROM appointments WHERE appointment_id=%s"
    add_cons = """INSERT INTO consultation_notes (consultation_id, appointment_id, patient_id, staff_id, symptoms, diagnosis, notes, created_at)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())"""
    update_app_status = "UPDATE appointments SET status='Completed' WHERE appointment_id=%s"

    p_med = """INSERT INTO Prescriptions (consultation_id, patient_id, medicine_id, dosage, duration, created_at)
               VALUES (%s, %s, %s, %s, %s, NOW())"""
    
    p_lab = """INSERT INTO lab_test_doc (consultation_id, lab_test_id, test_name, status, description)
               VALUES (%s, %s, %s, 'Requested', %s)"""

    history_consult = """SELECT c.consultation_id, c.appointment_id, c.staff_id, c.symptoms, c.diagnosis, c.notes, c.created_at
                         FROM consultation_notes c
                         JOIN appointments a ON c.appointment_id = a.appointment_id
                         WHERE a.patient_id=%s
                         ORDER BY c.created_at DESC"""

    query_prescriptions = """SELECT p.prescription_id, m.medicine_name, p.dosage, p.duration
                             FROM Prescriptions p
                             JOIN Medicines m ON p.medicine_id = m.medicine_id
                             WHERE p.consultation_id=%s"""

    query_lab = """SELECT test_id_doc, lab_test_id, test_name, status, description
                   FROM lab_test_doc
                   WHERE consultation_id=%s"""

    def __init__(self):
        self.conn = DBConnection().get_connection()
        
        
        
        
        
    

    # ------------------ Appointments ------------------
    def view_all_appointments(self, staff_id):
        appointments = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.view_appointments, (staff_id,))
            rows = cursor.fetchall()
            for row in rows:
                appointments.append(Appointment(**row))
        except Exception as e:
            print("Error while displaying appointments:", e)
        finally:
            cursor.close()
        return appointments

    def view_all_appointments_date(self, staff_id, date):
        appointments = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.view_appointments_date, (staff_id, date))
            rows = cursor.fetchall()
            for row in rows:
                appointments.append(Appointment(**row))
        except Exception as e:
            print("Error while displaying appointments:", e)
        finally:
            cursor.close()
        return appointments

    # ------------------ Consultation ------------------
    def insert_consultation(self, appointment_id, patient_id, staff_id, symptoms, diagnosis, notes):
        try:
            cursor = self.conn.cursor()

            # Get patient_id if not provided
            if not patient_id:
                cursor.execute(self.check_app_id, (appointment_id,))
                result = cursor.fetchone()
                if result:
                    patient_id = result['patient_id']
                else:
                    print(f"No appointment found with ID {appointment_id}.")
                    return None

            # Generate consultation_id
            cursor.callproc('generate_consultation_id', [None])
            cursor.execute("SELECT @_generate_consultation_id_0")
            consultation_id = cursor.fetchone()[0]

            # Insert consultation
            cursor.execute(self.add_cons, (consultation_id, appointment_id, patient_id, staff_id, symptoms, diagnosis, notes))
            
            # Mark appointment completed
            cursor.execute(self.update_app_status, (appointment_id,))

            self.conn.commit()
            return consultation_id

        except Exception as e:
            print("Error inserting consultation:", e)
            self.conn.rollback()
            return None
        finally:
            cursor.close()

    # ------------------ Medicines ------------------
    def prescribe_medicine(self, consultation_id, medicine_id, dosage, duration):
        """Keep single medicine method to satisfy abstract class."""
        return self.prescribe_medicines(consultation_id, [{"medicine_id": medicine_id, "dosage": dosage, "duration": duration}])

    def prescribe_medicines(self, consultation_id, medicines: list):
        """Accept multiple medicines as list of dicts"""
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT patient_id FROM consultation_notes WHERE consultation_id=%s", (consultation_id,))
            result = cursor.fetchone()
            if not result:
                print(f"No consultation found with ID {consultation_id}")
                return False
            patient_id = result['patient_id']

            for med in medicines:
                cursor.execute(self.p_med, (consultation_id, patient_id, med['medicine_id'], med['dosage'], med['duration']))
            
            self.conn.commit()
            return True
        except Exception as e:
            print("Error prescribing medicines:", e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    # ------------------ Lab Tests ------------------
    def prescribe_lab_test(self, consultation_id, lab_test_id, test_name, description=""):
        return self.prescribe_lab_tests(consultation_id, [{"lab_test_id": lab_test_id, "test_name": test_name, "description": description}])

    def prescribe_lab_tests(self, consultation_id, lab_tests: list):
        """Accept multiple lab tests as list of dicts"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT consultation_id FROM consultation_notes WHERE consultation_id=%s", (consultation_id,))
            if not cursor.fetchone():
                print(f"No consultation found with ID {consultation_id}")
                return False

            for test in lab_tests:
                cursor.execute(self.p_lab, (consultation_id, test['lab_test_id'], test['test_name'], test['description']))
            
            self.conn.commit()
            return True
        except Exception as e:
            print("Error prescribing lab tests:", e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    # ------------------ History ------------------
    def get_consultation_history(self, patient_id):
        history = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.history_consult, (patient_id,))
            consultations = cursor.fetchall()

            for consult in consultations:
                consult_id = consult['consultation_id']
                cursor.execute(self.query_prescriptions, (consult_id,))
                prescriptions = cursor.fetchall()
                cursor.execute(self.query_lab, (consult_id,))
                labs = cursor.fetchall()

                history.append({
                    "consultation": Doctor(
                        cons_id=consult['consultation_id'],
                        appointment_id=consult['appointment_id'],
                        staff_id=consult['staff_id'],
                        symptoms=consult['symptoms'],
                        diagnosis=consult['diagnosis'],
                        notes=consult['notes'],
                        created_at=consult['created_at']
                    ),
                    "prescriptions": prescriptions,
                    "lab_tests": labs
                })
        except Exception as e:
            print("Error fetching consultation history:", e)
        finally:
            cursor.close()
        return history
    
    
    # ------------------ Validation Methods ------------------
    # Staff validation
    def staff_exists(self, staff_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT staff_id FROM Staff WHERE staff_id=%s", (staff_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    # Patient validation
    def patient_exists(self, patient_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT patient_id FROM PatientS WHERE patient_id=%s", (patient_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    # Appointment validation (check status != 'Completed')
    def appointment_exists(self, appointment_id, staff_id):
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("""
                SELECT status 
                FROM Appointments 
                WHERE LOWER(TRIM(appointment_id)) = LOWER(TRIM(%s))
                  AND LOWER(TRIM(staff_id)) = LOWER(TRIM(%s))
            """, (appointment_id, staff_id))
            row = cursor.fetchone()
            if not row:
                return False
            # reject if appointment already completed
            return row['status'] != 'Completed'
        finally:
            cursor.close()

    # Consultation validation
    def consultation_exists(self, consultation_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT consultation_id FROM consultation_notes WHERE consultation_id=%s", (consultation_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    # Medicine validation
    def medicine_exists(self, med_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT medicine_id FROM Medicines WHERE medicine_id=%s", (med_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    # Lab test validation
    def lab_test_exists(self, lab_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT lab_test_id FROM lab_test_master WHERE lab_test_id=%s", (lab_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    # Duplicate medicine check
    def duplicate_medicine(self, consultation_id, med_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT prescription_id FROM Prescriptions WHERE consultation_id=%s AND medicine_id=%s", (consultation_id, med_id))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    # Duplicate lab test check
    def duplicate_lab(self, consultation_id, lab_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT test_id_doc FROM lab_test_doc WHERE consultation_id=%s AND lab_test_id=%s", (consultation_id, lab_id))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
