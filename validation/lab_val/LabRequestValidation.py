from datetime import date
from typing import List
from models.lab_technician_models.lab_test import LabTest

class LabRequestValidation:
    """Validation utilities for LabRequest"""

    @staticmethod
    def validate_doctor_id(doctor_id: int) -> bool:
        if doctor_id <= 0:
            print("❌ Doctor ID must be positive.")
            return False
        return True

    @staticmethod
    def validate_patient_id(patient_id: int) -> bool:
        if patient_id <= 0:
            print("❌ Patient ID must be positive.")
            return False
        return True

    @staticmethod
    def validate_request_date(rdate) -> bool:
        if not isinstance(rdate, date):
            print("❌ Request date must be a valid date object.")
            return False
        return True

    @staticmethod
    def validate_tests(tests: List[LabTest]) -> bool:
        if not tests:
            print("❌ At least one test must be selected.")
            return False
        return True

    @staticmethod
    def validate_status(status: str) -> bool:
        valid_statuses = ["NEW", "SENT", "IN_PROGRESS", "COMPLETED", "CANCELLED"]
        if status not in valid_statuses:
            print(f"❌ Status must be one of {valid_statuses}")
            return False
        return True
