from datetime import date

class LabResultValidation:
    """Validation utilities for LabResult"""

    @staticmethod
    def validate_result_value(value: str) -> bool:
        if not value or value.strip() == "":
            print("❌ Result value cannot be empty.")
            return False
        return True

    @staticmethod
    def validate_units(units: str) -> bool:
        if not units:
            print("❌ Units cannot be empty.")
            return False
        return True

    @staticmethod
    def validate_normal_range(normal: str) -> bool:
        if not normal:
            print("❌ Normal range cannot be empty.")
            return False
        return True

    @staticmethod
    def validate_result_date(rdate) -> bool:
        if not isinstance(rdate, date):
            print("❌ Result date must be a valid date object.")
            return False
        return True

    @staticmethod
    def validate_verification_status(status: str) -> bool:
        valid_statuses = ["PENDING", "VERIFIED", "REJECTED"]
        if status not in valid_statuses:
            print(f"❌ Verification status must be one of {valid_statuses}")
            return False
        return True
