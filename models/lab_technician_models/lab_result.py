# models/lab_result.py
from datetime import date, datetime
from typing import Optional
import re

class LabResult:
    """
    Represents a result for a single test on a lab request.
    Stores result text/value, normal range and verification status.
    """
    VALID_VERIFICATION = ("PENDING", "VERIFIED", "REJECTED")

    def __init__(self,
                 res_id: Optional[int] = None,
                 lab_request_id: Optional[int] = None,
                 lab_test_id: Optional[str] = None,
                 staff_id: Optional[int] = None,
                 result_value: Optional[float] = None,
                 normal_range: Optional[float] = None,
                 remarks:  str = "",
                 created_at: Optional[datetime] = None):
        self.__res_id = res_id
        self.__lab_request_id = lab_request_id
        self.__lab_test_id = lab_test_id
        self.__staff_id = staff_id
        self.__result_value = result_value
        self.__normal_range = normal_range
        self.__remarks = remarks
        self.__created_at = created_at if created_at else date.today()
        

    # getters / setters
    def get_res_id(self):
        return self.__res_id

    def set_res_id(self, rid):
        self.__res_id = rid

    def get_lab_request_id(self):
        return self.__lab_request_id

    def set_lab_request_id(self, request_id):
        self.__lab_request_id = request_id

    def get_lab_test_id(self):
        return self.__lab_test_id

    def set_lab_test_id(self, test_id):
        self.__lab_test_id = test_id

    def get_staff_id(self):
        return self.__staff_id

    def set_staff_id(self, staff_id):
        self.__staff_id = staff_id

    def get_result_value(self):
        return self.__result_value

    def set_result_value(self, value: str):
        # simple sanitize: strip leading/trailing whitespace
        self.__result_value = value.strip()

    def get_normal_range(self):
        return self.__normal_range

    def set_normal_range(self, normal: str):
        self.__normal_range = normal

    def get_remarks(self):
        return self.__remarks

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def get_created_at(self):
        return self.__created_at

    def set_created_at(self, created_at):
        self.__created_at = created_at
       


    def __str__(self):
        return (f"Result ID:{self.__res_id:<8}, Req ID:{self.__lab_request_id:<8}, Test ID:{self.__lab_test_id:<6}, "
                f"Tech ID:{self.__staff_id:<6}, Value:{self.__result_value:<12} "
                f"Range:{self.__normal_range:<12}, Date:{self.__created_at}, Status:{self.__remarks}")
