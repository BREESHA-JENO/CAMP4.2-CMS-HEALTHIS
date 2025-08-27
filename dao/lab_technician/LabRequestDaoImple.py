from dao.lab_technician.abstractLab_requestDao import LabRequestDaoService
from db.db_connection import DBConnection
from models.lab_technician_models.lab_request import LabRequest
from models.lab_technician_models.lab_test import LabTest
from typing import List
from pymysql.cursors import DictCursor
from datetime import date

class LabRequestDaoImplementation(LabRequestDaoService):
    DISPLAY_ALL = """SELECT * FROM lab_requests"""
    INSERT_REQUEST = """INSERT INTO lab_requests(doctorid, patientid, requestdate, clinicalnotes, status) 
                        VALUES(%s,%s,%s,%s,%s)"""
    FIND_BY_ID = """SELECT * FROM lab_requests WHERE requestid=%s"""
    UPDATE_REQUEST = """UPDATE lab_requests SET status=%s WHERE requestid=%s"""
    # Link table for request <-> tests
    INSERT_REQUEST_TEST = """INSERT INTO lab_request_tests(requestid, testid) VALUES(%s,%s)"""
    FIND_TESTS_FOR_REQUEST = """SELECT t.* FROM lab_tests t 
                                JOIN lab_request_tests r ON t.testid=r.testid 
                                WHERE r.requestid=%s"""

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def display_all_requests(self) -> List[LabRequest]:
        requests = []
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.DISPLAY_ALL)
        rows = cursor.fetchall()
        for row in rows:
            req = LabRequest(request_id=row["requestid"], doctor_id=row["doctorid"],
                             patient_id=row["patientid"], request_date=row["requestdate"],
                             clinical_notes=row["clinicalnotes"], status=row["status"])
            # attach tests
            req_tests = self._fetch_tests_for_request(row["requestid"])
            for t in req_tests:
                req.add_test(t)
            requests.append(req)
        cursor.close()
        return requests

    def insert_request(self, req: LabRequest) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.INSERT_REQUEST, (req.get_doctor_id(), req.get_patient_id(),
                                             req.get_request_date(), req.get_clinical_notes(),
                                             req.get_status()))
        request_id = cursor.lastrowid
        for test in req.get_tests():
            cursor.execute(self.INSERT_REQUEST_TEST, (request_id, test.get_test_id()))
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
        req = LabRequest(request_id=row["requestid"], doctor_id=row["doctorid"],
                         patient_id=row["patientid"], request_date=row["requestdate"],
                         clinical_notes=row["clinicalnotes"], status=row["status"])
        req_tests = self._fetch_tests_for_request(request_id)
        for t in req_tests:
            req.add_test(t)
        return req

    def update_request(self, req: LabRequest, request_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.UPDATE_REQUEST, (req.get_status(), request_id))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success

    def _fetch_tests_for_request(self, request_id: int) -> List[LabTest]:
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.FIND_TESTS_FOR_REQUEST, (request_id,))
        tests = []
        for row in cursor.fetchall():
            tests.append(LabTest(test_id=row["testid"], test_name=row["testname"],
                                 unit_price=row["unitprice"], sample_type=row["sampletype"],
                                 created_date=row["createddate"], is_active=row["isActive"]))
        cursor.close()
        return tests
