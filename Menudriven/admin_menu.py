from lib.admin_lib.AdminManagementLib import StaffManagementLib

def admin_menu():
    while True:
        print("\n===== Admin Menu =====")
        print("1. Add Staff")
        print("2. View All Staff")
        print("3. Search Staff by ID")
        print("4. Update Staff")
        print("5. Disable Staff")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            StaffManagementLib.add_staff()

        elif choice == "2":
            StaffManagementLib.display_all()

        elif choice == "3":
            staff_id = input("Enter Staff ID to search: ")
            staff = StaffManagementLib.dao_service.find_by_staff_id(staff_id)  
            if staff:
                print(staff)
            else:
                print("Staff not found!")

        elif choice == "4":
            staff_id = input("Enter Staff ID to update: ")
            StaffManagementLib.update_staff(staff_id)  # Preferred to route logic through lib!

        elif choice == "5":
            staff_id = input("Enter Staff ID to disable: ")
            StaffManagementLib.disable_staff(staff_id)  # Preferred!

        elif choice == "6":
            print("Exiting Admin Menu...")
            break

        else:
            print("Invalid choice! Please try again.")