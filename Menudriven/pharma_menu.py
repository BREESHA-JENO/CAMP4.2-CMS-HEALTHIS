from lib.pharmacist_lib.PharmaManagementLib import PharmaManagementLib

def run_pharma_menu():
    svc = PharmaManagementLib()
    while True:
        print("\n=== Pharmacist Menu ===")
        print("1) Add Stock")
        print("2) List Stock")
        print("3) Add Medicine FROM Stock")
        print("4) List Medicines")
        print("0) Exit")
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
            rows = svc.list_stock()
            for r in rows:
                print(r)

        elif ch == "3":
            med_id = input("Enter Medicine ID to move from stock: ").strip()
            name = input("Medicine name (for doctor view): ").strip()
            qty = int(input("Quantity: "))
            price = float(input("Price: "))
            ok, msg = svc.add_medicine_from_stock(med_id, name, qty, price)
            print("Added." if ok else f" Error: {msg}")

        elif ch == "4":
            meds = svc.list_medicines()
            for m in meds:
                print(m)

        elif ch == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    run_pharma_menu()
