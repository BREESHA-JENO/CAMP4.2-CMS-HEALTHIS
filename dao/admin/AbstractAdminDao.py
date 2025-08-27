from abc import ABC, abstractmethod
from typing import List
from models.admin_models.staff import Staff

class AdminDaoService(ABC):
    @abstractmethod
    def view_all_staff(self)->List[Staff]:
        ''' fetch all staff'''
        pass

    @abstractmethod
    def add_staff(self, staff: Staff)->str:
        ''' insert a staff details to db'''
        pass

    @abstractmethod
    def find_by_staff_id(self,staff_id:str)->Staff:
        '''find a staff by ID'''
        pass
    
    @abstractmethod
    def update_staff(self,staff:Staff)->bool:
        '''update a staff by its ID'''
        pass

    @abstractmethod
    def disable_staff(self,staff_id:str)->bool:
        '''disable a staff by its ID'''
        pass