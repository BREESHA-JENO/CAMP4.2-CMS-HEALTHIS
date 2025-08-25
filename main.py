from db.db_connection import DBConnection
from lib.pharmacist_lib.PharmaManagementLib import PharmacistLib
from models.pharmacist import Pharmacist

def menu():
    print("\nPHARMACIST MODULE")
    print("1. Add Medicine")
    print("2. List Medicines")
    print("3. Search Medicine")
    print("4. View Medicine")
    print("5. Edit Medicine")
    print("6. Disable Medicine")
    print("7. Update Stock")
    print("8. Update Price")
    print("9. Fetch Medicine (decrease stock)")
    print("0. Exit")

if __name__ == "__main__":
    __ini
    while True:
        menu()
        choice = input("Enter choice: ")
        if choice == "1":
            name = input("Name: ")
            category = input("Category: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))
            med_id = PharmacistLib.add_medicine(name, category, price, stock)
            print(f"Medicine added with ID {med_id}")

        elif choice == "2":
            meds = PharmacistLib.list_medicines()
            for m in meds:
                print(m)

        elif choice == "3":
            keyword = input("Enter name to search: ")
            meds = PharmacistLib.search_medicine(keyword)
            for m in meds:
                print(m)

        elif choice == "4":
            med_id = input("Enter Medicine ID: ")
            med = PharmacistLib.view_medicine(med_id)
            print(med if med else "Not found")

        elif choice == "5":
            med_id = input("Enter Medicine ID: ")
            med = PharmacistLib.view_medicine(med_id)
            if med:
                name = input(f"New Name ({med.name}): ") or med.name
                category = input(f"New Category ({med.category}): ") or med.category
                price = input(f"New Price ({med.price}): ")
                stock = input(f"New Stock ({med.stock_qty}): ")
                med.name = name
                med.category = category
                med.price = float(price) if price else med.price
                med.stock_qty = int(stock) if stock else med.stock_qty
                PharmacistLib.update_medicine(med)
                print("Updated successfully")
            else:
                print("Not found")

        elif choice == "6":
            med_id = input("Enter Medicine ID: ")
            PharmacistLib.disable_medicine(med_id)
            print("Medicine disabled")

        elif choice == "7":
            med_id = input("Enter Medicine ID: ")
            delta = int(input("Enter stock change (+/-): "))
            success, new_qty = PharmacistLib.update_stock(med_id, delta)
            print("Updated" if success else "Failed")

        elif choice == "8":
            med_id = input("Enter Medicine ID: ")
            new_price = float(input("Enter new price: "))
            PharmacistLib.update_price(med_id, new_price)
            print("Price updated")

        elif choice == "9":
            med_id = input("Enter Medicine ID: ")
            result = PharmacistLib.fetch_medicine(med_id)
            print(result)

        elif choice == "0":
            break
        else:
            print("Invalid choice")
