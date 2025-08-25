from dao.pharmacist.ABstractPharmaImple import MedicineDAOMySQL
from models.pharmacist_models.pharmacist import Medicine
import uuid

class PharmaManagementLib:
    dao = MedicineDAOMySQL()

    @staticmethod
    def generate_medicine_id():
        return "MED-" + str(uuid.uuid4())[:8]

    @staticmethod
    def add_medicine(name, category, price, stock_qty):
        med_id = PharmaManagementLib.generate_medicine_id()
        medicine = Medicine(med_id, name, category, price, stock_qty)
        PharmaManagementLib.dao.add_medicine(medicine)
        return medicine

    @staticmethod
    def list_medicines():
        return PharmaManagementLib.dao.list_medicines()
