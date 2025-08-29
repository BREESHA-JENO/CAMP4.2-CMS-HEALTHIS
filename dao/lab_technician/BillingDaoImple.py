from dao.lab_technician.abstractlab_billDao import BillingDaoService
from db.db_connection import DBConnection
from models.lab_technician_models.lab_bill import Billing
from typing import List
from pymysql.cursors import DictCursor

class BillingDaoImplementation(BillingDaoService):
    DISPLAY_ALL = "SELECT * FROM test_billing"
    INSERT_BILL = """
        INSERT INTO test_billing(patient_id, lab_test_id, total_amount, status, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    FIND_BY_ID = "SELECT * FROM test_billing WHERE test_bill_id=%s"
    UPDATE_BILL = "UPDATE test_billing SET status=%s, total_amount=%s WHERE test_bill_id=%s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def display_all_bills(self) -> List[Billing]:
        bills = []
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.DISPLAY_ALL)
        for row in cursor.fetchall():
            bills.append(Billing(
                test_bill_id=row["test_bill_id"],
                patient_id=row["patient_id"],
                lab_test_id=row["lab_test_id"],
                created_at=row["created_at"],
                total_amount=row["total_amount"],
                status=row["status"]
            ))
        cursor.close()
        return bills

    def insert_bill(self, bill: Billing) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.INSERT_BILL, (
            bill.get_patient_id(),
            bill.get_lab_test_id(),
            bill.get_total_amount(),
            bill.get_status(),
            bill.get_created_at()
        ))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success

    def find_by_bill_id(self, bill_id: int) -> Billing:
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.FIND_BY_ID, (bill_id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return Billing(
            test_bill_id=row["test_bill_id"],
            patient_id=row["patient_id"],
            lab_test_id=row["lab_test_id"],
            created_at=row["created_at"],
            total_amount=row["total_amount"],
            status=row["status"]
        )

    def update_bill(self, bill: Billing, bill_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.UPDATE_BILL, (
            bill.get_status(),
            bill.get_total_amount(),
            bill_id
        ))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success
