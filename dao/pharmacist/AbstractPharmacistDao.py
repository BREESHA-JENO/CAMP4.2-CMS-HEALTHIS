from abc import ABC, abstractmethod
from typing import List, Optional
from models.pharmacist_models.pharmacist import Medicine, StockMedicine, Billing

class MedicineDAO(ABC):

    # -------- Medicine --------
    @abstractmethod
    def add_medicine(self, medicine: Medicine) -> bool:
        pass

    @abstractmethod
    def list_medicines(self) -> List[Medicine]:
        pass

    @abstractmethod
    def search_medicine_by_id(self, medicine_id: str) -> Optional[Medicine]:
        pass

    @abstractmethod
    def search_medicine_by_name(self, name: str) -> List[Medicine]:
        pass

    @abstractmethod
    def update_medicine(self, medicine: Medicine) -> bool:
        """Update name/generic/expiry/price by medicine_id"""
        pass

    # Optional: only if you add an `is_active` column in DB
    @abstractmethod
    def disable_medicine(self, medicine_id: str) -> bool:
        pass

    # -------- Stock --------
    @abstractmethod
    def add_stock(self, stock: StockMedicine) -> bool:
        pass

    @abstractmethod
    def update_stock_quantity(self, medicine_id: str, add_qty: int) -> bool:
        """Increase stock for latest batch (or create a dummy batch)."""
        pass

    @abstractmethod
    def get_total_stock(self, medicine_id: str) -> int:
        pass

    @abstractmethod
    def list_stock_batches(self, medicine_id: str) -> List[StockMedicine]:
        pass


    @abstractmethod
    def update_price(self, medicine_id: str, new_price: float) -> bool:
        pass

    @abstractmethod
    def dispense_and_bill(
        self,
        prescription_id: int,
        patient_id: int,
        medicine_id: str,
        dispense_qty: int,
        bill_status: str = "unpaid"
    ) -> Billing:
        pass
