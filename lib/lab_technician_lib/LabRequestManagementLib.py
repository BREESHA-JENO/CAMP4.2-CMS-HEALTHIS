from dao.lab_technician.LabRequestDaoImple import LabRequestDaoImplementation
from dao.lab_technician.abstractLab_requestDao import LabRequestDaoService
from models.lab_technician_models.lab_request import LabRequest
from datetime import datetime

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
        req.set_consultation_id(input("Enter Consultation ID: "))
        req.set_patient_id(input("Enter Patient ID: "))
        req.set_test_id_doc(int(input("Enter Test ID: ")))
        req.set_staff_id(input("Enter Staff/Doctor ID: "))
        req.set_status("Completed")
        req.set_created_datetime(datetime.now())

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
