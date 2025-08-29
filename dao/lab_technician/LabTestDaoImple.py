from dao.lab_technician.AbstractLab_testDao import LabTestDaoService
from db.db_connection import DBConnection
from models.lab_technician_models.lab_test import LabTest
from typing import List
from pymysql.cursors import DictCursor

class LabTestDaoImplementation(LabTestDaoService):
    DISPLAY_ALL = "SELECT * FROM lab_test_master WHERE isActive='Y'"
    INSERT_TEST = "INSERT INTO lab_test_master(lab_test_id,test_name, sampletype, price, isActive, created_at) VALUES(%s,%s,%s,%s,%s,%s)"
    FIND_BY_ID = "SELECT * FROM lab_test_master WHERE lab_test_id=%s"
    UPDATE_TEST = "UPDATE lab_test_master SET test_name=%s, sampletype=%s, price=%s  WHERE lab_test_id=%s"
    DISABLE_TEST = "UPDATE lab_test_master SET isActive='N' WHERE lab_test_id=%s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def generate_labtest_id(self) -> str:
        try:
            cursor = self.conn.cursor()

            # Call the stored procedure
            cursor.callproc('generate_labtest_id', [])
            
            # Get the result set from the stored procedure
            result = cursor.fetchone()
            if result:
                new_id = result[0]  # The first column from the SELECT statement
                print(f"DEBUG generate_labtest_id returned: {new_id}")
                return new_id
            else:
                print("No result returned from generate_labtest_id procedure")
                return None
        except Exception as e:
            print("Error calling stored procedure generate_labtest_id:", e)
            return None
        finally:
            cursor.close()

    def create_labtest(self, test_name, sampletype, price, isActive="Y", created_at=None):
        lab_test_id = self.generate_labtest_id()   # call stored procedure here
        new_test = LabTest(
            lab_test_id=lab_test_id,   # pass generated ID to model
            test_name=test_name,
            price=price,
            sample_type=sampletype,
            isActive=isActive,
            created_at=created_at
        )
        self.insert_test(new_test)
        return new_test




    def display_all_tests(self) -> List[LabTest]:
        tests = []
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.DISPLAY_ALL)
        for row in cursor.fetchall():
            tests.append(LabTest(lab_test_id=row["lab_test_id"], test_name=row["test_name"],
                                sampletype=row["sampletype"],price=row["price"], 
                                 isActive=row["isActive"],created_at=row["created_at"]))
        cursor.close()
        return tests

    def insert_test(self, test: LabTest) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.INSERT_TEST, ( test.get_test_id(), test.get_test_name(),
                                          test.get_sampletype(),test.get_price(),
                                          test.get_isActive(), test.get_created_at()
                                          ))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success

    def find_by_test_id(self, test_id: int):
        cursor = self.conn.cursor(DictCursor)
        cursor.execute(self.FIND_BY_ID, (test_id,))
        row = cursor.fetchone()
        cursor.close()
        return LabTest(lab_test_id=row["lab_test_id"], test_name=row["test_name"],
                      sampletype=row["sampletype"],price=row["price"], 
                       isActive=row["isActive"],created_at=row["created_at"] ) if row else None

    def update_test(self, test: LabTest, test_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.UPDATE_TEST, (test.get_test_name(),test.get_sampletype(), 
                                         test.get_price(), test_id))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success



    def disable_test(self, test: LabTest, test_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(self.DISABLE_TEST, (test_id,))
        self.conn.commit()
        success = cursor.rowcount == 1
        cursor.close()
        return success
