from abc import ABC, abstractmethod
from models.pharmacist import Pharmacist

class MedicineDAO(ABC):

    @abstractmethod
    def add_medicine(self, medicine: Pharmacist):
        pass

    @abstractmethod
    def list_medicines(self):
        pass

    @abstractmethod
    def search_medicine(self, keyword: str):
        pass

    @abstractmethod
    def view_medicine(self, medicine_id: str):
        pass

    @abstractmethod
    def update_medicine(self, medicine: Pharmacist):
        pass

    @abstractmethod
    def disable_medicine(self, medicine_id: str):
        pass

    @abstractmethod
    def update_stock(self, medicine_id: str, delta: int):
        pass

    @abstractmethod
    def update_price(self, medicine_id: str, new_price: float):
        pass

    @abstractmethod
    def fetch_medicine(self, medicine_id: str):
        """Decrease stock by 1 and return updated medicine or message if unavailable"""
        pass
