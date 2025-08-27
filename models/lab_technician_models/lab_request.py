# models/lab_request.py
from datetime import date, datetime
from typing import List, Optional
from .lab_test import LabTest
import re

class LabRequest:
    """
    Represents a lab request raised by a doctor for a patient.
    Contains references to tests (by object or ids), status, and timestamps.
    """
    VALID_STATUSES = ("NEW", "SENT", "IN_PROGRESS", "COMPLETED", "CANCELLED")

    def __init__(self,
                 request_id: Optional[int] = None,
                 doctor_id: Optional[int] = None,
                 patient_id: Optional[int] = None,
                 tests: Optional[List[LabTest]] = None,
                 request_date: Optional[date] = None,
                 clinical_notes: str = "",
                 status: str = "NEW"):
        self.__request_id = request_id
        self.__doctor_id = doctor_id
        self.__patient_id = patient_id
        self.__tests = tests if tests else []  # list of LabTest objects
        self.__request_date = request_date if request_date else date.today()
        self.__clinical_notes = clinical_notes
        self.__status = status if status in self.VALID_STATUSES else "NEW"
        self.__created_datetime = datetime.now()

    # getters/setters
    def get_request_id(self):
        return self.__request_id

    def set_request_id(self, rid):
        self.__request_id = rid

    def get_doctor_id(self):
        return self.__doctor_id

    def set_doctor_id(self, did):
        self.__doctor_id = did

    def get_patient_id(self):
        return self.__patient_id

    def set_patient_id(self, pid):
        self.__patient_id = pid

    def get_tests(self):
        return list(self.__tests)  # return copy

    def add_test(self, test: LabTest):
        if not isinstance(test, LabTest):
            raise ValueError("add_test expects a LabTest instance")
        self.__tests.append(test)

    def remove_test_by_id(self, test_id):
        self.__tests = [t for t in self.__tests if t.get_test_id() != test_id]

    def get_request_date(self):
        return self.__request_date

    def set_request_date(self, rdate):
        self.__request_date = rdate

    def get_clinical_notes(self):
        return self.__clinical_notes

    def set_clinical_notes(self, notes: str):
        self.__clinical_notes = notes

    def get_status(self):
        return self.__status

    def set_status(self, status: str):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self.__status = status

    def get_created_datetime(self):
        return self.__created_datetime

    def total_estimated_cost(self):
        """
        Sum the unit_price of all included tests.
        """
        return sum([t.get_unit_price() for t in self.__tests])

    def __str__(self):
        tests_str = ", ".join([t.get_test_name() or f"ID:{t.get_test_id()}" for t in self.__tests])
        return (f"Request ID:{self.__request_id:<8}, Doctor ID:{self.__doctor_id:<6}, "
                f"Patient ID:{self.__patient_id:<6}, Tests:[{tests_str}], "
                f"Requested:{self.__request_date}, Status:{self.__status}")
