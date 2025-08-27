# models/lab_test.py
from datetime import date
import re
from typing import Optional

class LabTest:
    """
    Represents a lab test (metadata).
    Similar style to product.py: private attributes, validation in setters,
    and a readable __str__ method.
    """
    def __init__(self,
             lab_test_id: Optional[str] = None,
             test_name: Optional[str] = None,
             price: float = 0.0,
             sampletype: str = "Blood",
             isActive: str = "Y",
             created_at: Optional[date] = None):
        self.__test_id = lab_test_id   # DAO will pass generated ID
        self.__test_name = None
        self.__price = price
        self.__sampletype = sampletype
        self.__isActive = isActive
        self.__created_at = created_at if created_at else date.today()

        if test_name is not None:
            self.set_test_name(test_name)
    

    # getters / setters
    def get_test_id(self):
        return self.__test_id

    def set_test_id(self, test_id):
        self.__test_id = test_id

    def get_test_name(self):
        return self.__test_name

    def set_test_name(self, name: str):
        """
        Validate test name: 2-50 characters, letters, spaces, hyphens allowed.
        If invalid, re-prompt (mirrors product.py behavior).
        """
        pattern = re.compile(r"^[A-Za-z\s\-]{2,50}$")
        while True:
            if pattern.match(name):
                self.__test_name = name
                break
            else:
                print("\t\t Invalid test name (2-50 letters, spaces or hyphens).")
                name = input("\t\t Enter Test Name again: ")

    def get_price(self):
        return self.__price

    def set_price(self, price: float):
        if price < 0:
            raise ValueError("Unit price cannot be negative")
        self.__price = price

    def get_sampletype(self):
        return self.__sampletype

    def set_sampletype(self, stype: str):
        self.__sampletype = stype

    def get_created_at(self):
        return self.__created_at

    def set_created_at(self, created_at):
        if isinstance(created_at, date):
            self.__created_at = created_at
        else:
            raise ValueError("created_date must be a date object")

    def get_isActive(self):
        return self.__isActive

    def set_isActive(self, flag: str):
        self.__isActive = flag

    def __str__(self):
       return (f"Test ID:{str(self.__test_id or ''):<8}, "
            f"Test Name:{str(self.__test_name or ''):<30}, "
            f"Price:{str(self.__price or 0):<10}, "
            f"Sample Type:{str(self.__sampletype or ''):<15}, "
            f"Active:{str(self.__isActive or ''):<5}, "
            f"Created:{str(self.__created_at or ''):<15}")
