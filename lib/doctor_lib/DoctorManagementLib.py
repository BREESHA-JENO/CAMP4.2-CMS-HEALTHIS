# lib/doctor/DoctorManagementLib.py

from dao.doctor.DoctorDaoImplementation import DoctorDaoImplementation
from dao.doctor.AbstractDoctorDao import DoctorDaoService
from models.doctor_models.doctor import Doctor
from models.doctor_models.appointment import Appointment

class DoctorManagementLib:
    """Handles CRUD logic for doctor module"""

    dao_service: DoctorDaoService = DoctorDaoImplementation()
    
    # -------------------- Validation Methods --------------------
    @staticmethod
    def validate_staff(staff_id):
        return DoctorManagementLib.dao_service.staff_exists(staff_id)

    @staticmethod
    def validate_appointment(staff_id, appointment_id):
        return DoctorManagementLib.dao_service.appointment_exists(appointment_id, staff_id)

    @staticmethod
    def validate_consultation(consultation_id):
        return DoctorManagementLib.dao_service.consultation_exists(consultation_id)

    @staticmethod
    def validate_medicine(medicine_id):
        return DoctorManagementLib.dao_service.medicine_exists(medicine_id)

    @staticmethod
    def validate_lab_test(lab_test_id):
        return DoctorManagementLib.dao_service.lab_test_exists(lab_test_id)

    @staticmethod
    def validate_patient(patient_id):
        return DoctorManagementLib.dao_service.patient_exists(patient_id)
    
    @staticmethod
    def check_duplicate_medicine(consultation_id, med_id):
        return DoctorManagementLib.dao_service.duplicate_medicine(consultation_id, med_id)

    @staticmethod
    def check_duplicate_lab(consultation_id, lab_id):
        return DoctorManagementLib.dao_service.duplicate_lab(consultation_id, lab_id)
    

    # -------------------- Existing Methods --------------------
    
    

    @staticmethod
    def display_all(staff_id):
        appointments = DoctorManagementLib.dao_service.view_all_appointments(staff_id)
        if not appointments:
            print(f"No appointments found for Staff ID {staff_id} today.")
        else:
            print(f"Appointments for Staff ID {staff_id} today:")
            for app in appointments:
                print(app)

    @staticmethod
    def display_all_date(staff_id, date):
        appointments = DoctorManagementLib.dao_service.view_all_appointments_date(staff_id, date)
        if not appointments:
            print(f"No appointments found for Staff ID {staff_id} on {date}.")
        else:
            print(f"Appointments for Staff ID {staff_id} on {date}:")
            for app in appointments:
                print(app)

    @staticmethod
    def consult_patient(appointment_id, staff_id, symptoms, diagnosis, notes):
        # Fetch the appointment first
        appointments = DoctorManagementLib.dao_service.view_all_appointments(staff_id)
        patient_id = None
        for app in appointments:
            if (app.appointment_id) == (appointment_id):  # direct attribute access
                patient_id = app.patient_id
                break


        if patient_id is None:
            print(f"Appointment {appointment_id} not found for Staff ID {staff_id}.")
            return None

        cons_id = DoctorManagementLib.dao_service.insert_consultation(
            appointment_id, patient_id, staff_id, symptoms, diagnosis, notes
        )
        print(f"Consultation saved with ID: {cons_id}")
        return cons_id

    @staticmethod
    def prescribe_medicines(consultation_id, medicines):
        """Accept list of medicines"""
        success = DoctorManagementLib.dao_service.prescribe_medicines(consultation_id, medicines)
        if success:
            print("Medicines prescribed successfully.")
        else:
            print("Failed to prescribe medicines.")

    @staticmethod
    def prescribe_lab_tests(consultation_id, lab_tests):
        success = DoctorManagementLib.dao_service.prescribe_lab_tests(consultation_id, lab_tests)
        if success:
            print("Lab tests prescribed successfully.")
        else:
            print("Failed to prescribe lab tests.")


    @staticmethod
    def view_patient_history(patient_id):
        history = DoctorManagementLib.dao_service.get_consultation_history(patient_id)
        if not history:
            print(f"No consultation history found for patient ID {patient_id}.")
            return

        print(f"===== Consultation History for Patient {patient_id} =====")
        for record in history:
            consult: Doctor = record["consultation"]
            print(f"\nConsultation ID: {consult.cons_id}, "
                  f"Appointment ID: {consult.appointment_id}, "
                  f"Staff ID: {consult.staff_id}, "
                  f"Date: {consult.created_at}, "
                  f"Symptoms: {consult.symptoms}, "
                  f"Diagnosis: {consult.diagnosis}, "
                  f"Notes: {consult.notes}")

            # Prescriptions
            if record["prescriptions"]:
                print("  Prescriptions:")
                for p in record["prescriptions"]:
                    print(f"    - {p['medicine_name']} ({p['dosage']}, {p['duration']})")
            else:
                print("  No prescriptions.")

            # Lab tests
            if record["lab_tests"]:
                print("  Lab Tests:")
                for l in record["lab_tests"]:
                    print(f"    - {l['test_name']} (Status: {l['status']}, notes: {l['description']})")
            else:
                print("  No lab tests.")
