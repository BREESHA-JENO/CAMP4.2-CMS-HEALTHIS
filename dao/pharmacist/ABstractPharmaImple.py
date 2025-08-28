import pymysql
from pymysql.cursors import DictCursor
import pymysql
from pymysql.cursors import DictCursor
from db.db_connection import DBConnection
from models.pharmacist_models.pharmacist import StockMedicine, Medicine
from dao.pharmacist.AbstractPharmacistDao import AbstractPharmacistDao



class PharmacistDaoImpl(AbstractPharmacistDao):
    def __init__(self):
        self.conn = DBConnection().get_connection()

    def generate_medicine_id(self):
        with self.conn.cursor(DictCursor) as cur: 
            cur.execute("SELECT COUNT(*) AS cnt FROM stock_medicines")
            count = cur.fetchone()['cnt'] + 1
            return f"MED{str(count).zfill(3)}"

    # ---------- STOCK ----------
    def add_stock(self, stock: StockMedicine):
        try:
            stock.medicine_id = self.generate_medicine_id()
            sql = """INSERT INTO stock_medicines
                    (medicine_id, medicine_name, received_date, expiry_date, quantity, reorder_level)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            with self.conn.cursor() as cur:
                cur.execute(sql, (stock.medicine_id, stock.medicine_name,
                                stock.received_date, stock.expiry_date,
                                stock.quantity, stock.reorder_level))

            self.conn.commit()
            return True, stock.medicine_id
        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def list_stock(self):
        try:
            sql = "SELECT * FROM stock_medicines ORDER BY stock_id"
            with self.conn.cursor(DictCursor) as cur: 
                cur.execute(sql)
                return cur.fetchall()  # Return raw data
        except Exception as e:
            print(f"Error in list_stock: {e}")
            return []

    # ---------- MEDICINES ----------
    def add_medicine_from_stock(self, medicine_id: str, medicine_name: str, generic_name: str, quantity: int, price: float):
        try:
            with self.conn.cursor(DictCursor) as cur:  
                # Check stock exists
                cur.execute("SELECT SUM(quantity) AS total_qty FROM stock_medicines WHERE medicine_id=%s", (medicine_id,))
                row = cur.fetchone()
                if not row or row['total_qty'] is None or row['total_qty'] < quantity:
                    return False, f"Medicine ID is wrong or insufficient stock"

                
                cur.execute(
                    "INSERT INTO medicines (medicine_id, medicine_name, generic_name, price, expiry_date) "
                    "SELECT medicine_id, medicine_name, %s, %s, expiry_date "
                    "FROM stock_medicines WHERE medicine_id=%s ORDER BY expiry_date LIMIT 1",
                    (generic_name, price, medicine_id)
                )

                remaining = quantity
                cur.execute("SELECT stock_id, quantity FROM stock_medicines WHERE medicine_id=%s ORDER BY expiry_date", (medicine_id,))
                stocks = cur.fetchall()
                for s in stocks:
                    if remaining <= 0:
                        break
                    deduct = min(remaining, s['quantity'])
                    cur.execute("UPDATE stock_medicines SET quantity=quantity-%s WHERE stock_id=%s", (deduct, s['stock_id']))
                    remaining -= deduct


            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, str(e)



    def list_medicines(self):
        try:
            sql = "SELECT * FROM medicines ORDER BY medicine_auto_id"
            with self.conn.cursor(DictCursor) as cur: 
                cur.execute(sql)
                return cur.fetchall()  # Return raw data
        except Exception as e:
            print(f"Error in list_medicines: {e}")
            return []

    def search_medicine_by_id(self, medicine_id: str):
        sql = "SELECT * FROM medicines WHERE medicine_id=%s"
        with self.conn.cursor(DictCursor) as cur:
            cur.execute(sql, (medicine_id,))
            return cur.fetchone()

    def search_medicine_by_name(self, medicine_name: str):
        sql = "SELECT * FROM medicines WHERE LOWER(medicine_name)=LOWER(%s)"
        with self.conn.cursor(DictCursor) as cur:
            cur.execute(sql, (medicine_name,))
            return cur.fetchone()

    def update_medicine(self, medicine_id: str, field: str, value):
        try:
            if field not in ("quantity", "price"):
                return False, "Invalid field"
            sql = f"UPDATE medicines SET {field}=%s WHERE medicine_id=%s"
            with self.conn.cursor() as cur:
                cur.execute(sql, (value, medicine_id))
            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def disable_medicine(self, medicine_id: str):
        try:
            sql = "UPDATE medicines SET status='disabled' WHERE medicine_id=%s"
            with self.conn.cursor() as cur:
                cur.execute(sql, (medicine_id,))
            self.conn.commit()
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, str(e)
