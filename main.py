from lib.pharmacist_lib.PharmaManagementLib import PharmaManagementLib

def main():
    while True:
        print("\n--- Pharmacist Menu ---")
        print("1. Add Medicine")
        print("2. List Medicines")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter medicine name: ")
            category = input("Enter category: ")
            price = float(input("Enter price: "))
            stock = int(input("Enter stock quantity: "))

            med = PharmaManagementLib.add_medicine(name, category, price, stock)
            print(f"✅ Medicine Added: {med}")

        elif choice == "2":
            medicines = PharmaManagementLib.list_medicines()
            if medicines:
                print("\n--- Medicine List ---")
                for m in medicines:
                    print(m)
            else:
                print("No medicines found.")

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
