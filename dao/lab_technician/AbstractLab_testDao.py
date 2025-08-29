from abc import ABC, abstractmethod
from typing import List
from models.lab_technician_models.lab_test import LabTest

class LabTestDaoService(ABC):

    @abstractmethod
    def display_all_tests(self) -> List[LabTest]:
        '''fetch all lab tests'''
        pass

    @abstractmethod
    def insert_test(self, test: LabTest) -> bool:
        '''insert new lab test'''
        pass

    @abstractmethod
    def find_by_test_id(self, test_id: int) -> LabTest:
        '''find test by id'''
        pass

    @abstractmethod
    def update_test(self, test: LabTest, test_id: int) -> bool:
        '''update lab test'''
        pass

    @abstractmethod
    def disable_test(self, test: LabTest, test_id: int) -> bool:
        '''disable a test (set is_active=N)'''
        pass
