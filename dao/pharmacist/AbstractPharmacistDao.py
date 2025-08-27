from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from models.pharmacist_models.pharmacist import StockMedicine, Medicine

class AbstractPharmacistDao(ABC):
    @abstractmethod
    def add_stock(self, stock: StockMedicine) -> Tuple[bool, Optional[str]]: pass
    @abstractmethod
    def list_stock(self) -> List[dict]: pass
    @abstractmethod
    def add_medicine_from_stock(self, medicine_id: str, medicine_name: str,
                                quantity: int, price: float) -> Tuple[bool, Optional[str]]: pass
    @abstractmethod
    def list_medicines(self) -> List[dict]: pass
