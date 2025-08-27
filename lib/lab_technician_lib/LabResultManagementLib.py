from dao.lab_technician.LabResultDaoImple import LabResultDaoImplementation
from dao.lab_technician.abstractLab_resultDao import LabResultDaoService
from models.lab_technician_models.lab_result import LabResult
from datetime import date

class LabResultManagementLib:
    """Handles logic for Lab Results"""

    dao_service: LabResultDaoService = LabResultDaoImplementation()

    @staticmethod
    def display_all():
        results = LabResultManagementLib.dao_service.display_all_results()
        for result in results:
            print(result)

    @staticmethod
    def add_result():
        res = LabResult()
        res.set_lab_request_id(int(input("Enter Request ID: ")))
        res.set_lab_test_id(int(input("Enter Test ID: ")))
        res.set_staff_id(int(input("Enter Technician ID: ")))
        res.set_result_value(input("Enter Result Value: "))
        res.set_normal_range(input("Enter Normal Range: "))
        res.set_remarks("Enter the remarks")
        res.set_created_at(date.today())

        if LabResultManagementLib.dao_service.insert_result(res):
            print("Result inserted successfully...")
        else:
            print("Something went wrong...")

    @staticmethod
    def verify_result():
        rid = int(input("Enter Result ID: "))
        result = LabResultManagementLib.dao_service.find_by_result_id(rid)
        if not result:
            print("Result not found")
            return
        print(result)
        confirm = input("Mark this result as VERIFIED? (y/n): ")
        if confirm.lower() == "y":
            result.set_verification_status("VERIFIED")
            if LabResultManagementLib.dao_service.update_result(result, rid):
                print("Result verified successfully...")
            else:
                print("Something went wrong...")
