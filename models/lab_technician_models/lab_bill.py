# models/billing.py
from datetime import date
from typing import List, Optional, Dict

class Billing:
    """
    Simple Billing class that stores billed items (description + amount) and computes totals.
    Designed similar to product.py style with private attributes and getters/setters.
    """
    def __init__(self,
                 test_bill_id: Optional[int] = None,
                 patient_id: Optional[str] = None,
                 lab_test_id: Optional[str] = None,
                 total_amount: float = 0.0,
                 status: str = "Paid",
                 created_at: Optional[date] = None):
            self.__test_bill_id = test_bill_id
            self.__patient_id = patient_id
            # items: list of dicts like {"description": "CBC", "amount": 200.0}
            self.__lab_test_id = lab_test_id
            self.__total_amount = total_amount
            self.__status = status
            self.__created_at = created_at if created_at else date.today()
        

    # getters / setters
    def get_test_bill_id(self):
        return self.__test_bill_id

    def set_test_bill_id(self, bid):
        self.__test_bill_id = bid

    def get_patient_id(self):
        return self.__patient_id

    def set_patient_id(self, pid):
        self.__patient_id = pid

    def get_lab_test_id(self):
        return self.__lab_test_id

    def set_lab_test_id(self, ltid):
        self.__lab_test_id= ltid


    def get_total_amount(self):
        return self.__total_amount
    
    def set_total_amount(self, amount: float):
        self.__total_amount = float(amount)


    def get_status(self):
        return self.__status

    def set_status(self, status:str):
        self.__status = status.upper() # store as "UNPAID"/"PAID"

    def get_created_at(self):
        return self.__created_at

    def set_created_at(self, cdate: date):
        self.__created_at = cdate



    def generate_simple_invoice(self):
        """
        Returns a multi-line string invoice (simple).
        """
        lines = []
        lines.append(f"Bill ID: {self.__test_bill_id}")
        lines.append(f"Patient ID: {self.__patient_id}")
        lines.append(f"Date: {self.__created_at}")
        lines.append("-" * 40)
        for it in self.__items:
            lines.append(f"{it.get('description'):<30} {it.get('amount'):>8.2f}")
        lines.append("-" * 40)
        lines.append(f"{'Total':<30} {self.__total_amount:>8.2f}")
        lines.append(f"Paid: {'Yes' if self.__status else 'No'}")
        return "\n".join(lines)

    def __str__(self):
        return f"Bill ID:{self.__test_bill_id:<8}, Patient:{self.__patient_id:<8}, Total:{self.__total_amount:<10.2f}, Paid:{self.__status}"
