from datetime import date
from typing import List, Dict

class BillingValidation:
    """Validation utilities for Billing"""

    @staticmethod
    def validate_patient_id(patient_id: int) -> bool:
        if patient_id <= 0:
            print("❌ Patient ID must be positive.")
            return False
        return True

    @staticmethod
    def validate_items(items: List[Dict[str, float]]) -> bool:
        if not items:
            print("❌ Billing items cannot be empty.")
            return False
        for item in items:
            if "description" not in item or not item["description"]:
                print("❌ Item description cannot be empty.")
                return False
            if "amount" not in item or item["amount"] < 0:
                print("❌ Item amount must be non-negative.")
                return False
        return True

    @staticmethod
    def validate_bill_date(bill_date) -> bool:
        if not isinstance(bill_date, date):
            print("❌ Bill date must be a valid date object.")
            return False
        return True

    @staticmethod
    def validate_payment_mode(mode: str) -> bool:
        if mode.upper() not in ["CASH", "CARD", "UPI", "UNPAID"]:
            print("❌ Payment mode must be CASH, CARD, UPI, or UNPAID.")
            return False
        return True
