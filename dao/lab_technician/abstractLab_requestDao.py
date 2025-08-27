from abc import ABC, abstractmethod
from typing import List
from models.lab_technician_models.lab_request import LabRequest

class LabRequestDaoService(ABC):

    @abstractmethod
    def display_all_requests(self) -> List[LabRequest]:
        pass

    @abstractmethod
    def insert_request(self, req: LabRequest) -> bool:
        pass

    @abstractmethod
    def find_by_request_id(self, request_id: int) -> LabRequest:
        pass

    @abstractmethod
    def update_request(self, req: LabRequest, request_id: int) -> bool:
        pass
