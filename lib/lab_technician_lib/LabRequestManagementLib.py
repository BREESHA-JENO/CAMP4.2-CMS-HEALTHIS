from dao.lab_technician.LabRequestDaoImple import LabRequestDaoImplementation
from dao.lab_technician.abstractLab_requestDao import LabRequestDaoService
from models.lab_technician_models.lab_request import LabRequest
from models.lab_technician_models.lab_test import LabTest
from datetime import date

class LabRequestManagementLib:
    """Handles logic for Lab Requests"""

    dao_service: LabRequestDaoService = LabRequestDaoImplementation()

    @staticmethod
    def display_all():
        requests = LabRequestManagementLib.dao_service.display_all_requests()
        for req in requests:
            print(req)

    @staticmethod
    def add_request():
        req = LabRequest()
        req.set_doctor_id(int(input("Enter Doctor ID: ")))
        req.set_patient_id(int(input("Enter Patient ID: ")))
        req.set_request_date(date.today())
        notes = input("Enter Clinical Notes: ")
        req.set_clinical_notes(notes)

        # add tests interactively
        while True:
            tid = input("Enter Test ID to add (blank to stop): ")
            if not tid:
                break
            test = LabTest(test_id=int(tid), test_name="")  # minimal info, DAO should fill later
            req.add_test(test)

        if LabRequestManagementLib.dao_service.insert_request(req):
            print("Lab request inserted successfully...")
        else:
            print("Something went wrong...")

    @staticmethod
    def update_status():
        rid = int(input("Enter Request ID: "))
        req = LabRequestManagementLib.dao_service.find_by_request_id(rid)
        if not req:
            print("Request not found")
            return
        print(req)
        new_status = input("Enter new Status (NEW/SENT/IN_PROGRESS/COMPLETED/CANCELLED): ")
        req.set_status(new_status)
        if LabRequestManagementLib.dao_service.update_request(req, rid):
            print("Status updated successfully...")
        else:
            print("Something went wrong...")
