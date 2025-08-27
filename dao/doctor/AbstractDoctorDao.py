from abc import ABC, abstractmethod
from typing import List
from models.doctor_models.doctor import Doctor

class DoctorDaoService(ABC):
    @abstractmethod
    def view_all_appointments(self):
        '''to view all patient appointments created by receptionist'''
        pass 


    # @abstractmethod
    # def insert_consultation_details(self):
    #     '''method to insert consultation details into consultation table '''
    #     pass
    # @abstractmethod
    # def priscribe_med(self)->List[Doctor]:
    #     pass
    
    # @abstractmethod
    # def priscribe_test(self)->list[Doctor]:
    #     pass
    
    # @abstractmethod
    # def display_result(self, consultation_id:int)->Doctor:
    #     pass
