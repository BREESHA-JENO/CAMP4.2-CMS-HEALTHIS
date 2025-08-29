from abc import ABC, abstractmethod
from typing import List
from models.doctor_models.doctor import Doctor

class DoctorDaoService(ABC):
    @abstractmethod
    def view_all_appointments(self, staff_id):
        '''to view all patient appointments created by receptionist'''
        pass 
    
    @abstractmethod
    def view_all_appointments_date(self, staff_id, date):
        '''to view all patient appointments created by receptionist by date'''
        pass 
    
    @abstractmethod
    def insert_consultation(self, appointment_id, staff_id, symptoms, diagnosis, notes):
        '''inserting after consulting patients'''
        pass
    
    @abstractmethod
    def prescribe_medicine(self, consultation_id, medicine_id, dosage, duration):
        '''prescribe med after consulting patients'''
        pass
    
    @abstractmethod
    def prescribe_lab_test(self, consultation_id, test_id, staff_id):
        '''prescribing for test after consulting patients'''
        pass
    
    @abstractmethod
    def get_consultation_history(self, patient_id):
        '''consultation history'''
        pass
