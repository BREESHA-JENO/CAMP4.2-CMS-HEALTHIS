from lib.pharmacist_lib.PharmaManagementLib import PharmaManagementLib

def run_pharma_menu():
    svc = PharmaManagementLib()
    while True:
        print("\n=== Pharmacist Menu ===")
        print("1) Add Stock")
        print("2) List Stock")
        print("3) Add Medicine FROM Stock")
        print("4) List Medicines")
        print("5) Search & View Medicine")
        print("6) Exit")
        ch = input("Choose: ").strip()

        if ch == "1":
            name = input("Medicine name: ").strip()
            rcv = input("Received date (YYYY-MM-DD): ").strip()
            exp = input("Expiry date (YYYY-MM-DD): ").strip()
            qty = int(input("Quantity: "))
            ok, med_id_or_msg = svc.add_stock(name, rcv, exp, qty)
            if ok:
                print(f"Stock added. Medicine ID: {med_id_or_msg}")
            else:
                print(f"Error: {med_id_or_msg}")

        elif ch == "2":
            stock_table = svc.list_stock()
            print(stock_table)

        elif ch == "3":
            med_id = input("Enter Medicine ID to move from stock: ").strip()
            name = input("Medicine name (for doctor view): ").strip()
            gen_name=input("Medicine generic name: ").strip()
            qty = int(input("Quantity: "))
            price = float(input("Price: "))
            ok, msg = svc.add_medicine_from_stock(med_id, name, gen_name,qty, price)
            print("Added." if ok else f" Error: {msg}")

        elif ch == "4":
            medicine_table = svc.list_medicines()
            print(medicine_table)
        
        elif ch == "5":
            print("\nSearch Medicine By:")
            print("1) Medicine Code")
            print("2) Medicine Name")
            sopt = input("Choose: ").strip()
            med = None
            
            if sopt == "1":
                mid = input("Enter Medicine Code: ").strip()
                result = svc.search_medicine_by_id(mid)
                print(result)
                med = svc.dao.search_medicine_by_id(mid)  # Call DAO directly
                
            elif sopt == "2":
                mname = input("Enter Medicine Name: ").strip()
                result = svc.search_medicine_by_name(mname)
                print(result)
                med = svc.dao.search_medicine_by_name(mname)  # Call DAO directly
            else:
                print("Invalid choice")
                continue

            if not med:
                print("Medicine not found")
                continue

            while True:
                print("\nHow would you like to proceed?")
                print("1) Edit Price")  # Only price editing option
                print("2) Disable Medicine")
                print("3) Go Back")
                opt = input("Choose: ").strip()

                if opt == "1":
                    new_price = float(input("Enter new Price: "))
                    ok, msg = svc.update_medicine(med["medicine_id"], "price", new_price)
                    print("Updated successfully" if ok else f"Error: {msg}")

                elif opt == "2":
                    ok, msg = svc.disable_medicine(med["medicine_id"])
                    print("Medicine disabled" if ok else f"Error: {msg}")

                elif opt == "3":
                    break
                else:
                    print("Invalid choice")

        elif ch == "6":
            print("Exiting program...")
            exit()
