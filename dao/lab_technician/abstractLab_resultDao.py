from abc import ABC, abstractmethod
from typing import List
from models.lab_technician_models.lab_result import LabResult

class LabResultDaoService(ABC):

    @abstractmethod
    def display_all_results(self) -> List[LabResult]:
        pass

    @abstractmethod
    def insert_result(self, result: LabResult) -> bool:
        pass

    @abstractmethod
    def find_by_result_id(self, result_id: int) -> LabResult:
        pass

    @abstractmethod
    def update_result(self, result: LabResult, result_id: int) -> bool:
        pass
