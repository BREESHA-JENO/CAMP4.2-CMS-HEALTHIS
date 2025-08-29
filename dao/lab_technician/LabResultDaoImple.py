from dao.lab_technician.abstractLab_resultDao import LabResultDaoService
from db.db_connection import DBConnection
from models.lab_technician_models.lab_result import LabResult
from typing import List
from pymysql.cursors import DictCursor

class LabResultDaoImplementation(LabResultDaoService):
    DISPLAY_ALL = """SELECT * FROM lab_result"""
    INSERT_RESULT = """INSERT INTO lab_result(res_id, lab_request_id, staff_id, result_value, normal_range,remarks,created_at)
                       VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    FIND_BY_ID = """SELECT * FROM lab_result WHERE res_id=%s"""
    UPDATE_RESULT = """UPDATE lab_result SET result_value=%s, remarks=%s WHERE res_id=%s"""

    def __init__(self):
        self.conn = DBConnection().get_connection()
    def display_all_results(self) -> List[LabResult]:
        results = []
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.DISPLAY_ALL)
        for row in cursor.fetchall():
            results.append(LabResult(res_id=row["res_id"], lab_request_id=row["lab_request_id"],
                                     lab_test_id=row["lab_test_id"], staff_id=row["staff_id"],
                                     result_value=row["result_value"], normal_range=row["normal_range"],
                                     remarks=row["remarks"], created_at=row["created_at"]))
                                     
        cursor.close()
        return results

    def insert_result(self, result: LabResult) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.INSERT_RESULT, (result.get_lab_request_id(), result.get_lab_test_id(),
                                            result.get_staff_id(), result.get_result_value(),
                                            result.get_normal_range(), result.get_remarks(),
                                            result.get_created_at()))
                                            
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success

    def find_by_result_id(self, result_id: int) -> LabResult:
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.FIND_BY_ID, (result_id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return LabResult(res_id=row["res_id"], lab_request_id=row["lab_request_id"],
                         lab_test_id=row["lab_test_id"], staff_id=row["staff_id"],
                         result_value=row["result_value"], normal_range=row["normalrange"],
                         remarks=row["remarks"], created_at=row["created_at"])
                         

    def update_result(self, result: LabResult, result_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.UPDATE_RESULT, (result.get_result_value(), 
                                            result.get_normal_range(), 
                                            result.get_remarks(), result_id))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success
