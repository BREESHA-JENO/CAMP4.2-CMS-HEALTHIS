import re
from datetime import date

class LabTestValidation:
    """Validation utilities for LabTest"""

    @staticmethod
    def validate_test_name(name: str) -> bool:
        if not name:
            print("❌ Test name cannot be empty.")
            return False
        if not re.match(r"^[A-Za-z\s\-]{2,50}$", name):
            print("❌ Test name must be 2–50 characters (letters/spaces/hyphens).")
            return False
        return True

    @staticmethod
    def validate_unit_price(price: float) -> bool:
        if price < 0:
            print("❌ Unit price cannot be negative.")
            return False
        return True

    @staticmethod
    def validate_sample_type(stype: str) -> bool:
        if not stype:
            print("❌ Sample type cannot be empty.")
            return False
        if len(stype) < 2:
            print("❌ Sample type must have at least 2 characters.")
            return False
        return True

    @staticmethod
    def validate_created_date(cdate) -> bool:
        if not isinstance(cdate, date):
            print("❌ Created date must be a valid date object.")
            return False
        return True
