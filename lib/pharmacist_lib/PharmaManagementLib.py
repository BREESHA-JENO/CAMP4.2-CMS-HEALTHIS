import uuid
from models.pharmacist import Pharmacist
from dao.pharmacist.ABstractPharmaImple import Medicine

class PharmacistLib:
    dao = Medicine()

    @staticmethod
    def generate_id():
        return "MED-" + str(uuid.uuid4())[:8]

    @staticmethod
    def add_medicine(name, category, price, stock_qty):
        med_id = PharmacistLib.generate_id()
        medicine = Medicine(med_id, name, category, price, stock_qty)
        PharmacistLib.dao.add_medicine(medicine)
        return med_id

    @staticmethod
    def list_medicines():
        return PharmacistLib.dao.list_medicines()

    @staticmethod
    def search_medicine(keyword):
        return PharmacistLib.dao.search_medicine(keyword)

    @staticmethod
    def view_medicine(med_id):
        return PharmacistLib.dao.view_medicine(med_id)

    @staticmethod
    def update_medicine(medicine: Pharmacist):
        PharmacistLib.dao.update_medicine(medicine)

    @staticmethod
    def disable_medicine(med_id):
        PharmacistLib.dao.disable_medicine(med_id)

    @staticmethod
    def update_stock(med_id, delta):
        return PharmacistLib.dao.update_stock(med_id, delta)

    @staticmethod
    def update_price(med_id, new_price):
        PharmacistLib.dao.update_price(med_id, new_price)

    @staticmethod
    def fetch_medicine(med_id):
        return PharmacistLib.dao.fetch_medicine(med_id)
