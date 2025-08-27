from dao.lab_technician.LabTestDaoImple import LabTestDaoImplementation
from models.lab_technician_models.lab_test import LabTest


def main():
    dao = LabTestDaoImplementation()

    while True:
        print("\n===== LAB TEST MANAGEMENT =====")
        print("1. Display All Lab Tests")
        print("2. Add New Lab Test")
        print("3. Search Lab Test by ID")
        print("4. Update Lab Test")
        print("5. Delete Lab Test")
        print("6. Exit")

        choice = input("Enter your choice: ")

        # -------------------------------
        if choice == "1":
            tests = dao.display_all_tests()
            for t in tests:
                print(f"Test ID: {t.lab_test_id} | Name: {t.test_name} | "
                      f"Description: {t.description} | Cost: {t.cost}")

        # -------------------------------
        elif choice == "2":
            lab_test_id = input("Enter Lab Test ID (e.g. TS101): ")
            test_name = input("Enter Test Name: ")
            description = input("Enter Description: ")
            cost = float(input("Enter Cost: "))

            new_test = LabTest(
                lab_test_id=lab_test_id,
                test_name=test_name,
                description=description,
                cost=cost
            )

            dao.insert_lab_test(new_test)
            print("✅ Lab test added successfully!")

        # -------------------------------
        elif choice == "3":
            lab_test_id = input("Enter Lab Test ID to search: ")
            test = dao.find_by_id(lab_test_id)
            if test:
                print(f"Test ID: {test.lab_test_id} | Name: {test.test_name} | "
                      f"Description: {test.description} | Cost: {test.cost}")
            else:
                print("⚠️ Lab Test not found.")

        # -------------------------------
        elif choice == "4":
            lab_test_id = input("Enter Lab Test ID to update: ")
            test = dao.find_by_id(lab_test_id)
            if not test:
                print("⚠️ Lab Test not found.")
                continue

            new_name = input(f"Enter new name (leave blank to keep '{test.test_name}'): ")
            new_description = input(f"Enter new description (leave blank to keep '{test.description}'): ")
            new_cost = input(f"Enter new cost (leave blank to keep '{test.cost}'): ")

            if new_name:
                test.test_name = new_name
            if new_description:
                test.description = new_description
            if new_cost:
                test.cost = float(new_cost)

            dao.update_lab_test(test, lab_test_id)
            print("✅ Lab test updated successfully!")

        # -------------------------------
        elif choice == "5":
            lab_test_id = input("Enter Lab Test ID to delete: ")
            dao.delete_lab_test(lab_test_id)
            print("✅ Lab test deleted successfully!")

        # -------------------------------
        elif choice == "6":
            print("👋 Exiting Lab Test Management...")
            break

        else:
            print("❌ Invalid choice. Please try again.")


