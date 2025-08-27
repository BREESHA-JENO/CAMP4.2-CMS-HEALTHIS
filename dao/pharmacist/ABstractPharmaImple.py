from typing import List, Optional
from dao.pharmacist.AbstractPharmacistDao import MedicineDAO
from db.db_connection import DBConnection
from models.pharmacist_models.pharmacist import Medicine, StockMedicine, Billing

class MedicineDAOMySQL(MedicineDAO):

    #medicine
    def add_medicine(self, medicine: Medicine) -> bool:
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            sql = """
                INSERT INTO medicines (medicine_id, medicine_name, generic_name, expiry_date, price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(sql, (
                medicine.medicine_id,
                medicine.medicine_name,
                medicine.generic_name,
                medicine.expiry_date,
                medicine.price
            ))
        conn.commit()
        return True

    def list_medicines(self) -> List[Medicine]:
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT medicine_id, medicine_name, generic_name, expiry_date, price
                FROM medicines
                ORDER BY medicine_name
            """)
            rows = cur.fetchall()
        return [Medicine(*row) for row in rows]

    def search_medicine_by_id(self, medicine_id: str) -> Optional[Medicine]:
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT medicine_id, medicine_name, generic_name, expiry_date, price
                FROM medicines
                WHERE medicine_id = %s
            """, (medicine_id,))
            row = cur.fetchone()
        return Medicine(*row) if row else None

    def search_medicine_by_name(self, name: str) -> List[Medicine]:
        like = f"%{name}%"
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT medicine_id, medicine_name, generic_name, expiry_date, price
                FROM medicines
                WHERE medicine_name LIKE %s OR generic_name LIKE %s
                ORDER BY medicine_name
            """, (like, like))
            rows = cur.fetchall()
        return [Medicine(*row) for row in rows]

    def update_medicine(self, medicine: Medicine) -> bool:
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            sql = """
                UPDATE medicines
                SET medicine_name=%s, generic_name=%s, expiry_date=%s, price=%s
                WHERE medicine_id=%s
            """
            cur.execute(sql, (
                medicine.medicine_name,
                medicine.generic_name,
                medicine.expiry_date,
                medicine.price,
                medicine.medicine_id
            ))
        conn.commit()
        return cur.rowcount > 0

    def disable_medicine(self, medicine_id: str) -> bool:
        """
        Requires a column: ALTER TABLE medicines ADD COLUMN is_active ENUM('Y','N') DEFAULT 'Y';
        If you don't have it, skip calling this method.
        """
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE medicines SET is_active='N' WHERE medicine_id=%s
            """, (medicine_id,))
        conn.commit()
        return cur.rowcount > 0

    #  Stock 
    def add_stock(self, stock: StockMedicine) -> bool:
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            sql = """
                INSERT INTO stock_medicine (medicine_id, received_date, expiry_date, quantity, reorder_level)
                VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(sql, (
                stock.medicine_id,
                stock.received_date,
                stock.expiry_date,
                stock.quantity,
                stock.reorder_level
            ))
        conn.commit()
        return True

    def update_stock_quantity(self, medicine_id: str, add_qty: int) -> bool:
        """
        Increase quantity by add_qty in the latest-received batch.
        If no batch exists, create a placeholder batch with NULL expiry.
        """
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            # find a latest batch
            cur.execute("""
                SELECT stock_id FROM stock_medicine
                WHERE medicine_id=%s
                ORDER BY received_date DESC, stock_id DESC
                LIMIT 1
            """, (medicine_id,))
            row = cur.fetchone()
            if row:
                stock_id = row[0]
                cur.execute("""
                    UPDATE stock_medicine
                    SET quantity = quantity + %s
                    WHERE stock_id=%s
                """, (add_qty, stock_id))
            else:
                cur.execute("""
                    INSERT INTO stock_medicine (medicine_id, received_date, expiry_date, quantity, reorder_level)
                    VALUES (%s, CURRENT_DATE(), NULL, %s, 0)
                """, (medicine_id, add_qty))
        conn.commit()
        return True

    def get_total_stock(self, medicine_id: str) -> int:
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(SUM(quantity),0)
                FROM stock_medicine
                WHERE medicine_id=%s
            """, (medicine_id,))
            total = cur.fetchone()[0]
        return int(total or 0)

    def list_stock_batches(self, medicine_id: str) -> List[StockMedicine]:
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT stock_id, medicine_id, received_date, expiry_date, quantity, reorder_level
                FROM stock_medicine
                WHERE medicine_id=%s
                ORDER BY expiry_date ASC NULLS LAST, received_date ASC, stock_id ASC
            """, (medicine_id,))
            rows = cur.fetchall()
        return [StockMedicine(*row) for row in rows]

    # ------------ Price ------------
    def update_price(self, medicine_id: str, new_price: float) -> bool:
        conn = DBConnection().get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE medicines SET price=%s WHERE medicine_id=%s
            """, (new_price, medicine_id))
        conn.commit()
        return cur.rowcount > 0

    # ------------ Dispense + Billing ------------
    def dispense_and_bill(
        self,
        prescription_id: int,
        patient_id: int,
        medicine_id: str,
        dispense_qty: int,
        bill_status: str = "unpaid"
    ) -> Billing:
        """
        FEFO: reduce from earliest expiry first.
        Creates pha_billing row for the full dispense.
        Raises ValueError on insufficient stock.
        """
        if dispense_qty <= 0:
            raise ValueError("dispense quantity must be > 0")

        conn = DBConnection().get_connection()
        try:
            conn.begin()  # start transaction
            with conn.cursor() as cur:
                # 1) check total stock
                cur.execute("""
                    SELECT COALESCE(SUM(quantity),0)
                    FROM stock_medicine
                    WHERE medicine_id=%s
                """, (medicine_id,))
                total = cur.fetchone()[0] or 0
                if total < dispense_qty:
                    raise ValueError("Not enough stock for this medicine")

                # 2) get unit price
                cur.execute("""
                    SELECT price FROM medicines WHERE medicine_id=%s
                """, (medicine_id,))
                row = cur.fetchone()
                if not row:
                    raise ValueError("Medicine not found")
                unit_price = float(row[0])

                qty_to_reduce = dispense_qty

                # 3) pull batches in FEFO order
                cur.execute("""
                    SELECT stock_id, quantity
                    FROM stock_medicine
                    WHERE medicine_id=%s AND quantity > 0
                    ORDER BY expiry_date ASC, received_date ASC, stock_id ASC
                """, (medicine_id,))
                batches = cur.fetchall()

                for stock_id, qty in batches:
                    if qty_to_reduce <= 0:
                        break
                    take = min(qty, qty_to_reduce)
                    cur.execute("""
                        UPDATE stock_medicine
                        SET quantity = quantity - %s
                        WHERE stock_id = %s
                    """, (take, stock_id))
                    qty_to_reduce -= take

                # 4) insert billing
                amount = unit_price * dispense_qty
                cur.execute("""
                    INSERT INTO pha_billing
                        (prescription_id, patient_id, medicine_id, amount, status, quantity, created_at)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, NOW())
                """, (prescription_id, patient_id, medicine_id, amount, bill_status, dispense_qty))

                # fetch bill_id
                bill_id = cur.lastrowid

            conn.commit()
            return Billing(
                bill_id=bill_id,
                prescription_id=prescription_id,
                patient_id=patient_id,
                medicine_id=medicine_id,
                amount=amount,
                status=bill_status,
                quantity=dispense_qty,
                created_at=None  # DB NOW()
            )
        except Exception:
            conn.rollback()
            raise
