from lib.doctor_lib.DoctorManagementLib import DoctorManagementLib
from datetime import datetime
def validate_date(input_date):
    try:
        dt = datetime.strptime(input_date, "%Y-%m-%d")
        return dt
    except ValueError:
        return None

def doctor_menu():
    
    while True:
        print("\n===== Doctor Dashboard =====")
        print("1. View today's appointments")
        print("2. View appointments by date")
        print("3. Consult patient")
        print("4. Prescribe medicine")
        print("5. Prescribe lab test")
        print("6. View patient consultation history")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            while True:
                staff_id = input("Enter your Staff ID: ").strip().upper()
                if DoctorManagementLib.validate_staff(staff_id):
                    break
                print("Invalid Staff ID. Try again.")
            DoctorManagementLib.display_all(staff_id)

        elif choice == "2":
            while True:
                staff_id = input("Enter your Staff ID: ").strip().upper()
                if DoctorManagementLib.validate_staff(staff_id):
                    break
                print("Invalid Staff ID. Try again.")
            date = input("Enter date (YYYY/MM/DD): ").strip()
            if not validate_date(date):
                print("Invalid date format. Use YYYY-MM-DD.")
                continue
            DoctorManagementLib.display_all_date(staff_id, date)

        elif choice == "3":  # Consult patient
            while True:
                staff_id = input("Enter your Staff ID: ").strip().upper()
                if DoctorManagementLib.validate_staff(staff_id):
                    break
                print("Invalid Staff ID. Try again.")

            while True:
                appointment_id = input("Enter Appointment ID: ").strip().upper()
                if DoctorManagementLib.validate_appointment(staff_id, appointment_id):
                    break
                print("Invalid Appointment ID. Try again.")

            symptoms = input("Enter Symptoms: ").strip()
            diagnosis = input("Enter Diagnosis: ").strip()
            notes = input("Enter Notes: ").strip()

            DoctorManagementLib.consult_patient(appointment_id, staff_id, symptoms, diagnosis, notes)

        elif choice == "4":  # Prescribe medicines
            while True:
                consultation_id = input("Enter Consultation ID: ").strip().upper()
                if DoctorManagementLib.validate_consultation(consultation_id):
                    break
                print("Invalid Consultation ID. Try again.")

            medicines = []
            while True:
                med_id = input("Enter Medicine ID (or 'done' to finish): ").strip().upper()
                if med_id.lower() == "done":
                    break
                if not DoctorManagementLib.validate_medicine(med_id):
                    print("Invalid Medicine ID. Try again.")
                    continue
                if DoctorManagementLib.check_duplicate_medicine(consultation_id, med_id):
                        print("Medicine already prescribed for this consultation.")
                        continue
                dosage = input("Enter Dosage: ").strip()
                duration = input("Enter Duration: ").strip()
                medicines.append({"medicine_id": med_id, "dosage": dosage, "duration": duration})

            if medicines:
                DoctorManagementLib.prescribe_medicines(consultation_id, medicines)
            
        elif choice == "5":  # Prescribe lab tests
            while True:
                consultation_id = input("Enter Consultation ID: ").strip().upper()
                if DoctorManagementLib.validate_consultation(consultation_id):
                    break
                print("Invalid Consultation ID. Try again.")

            lab_tests = []
            while True:
                lab_id = input("Enter Lab Test ID (or 'done' to finish): ").strip().upper()
                if lab_id.lower() == "done":
                    break
                if not DoctorManagementLib.validate_lab_test(lab_id):
                    print("Invalid Lab Test ID. Try again.")
                    continue
                if DoctorManagementLib.check_duplicate_lab(consultation_id, lab_id):
                    print("Lab test already prescribed for this consultation.")
                    continue
                test_name = input("Enter Lab Test Name: ").strip()
                description = input("Enter Description / Notes: ").strip()
                lab_tests.append({"lab_test_id": lab_id, "test_name": test_name, "description": description})

            if lab_tests:
                DoctorManagementLib.prescribe_lab_tests(consultation_id, lab_tests)
            
        elif choice == "6":  # View patient history
            while True:
                patient_id = input("Enter Patient ID: ").strip().upper()
                if DoctorManagementLib.validate_patient(patient_id):
                    break
                print("Invalid Patient ID. Try again.")
            DoctorManagementLib.view_patient_history(patient_id)

        elif choice == "0":
            print("Exiting Doctor Dashboard...")
            break

        else:
            print("Invalid choice! Try again.")
