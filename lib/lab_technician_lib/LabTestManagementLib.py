from dao.lab_technician.LabTestDaoImple import LabTestDaoImplementation
from dao.lab_technician.AbstractLab_testDao import LabTestDaoService
from models.lab_technician_models.lab_test import LabTest
from datetime import date

class LabTestManagementLib:
    """Handles CRUD logic for Lab Tests"""

    dao_service: LabTestDaoService = LabTestDaoImplementation()

    @staticmethod
    def display_all():
        tests = LabTestManagementLib.dao_service.display_all_tests()
        for test in tests:
            print(test)

    @staticmethod
    def add_lab_test():
        test = LabTest()
        name = input("Enter Lab Test Name: ")
        test.set_test_name(name)
        price = float(input("Enter Unit Price: "))
        test.set_price(price)
        sample = input("Enter Sample Type (Blood/Urine/etc): ")
        test.set_sampletype(sample)
        test.set_created_at(date.today())

        if LabTestManagementLib.dao_service.insert_test(test):
            print("Test inserted successfully...")
        else:
            print("Something went wrong...")

    @staticmethod
    def update_lab_test():
        tid = (input("Enter Test ID: "))
        test = LabTestManagementLib.dao_service.find_by_test_id(tid)
        if not test:
            print("Test not found")
            return
        print(test)
        confirm = input("Do you want to edit this test? (y/n): ")
        if confirm.lower() == "y":
            test.set_test_name(input("Enter new Test Name: "))
            test.set_price(float(input("Enter new Unit Price: ")))
            test.set_sampletype(input("Enter new Sample Type: "))
            if LabTestManagementLib.dao_service.update_test(test, tid):
                print("Updated successfully...")
            else:
                print("Something went wrong...")

    @staticmethod
    def search_by_id():
        tid = input("Enter Test ID: ")
        test = LabTestManagementLib.dao_service.find_by_test_id(tid)
        if test:
            print("Lab Test Found:")
            print(test)
        else:
            print("No Lab Test found with ID:", tid)


    @staticmethod
    def disable_lab_test():
        tid = (input("Enter Test ID: "))
        test = LabTestManagementLib.dao_service.find_by_test_id(tid)
        if not test:
            print("Test not found")
            return
        print(test)
        confirm = input("Do you want to disable this test? (y/n): ")
        if confirm.lower() == "y":
            if LabTestManagementLib.dao_service.disable_test(test, tid):
                print("Test disabled successfully...")
            else:
                print("Something went wrong...")
