import pymysql
from pymysql.cursors import DictCursor
from db.db_connection import DBConnection
from models.pharmacist_models.pharmacist import StockMedicine, Medicine
from dao.pharmacist.AbstractPharmacistDao import AbstractPharmacistDao


class PharmacistDaoImpl(AbstractPharmacistDao):
    def __init__(self):
        self.conn = DBConnection().get_connection()

    def generate_medicine_id(self):
        with self.conn.cursor(DictCursor) as cur:   # ✅ Use DictCursor
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
        sql = "SELECT * FROM stock_medicines ORDER BY stock_id"
        with self.conn.cursor(DictCursor) as cur:   # ✅ DictCursor
            cur.execute(sql)
            return cur.fetchall()

    # ---------- MEDICINES ----------
    def add_medicine_from_stock(self, medicine_id: str, medicine_name: str, generic_name: str, quantity: int, price: float):
        try:
            with self.conn.cursor(DictCursor) as cur:   # ✅ DictCursor
                # Check stock exists
                cur.execute("SELECT SUM(quantity) AS total_qty FROM stock_medicines WHERE medicine_id=%s", (medicine_id,))
                row = cur.fetchone()
                if not row or row['total_qty'] is None or row['total_qty'] < quantity:
                    return False, f"Medicine ID is wrong or insufficient stock"

                # Insert into medicines (use passed generic_name instead of NULL)
                cur.execute(
                    "INSERT INTO medicines (medicine_id, medicine_name, generic_name, price, expiry_date) "
                    "SELECT medicine_id, medicine_name, %s, %s, expiry_date "
                    "FROM stock_medicines WHERE medicine_id=%s ORDER BY expiry_date LIMIT 1",
                    (generic_name, price, medicine_id)
                )

                # Decrease stock FIFO
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
        sql = "SELECT * FROM medicines ORDER BY medicine_auto_id"
        with self.conn.cursor(DictCursor) as cur:   # ✅ DictCursor
            cur.execute(sql)
            return cur.fetchall()
