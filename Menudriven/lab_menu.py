# ================== IMPORTS ==================
from lib.lab_technician_lib.LabTestManagementLib import LabTestManagementLib
from lib.lab_technician_lib.LabResultManagementLib import LabResultManagementLib
from lib.lab_technician_lib.LabRequestManagementLib import LabRequestManagementLib
from lib.lab_technician_lib.BillingManagementLib import BillingManagementLib

from dao.lab_technician.LabTestDaoImple import LabTestDaoImplementation
from dao.lab_technician.AbstractLab_testDao import LabTestDaoService

from dao.lab_technician.LabResultDaoImple import LabResultDaoImplementation
from dao.lab_technician.abstractLab_resultDao import LabResultDaoService

from dao.lab_technician.BillingDaoImple import BillingDaoImplementation
from dao.lab_technician.abstractlab_billDao import BillingDaoService

from db.db_connection import DBConnection


# ================== MAIN DASHBOARD ==================
def main():
    while True:
        print("\n======= MAIN DASHBOARD =======")
        print("1. LAB TEST MANAGEMENT")
        print("2. LAB RESULT MANAGEMENT")
        print("3. LAB REQUEST MANAGEMENT")
        print("4. LAB BILLING MANAGEMENT")
        print("5. EXIT")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input, please enter a number (1-5)")
            continue

        # ================== LAB TEST ==================
        if choice == 1:
            while True:
                print("\n======= LAB TEST MANAGEMENT MENU ======")
                print("1. ADD LAB TEST")
                print("2. DISPLAY ALL LAB TEST")
                print("3. UPDATE LAB TEST")
                print("4. SEARCH LAB TEST BY ID")
                print("5. DISABLE LAB TEST")
                print("6. BACK TO MAIN MENU")

                try:
                    sub_choice = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid input, please enter a number (1-6)")
                    continue

                if sub_choice == 1:
                    LabTestManagementLib.add_lab_test()
                elif sub_choice == 2:
                    LabTestManagementLib.display_all()
                elif sub_choice == 3:
                    LabTestManagementLib.update_lab_test()
                elif sub_choice == 4:
                    LabTestManagementLib.search_by_id()
                elif sub_choice == 5:
                    LabTestManagementLib.disable_lab_test()
                elif sub_choice == 6:
                    break
                else:
                    print("Invalid choice, try again!")

        # ================== LAB RESULT ==================
        elif choice == 2:
            while True:
                print("\n======= LAB RESULT MANAGEMENT MENU ======")
                print("1. ADD LAB RESULT")
                print("2. DISPLAY ALL LAB RESULTS")
                print("3. UPDATE LAB RESULT")
                print("4. SEARCH LAB RESULT BY ID")
                print("5. DISABLE LAB RESULT")
                print("6. BACK TO MAIN MENU")

                try:
                    sub_choice = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid input, please enter a number (1-6)")
                    continue

                if sub_choice == 1:
                    LabResultManagementLib.add_result()
                elif sub_choice == 2:
                    LabResultManagementLib.display_all()
                elif sub_choice == 3:
                    LabResultManagementLib.update_result()
                elif sub_choice == 4:
                    LabResultManagementLib.search_by_id()
                elif sub_choice == 5:
                    LabResultManagementLib.disable_lab_result()
                elif sub_choice == 6:
                    break
                else:
                    print("Invalid choice, try again!")

        # ================== LAB REQUEST ==================
        elif choice == 3:
            while True:
                print("\n======= LAB REQUEST MANAGEMENT MENU ======")
                print("1. ADD LAB REQUEST")
                print("2. DISPLAY ALL LAB REQUESTS")
                print("3. UPDATE LAB REQUEST STATUS")
                print("4. BACK TO MAIN MENU")

                try:
                    sub_choice = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid input, please enter a number (1-4)")
                    continue

                if sub_choice == 1:
                    LabRequestManagementLib.add_request()
                elif sub_choice == 2:
                    LabRequestManagementLib.display_all()
                elif sub_choice == 3:
                    LabRequestManagementLib.update_status()
                elif sub_choice == 4:
                    break
                else:
                    print("Invalid choice, try again!")

        # ================== LAB BILL ==================
        elif choice == 4:
            while True:
                print("\n======= BILLING MANAGEMENT MENU ======")
                print("1. ADD BILL")
                print("2. DISPLAY ALL BILLS")
                print("3. BACK TO MAIN MENU")

                try:
                    sub_choice = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid input, please enter a number (1-3)")
                    continue

                if sub_choice == 1:
                    BillingManagementLib.add_bill()
                elif sub_choice == 2:
                    BillingManagementLib.display_all()
                elif sub_choice == 3:
                    break
                else:
                    print("Invalid choice, try again!")

        # ================== EXIT APP ==================
        elif choice == 5:
            print("Exiting Application... Goodbye!")
            break
        else:
            print("Invalid choice, try again!")


if __name__ == "__main__":
    main()
