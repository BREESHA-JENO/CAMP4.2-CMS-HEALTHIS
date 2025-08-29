from dao.lab_technician.BillingDaoImple import BillingDaoImplementation
from dao.lab_technician.abstractlab_billDao import BillingDaoService
from models.lab_technician_models.lab_bill import Billing
from datetime import date

class BillingManagementLib:
    """Handles logic for Billing"""

    dao_service: BillingDaoService = BillingDaoImplementation()

    @staticmethod
    def display_all():
        bills = BillingManagementLib.dao_service.display_all_bills()
        for bill in bills:
            print(bill)

    @staticmethod
    def add_bill():
        bill = Billing()
        bill.set_patient_id((input("Enter Patient ID: ")))
        bill.set_lab_test_id(input("Enter Lab Test ID: "))   # <-- NEW
        bill.set_total_amount(float(input("Enter Total Amount: ")))  # <-- NEW
        bill.set_status("Paid")  # default
        bill.set_created_at(date.today())

        if BillingManagementLib.dao_service.insert_bill(bill):
          print("Bill inserted successfully...")
        else:
         print("Something went wrong...")


    @staticmethod
    def mark_paid():
        bid = int(input("Enter Bill ID: "))
        bill = BillingManagementLib.dao_service.find_by_bill_id(bid)
        if not bill:
            print("Bill not found")
            return
        print(bill)
        confirm = input("Mark this bill as PAID? (y/n): ")
        if confirm.lower() == "y":
            bill.set_status(True)
            if BillingManagementLib.dao_service.update_bill(bill, bid):
                print("Bill updated successfully...")
            else:
                print("Something went wrong...")
