from dao.lab_technician.abstractlab_billDao import BillingDaoService
from db.db_connection import DBConnection
from models.lab_technician_models.lab_bill import Billing
from typing import List
from pymysql.cursors import DictCursor
import json  # storing bill items as JSON in db

class BillingDaoImplementation(BillingDaoService):
    DISPLAY_ALL = "SELECT * FROM billing"
    INSERT_BILL = "INSERT INTO billing(patientid, items, billdate, ispaid, paymentmode) VALUES(%s,%s,%s,%s,%s)"
    FIND_BY_ID = "SELECT * FROM billing WHERE billid=%s"
    UPDATE_BILL = "UPDATE billing SET ispaid=%s, paymentmode=%s, items=%s WHERE billid=%s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def display_all_bills(self) -> List[Billing]:
        bills = []
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.DISPLAY_ALL)
        for row in cursor.fetchall():
            items = json.loads(row["items"]) if row["items"] else []
            bills.append(Billing(bill_id=row["billid"], patient_id=row["patientid"],
                                 items=items, bill_date=row["billdate"],
                                 is_paid=row["ispaid"], payment_mode=row["paymentmode"]))
        cursor.close()
        return bills

    def insert_bill(self, bill: Billing) -> bool:
        cursor = self.conn.cursor()
        items_json = json.dumps(bill.get_items())
        cursor.execute(self.INSERT_BILL, (bill.get_patient_id(), items_json,
                                          bill.get_bill_date(), bill.get_is_paid(),
                                          bill.get_payment_mode()))
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
        items = json.loads(row["items"]) if row["items"] else []
        return Billing(bill_id=row["billid"], patient_id=row["patientid"],
                       items=items, bill_date=row["billdate"],
                       is_paid=row["ispaid"], payment_mode=row["paymentmode"])

    def update_bill(self, bill: Billing, bill_id: int) -> bool:
        cursor = self.conn.cursor()
        items_json = json.dumps(bill.get_items())
        cursor.execute(self.UPDATE_BILL, (bill.get_is_paid(), bill.get_payment_mode(), items_json, bill_id))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success
