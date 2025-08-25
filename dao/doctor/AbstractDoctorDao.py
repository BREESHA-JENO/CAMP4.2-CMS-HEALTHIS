from abc import ABC, abstractmethod
from typing import List
from models.doctor import Doctor

class DoctorDaoService(ABC):
    @abstractmethod
    def priscribe_med(self)->List[Doctor]:
        pass
    
    @abstractmethod
    def priscribe_test(self)->list[Doctor]:
        pass
    
    @abstractmethod
    def display_result(self, consultation_id:int)->Doctor:
        pass
