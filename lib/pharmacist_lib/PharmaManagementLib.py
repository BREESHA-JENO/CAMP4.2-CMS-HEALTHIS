from dao.pharmacist.ABstractPharmaImple import PharmacistDaoImpl
from validation.pharmacist_val.pharmacistValidation import validate_stock_input, validate_medicine_input
from models.pharmacist_models.pharmacist import StockMedicine

class PharmaManagementLib:
    def __init__(self):
        self.dao = PharmacistDaoImpl()

    # ---------- STOCK ----------
    def add_stock(self, medicine_name, received_date, expiry_date, quantity, reorder_level=None):
        ok, msg = validate_stock_input(medicine_name, received_date, expiry_date, quantity)
        if not ok:
            return False, msg
        stock = StockMedicine(medicine_name=medicine_name, received_date=received_date,
                              expiry_date=expiry_date, quantity=quantity, reorder_level=reorder_level)
        return self.dao.add_stock(stock)

    def list_stock(self):
        return self.dao.list_stock()

    # ---------- MEDICINES ----------
    def add_medicine_from_stock(self, medicine_id, medicine_name,generic_name, quantity, price):
        ok, msg = validate_medicine_input(medicine_id, quantity, price)
        if not ok:
            return False, msg
        return self.dao.add_medicine_from_stock(medicine_id, medicine_name,generic_name, quantity, price)

    def list_medicines(self):
        return self.dao.list_medicines()
