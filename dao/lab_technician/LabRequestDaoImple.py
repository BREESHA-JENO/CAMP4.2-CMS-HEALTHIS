from dao.lab_technician.abstractLab_requestDao import LabRequestDaoService
from db.db_connection import DBConnection
from models.lab_technician_models.lab_request import LabRequest
from models.lab_technician_models.lab_test import LabTest
from typing import List
from pymysql.cursors import DictCursor


class LabRequestDaoImplementation(LabRequestDaoService):
    DISPLAY_ALL = """SELECT * FROM lab_request"""
    INSERT_REQUEST = """INSERT INTO lab_request(consultation_id, patient_id, test_id_doc, staff_id, status, created_at) 
                        VALUES(%s,%s,%s,%s,%s,%s)"""
    FIND_BY_ID = """SELECT * FROM lab_request WHERE lab_request_id=%s"""
    UPDATE_REQUEST = """UPDATE lab_request SET status=%s WHERE lab_request_id=%s"""
    FIND_TESTS_FOR_REQUEST = """SELECT t.* FROM lab_tests t 
                                JOIN lab_request_tests r ON t.test_id=r.test_id 
                                WHERE r.request_id=%s"""

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def display_all_requests(self) -> List[LabRequest]:
        requests = []
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.DISPLAY_ALL)
        rows = cursor.fetchall()
        for row in rows:
            req = LabRequest(
                lab_request_id=row["lab_request_id"],
                consultation_id=row["consultation_id"],
                patient_id=row["patient_id"],
                test_id_doc=row["test_id_doc"],
                staff_id=row["staff_id"],
                status=row["status"],
                created_at=row["created_at"]
            )
            requests.append(req)
        cursor.close()
        return requests

    def insert_request(self, req: LabRequest) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.INSERT_REQUEST, (
            req.get_consultation_id(),
            req.get_patient_id(),
            req.get_test_id_doc(),
            req.get_staff_id(),
            req.get_status(),
            req.get_created_datetime()
        ))
        request_id = cursor.lastrowid
        self.conn.commit()
        success = request_id is not None
        cursor.close()
        return success

    def find_by_request_id(self, request_id: int) -> LabRequest:
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.FIND_BY_ID, (request_id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        req = LabRequest(
            lab_request_id=row["lab_request_id"],
            consultation_id=row["consultation_id"],
            patient_id=row["patient_id"],
            test_id_doc=row["test_id_doc"],
            staff_id=row["staff_id"],
            status=row["status"],
            created_at=row["created_at"]
        )
        return req

    def update_request(self, req: LabRequest, request_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.UPDATE_REQUEST, (req.get_status(), request_id))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success
