from abc import ABC, abstractmethod
from typing import List
from models.lab_technician_models.lab_bill import Billing

class BillingDaoService(ABC):

    @abstractmethod
    def display_all_bills(self) -> List[Billing]:
        pass

    @abstractmethod
    def insert_bill(self, bill: Billing) -> bool:
        pass

    @abstractmethod
    def find_by_bill_id(self, bill_id: int) -> Billing:
        pass

    @abstractmethod
    def update_bill(self, bill: Billing, bill_id: int) -> bool:
        pass
