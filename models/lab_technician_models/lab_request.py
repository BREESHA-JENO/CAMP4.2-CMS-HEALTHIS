# models/lab_request.py
from datetime import datetime
from typing import Optional
from .lab_test import LabTest

class LabRequest:
    """
    Represents a lab request raised by a doctor for a patient.
    Matches the lab_request table in the database.
    """
    VALID_STATUSES = ("New", "Sent", "In_Progress", "Completed", "Cancelled")

    def __init__(self,
                 lab_request_id: Optional[int] = None,
                 consultation_id: Optional[str] = None,
                 patient_id: Optional[str] = None,
                 test_id_doc: Optional[int] = None,
                 staff_id: Optional[str] = None,
                 status: str = "Completed",
                 created_at: Optional[datetime] = None):
        self.__lab_request_id = lab_request_id
        self.__consultation_id = consultation_id
        self.__patient_id = patient_id
        self.__test_id_doc = test_id_doc
        self.__staff_id = staff_id
        self.__status = status if status in self.VALID_STATUSES else "NEW"
        self.__created_at = created_at if created_at else datetime.now()

    # --- getters/setters ---
    def get_lab_request_id(self):
        return self.__lab_request_id

    def set_lab_request_id(self, rid):
        self.__lab_request_id = rid

    def get_consultation_id(self):
        return self.__consultation_id

    def set_consultation_id(self, cid):
        self.__consultation_id = cid

    def get_patient_id(self):
        return self.__patient_id

    def set_patient_id(self, pid):
        self.__patient_id = pid

    def get_test_id_doc(self):
        return self.__test_id_doc

    def set_test_id_doc(self, tid):
        self.__test_id_doc = tid

    def get_staff_id(self):
        return self.__staff_id

    def set_staff_id(self, sid):
        self.__staff_id = sid

    def get_status(self):
        return self.__status

    def set_status(self, status: str):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self.__status = status

    def get_created_datetime(self):
        return self.__created_at

    def set_created_datetime(self, cdt):
        self.__created_at = cdt

    # --- string representation ---
    def __str__(self):
        return (f"Request ID:{self.__lab_request_id}, Consultation ID:{self.__consultation_id}, "
                f"Patient ID:{self.__patient_id}, Test ID:{self.__test_id_doc}, "
                f"Staff ID:{self.__staff_id}, Status:{self.__status}, "
                f"Created At:{self.__created_at}")
