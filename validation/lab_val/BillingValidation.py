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
    def validate_created_at(created_at) -> bool:
        if not isinstance(created_at, date):
            print("❌ Bill date must be a valid date object.")
            return False
        return True

