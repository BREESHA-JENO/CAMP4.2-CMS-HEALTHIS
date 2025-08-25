import mysql
from dao.pharmacist.AbstractPharmacistDao import MedicineDAO
from models.pharmacist import Pharmacist
from db.db_connection import DBConnection

class Medicine(MedicineDAO):

    def add_medicine(self, medicine: MedicineDAO):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO medicines (medicine_id, name, category, price, stock_qty, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (medicine.medicine_id, medicine.name, medicine.category,
              medicine.price, medicine.stock_qty, medicine.is_active))
        conn.commit()
        conn.close()

    def list_medicines(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicines")
        rows = cur.fetchall()
        conn.close()
        return [Medicine(*row) for row in rows]

    def search_medicine(self, keyword: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicines WHERE name LIKE ?", ('%' + keyword + '%',))
        rows = cur.fetchall()
        conn.close()
        return [Medicine(*row) for row in rows]

    def view_medicine(self, medicine_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicines WHERE medicine_id=?", (medicine_id,))
        row = cur.fetchone()
        conn.close()
        return Medicine(*row) if row else None

    def update_medicine(self, medicine: MedicineDAO):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE medicines
            SET name=?, category=?, price=?, stock_qty=?, is_active=?
            WHERE medicine_id=?
        """, (medicine.name, medicine.category, medicine.price, medicine.stock_qty,
              medicine.is_active, medicine.medicine_id))
        conn.commit()
        conn.close()

    def disable_medicine(self, medicine_id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE medicines SET is_active='N' WHERE medicine_id=?", (medicine_id,))
        conn.commit()
        conn.close()

    def update_stock(self, medicine_id: str, delta: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT stock_qty FROM medicines WHERE medicine_id=?", (medicine_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return False, None
        new_qty = row[0] + delta
        if new_qty < 0:
            conn.close()
            return False, row[0]
        cur.execute("UPDATE medicines SET stock_qty=? WHERE medicine_id=?", (new_qty, medicine_id))
        conn.commit()
        conn.close()
        return True, new_qty

    def update_price(self, medicine_id: str, new_price: float):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE medicines SET price=? WHERE medicine_id=?", (new_price, medicine_id))
        conn.commit()
        conn.close()

    def fetch_medicine(self, medicine_id: str):
        success, new_qty = self.update_stock(medicine_id, -1)
        if not success:
            med = self.view_medicine(medicine_id)
            if med:
                return f"No {med.name} available"
            return "Medicine not found"
        return self.view_medicine(medicine_id)
