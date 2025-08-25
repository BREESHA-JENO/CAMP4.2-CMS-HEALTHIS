from abc import ABC, abstractmethod

class MedicineDAO(ABC):

    @abstractmethod
    def add_medicine(self, medicine):
        pass

    @abstractmethod
    def list_medicines(self):
        pass
