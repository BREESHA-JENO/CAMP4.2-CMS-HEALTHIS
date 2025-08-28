from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from models.pharmacist_models.pharmacist import StockMedicine, Medicine

class AbstractPharmacistDao(ABC):
    # ---------- STOCK ----------
    @abstractmethod
    def add_stock(self, stock: StockMedicine) -> Tuple[bool, Optional[str]]: 
        pass

    @abstractmethod
    def list_stock(self) -> List[dict]: 
        pass

    # ---------- MEDICINES ----------
    @abstractmethod
    def add_medicine_from_stock(self, medicine_id: str, medicine_name: str,quantity: int, price: float) -> Tuple[bool, Optional[str]]: 
        pass

    @abstractmethod
    def list_medicines(self) -> List[dict]: 
        pass

    @abstractmethod
    def search_medicine_by_id(self, medicine_id: str) -> Optional[dict]: 
        pass

    @abstractmethod
    def search_medicine_by_name(self, medicine_name: str) -> Optional[dict]: 
        pass

    @abstractmethod
    def update_medicine(self, medicine_id: str, field: str, value) -> Tuple[bool, Optional[str]]: 
        pass

    @abstractmethod
    def disable_medicine(self, medicine_id: str) -> Tuple[bool, Optional[str]]: 
        pass
