from abc import ABC, abstractmethod
from typing import List
from models.admin_models.staff import Staff

class AdminDaoService(ABC):
    @abstractmethod
    def view_all_staff(self)->List[Staff]:
        ''' fetch all staff'''
        pass

    @abstractmethod
    def add_staff(self)->bool:
        ''' insert a staff details to db'''
        pass

    @abstractmethod
    def find_by_staff_id(self,staff_id:int)->Staff:
        '''find a staff by ID'''
        pass
    
    @abstractmethod
    def update_staff(self,staff:Staff,staff_id:int)->bool:
        '''update a staff by its ID'''
        pass

    @abstractmethod
    def disable_staff(self,staff:Staff,staff_id:int)->bool:
        '''disable a staff by its ID'''
        pass

print("hello")