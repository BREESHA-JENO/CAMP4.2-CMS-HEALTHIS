import uuid
from typing import List, Optional
from db.db_connection import DBConnection
from dao.pharmacist.AbstractPharmacistDao import MedicineDAO
from dao.pharmacist.ABstractPharmaImple import MedicineDAOMySQL
from models.pharmacist_models.pharmacist import Medicine, StockMedicine, Billing

class PharmaManagementLib:
    dao = MedicineDAOMySQL()

    # ---------- ID Generators ----------
    @staticmethod
    def generate_medicine_id() -> str:
    # fetch latest medicine_id from DB
      conn = PharmaManagementLib.dao.db.get_connection() 
      with conn.cursor() as cur:
        cur.execute("SELECT medicine_id FROM medicines ORDER BY medicine_id DESC LIMIT 1")
        row = cur.fetchone()

      if row:
        last_id = int(row[0].replace("MED", ""))  # strip MED prefix
        new_id = last_id + 1
      else:
        new_id = 1  # first medicine

      return f"MED{new_id:03d}"


    @staticmethod
    def generate_stock_batch_qty(medicine_id: str, qty: int, received_date: str, expiry_date: Optional[str], reorder_level: int) -> StockMedicine:
        return StockMedicine(
            stock_id=None,
            medicine_id=medicine_id,
            received_date=received_date,
            expiry_date=expiry_date,
            quantity=qty,
            reorder_level=reorder_level
        )

    # ---------- Medicine ----------
    @staticmethod
    def add_medicine(medicine_name: str, generic_name: str, expiry_date: str, price: float) -> Medicine:
        mid = PharmaManagementLib.generate_medicine_id()
        med = Medicine(mid, medicine_name, generic_name, expiry_date, price)
        PharmaManagementLib.dao.add_medicine(med)
        return med

    @staticmethod
    def list_medicines() -> List[Medicine]:
        return PharmaManagementLib.dao.list_medicines()

    @staticmethod
    def search_medicine_by_id(medicine_id: str) -> Optional[Medicine]:
        return PharmaManagementLib.dao.search_medicine_by_id(medicine_id)

    @staticmethod
    def search_medicine_by_name(name: str) -> List[Medicine]:
        return PharmaManagementLib.dao.search_medicine_by_name(name)

    @staticmethod
    def update_medicine(medicine_id: str, medicine_name: str, generic_name: str, expiry_date: str, price: float) -> bool:
        med = Medicine(medicine_id, medicine_name, generic_name, expiry_date, price)
        return PharmaManagementLib.dao.update_medicine(med)


    # ---------- Stock ----------
    @staticmethod
    def add_stock(medicine_id: str, received_date: str, expiry_date: Optional[str], quantity: int, reorder_level: int) -> bool:
        stock = PharmaManagementLib.generate_stock_batch_qty(
            medicine_id=medicine_id,
            qty=quantity,
            received_date=received_date,
            expiry_date=expiry_date,
            reorder_level=reorder_level
        )
        return PharmaManagementLib.dao.add_stock(stock)

    @staticmethod
    def get_total_stock(medicine_id: str) -> int:
        return PharmaManagementLib.dao.get_total_stock(medicine_id)

    @staticmethod
    def list_stock_batches(medicine_id: str) -> List[StockMedicine]:
        return PharmaManagementLib.dao.list_stock_batches(medicine_id)

    @staticmethod
    def update_stock_quantity(medicine_id: str, add_qty: int) -> bool:
        return PharmaManagementLib.dao.update_stock_quantity(medicine_id, add_qty)

    # ---------- Price ----------
    @staticmethod
    def update_price(medicine_id: str, new_price: float) -> bool:
        return PharmaManagementLib.dao.update_price(medicine_id, new_price)

    # ---------- Dispense + Billing ----------
    @staticmethod
    def dispense_and_bill(prescription_id: int, patient_id: int, medicine_id: str, quantity: int, bill_status: str = "unpaid") -> Billing:
        return PharmaManagementLib.dao.dispense_and_bill(
            prescription_id=prescription_id,
            patient_id=patient_id,
            medicine_id=medicine_id,
            dispense_qty=quantity,
            bill_status=bill_status
        )
