# models/billing.py
from datetime import date
from typing import List, Optional, Dict

class Billing:
    """
    Simple Billing class that stores billed items (description + amount) and computes totals.
    Designed similar to product.py style with private attributes and getters/setters.
    """
    def __init__(self,
                 bill_id: Optional[int] = None,
                 patient_id: Optional[int] = None,
                 items: Optional[List[Dict[str, float]]] = None,
                 bill_date: Optional[date] = None,
                 is_paid: bool = False,
                 payment_mode: str = "UNPAID"):
        self.__bill_id = bill_id
        self.__patient_id = patient_id
        # items: list of dicts like {"description": "CBC", "amount": 200.0}
        self.__items = items if items else []
        self.__bill_date = bill_date if bill_date else date.today()
        self.__is_paid = is_paid
        self.__payment_mode = payment_mode

    # getters / setters
    def get_bill_id(self):
        return self.__bill_id

    def set_bill_id(self, bid):
        self.__bill_id = bid

    def get_patient_id(self):
        return self.__patient_id

    def set_patient_id(self, pid):
        self.__patient_id = pid

    def get_items(self):
        return list(self.__items)  # return copy

    def add_item(self, description: str, amount: float):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.__items.append({"description": description, "amount": float(amount)})

    def remove_item(self, description: str):
        self.__items = [i for i in self.__items if i.get("description") != description]

    def get_bill_date(self):
        return self.__bill_date

    def set_bill_date(self, bdate):
        self.__bill_date = bdate

    def get_is_paid(self):
        return self.__is_paid

    def set_is_paid(self, paid: bool):
        self.__is_paid = bool(paid)

    def get_payment_mode(self):
        return self.__payment_mode

    def set_payment_mode(self, mode: str):
        self.__payment_mode = mode

    def total_amount(self):
        return sum([i.get("amount", 0.0) for i in self.__items])

    def generate_simple_invoice(self):
        """
        Returns a multi-line string invoice (simple).
        """
        lines = []
        lines.append(f"Bill ID: {self.__bill_id}")
        lines.append(f"Patient ID: {self.__patient_id}")
        lines.append(f"Date: {self.__bill_date}")
        lines.append("-" * 40)
        for it in self.__items:
            lines.append(f"{it.get('description'):<30} {it.get('amount'):>8.2f}")
        lines.append("-" * 40)
        lines.append(f"{'Total':<30} {self.total_amount():>8.2f}")
        lines.append(f"Paid: {'Yes' if self.__is_paid else 'No'} Mode: {self.__payment_mode}")
        return "\n".join(lines)

    def __str__(self):
        return f"Bill ID:{self.__bill_id:<8}, Patient:{self.__patient_id:<8}, Total:{self.total_amount():<10.2f}, Paid:{self.__is_paid}"
