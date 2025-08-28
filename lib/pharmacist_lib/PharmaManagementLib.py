from dao.pharmacist.ABstractPharmaImple import PharmacistDaoImpl
from pymysql.cursors import DictCursor
from db.db_connection import DBConnection
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
        # Call the DAO method to get the data
        rows = self.dao.list_stock()
        
        # Format the output in table format
        if not rows:
            return "No stock items found."
        
        # Create header
        formatted_output = []
        formatted_output.append(f"{'ID':<4} {'Med_ID':<8} {'Name':<20} {'Received':<12} {'Expiry':<12} {'Qty':<6} {'Reorder':<8}")
        formatted_output.append("-" * 75)
        
        # Add rows
        for row in rows:
            received = row['received_date'].strftime('%Y-%m-%d') if row['received_date'] else 'N/A'
            expiry = row['expiry_date'].strftime('%Y-%m-%d') if row['expiry_date'] else 'N/A'
            reorder = row['reorder_level'] if row['reorder_level'] is not None else '-'
            
            formatted_output.append(
                f"{row['stock_id']:<4} {row['medicine_id']:<8} {row['medicine_name'][:18]:<20} "
                f"{received:<12} {expiry:<12} {row['quantity']:<6} {reorder:<8}"
            )
        
        return "\n".join(formatted_output)

    def list_medicines(self):
        # Call the DAO method to get the data
        rows = self.dao.list_medicines()
        
        # Format the output in table format
        if not rows:
            return "No medicines found."
        
        # Create header
        formatted_output = []
        formatted_output.append(f"{'ID':<4} {'Med_ID':<8} {'Name':<20} {'Generic':<15} {'Expiry':<12} {'Price':<8} {'Status':<10}")
        formatted_output.append("-" * 80)
        
        # Add rows
        for row in rows:
            expiry = row['expiry_date'].strftime('%Y-%m-%d') if row['expiry_date'] else 'N/A'
            status = row.get('status', 'active')
            generic_name = row.get('generic_name', 'N/A')[:13] if row.get('generic_name') else 'N/A'
            
            formatted_output.append(
                f"{row['medicine_auto_id']:<4} {row['medicine_id']:<8} {row['medicine_name'][:18]:<20} "
                f"{generic_name:<15} {expiry:<12} ${row['price']:<7.2f} {status:<10}"
            )
        
        return "\n".join(formatted_output)

    # ---------- SEARCH MEDICINES (Formatted) ----------
    def search_medicine_by_id(self, med_id):
        medicine = self.dao.search_medicine_by_id(med_id)
        if not medicine:
            return "Medicine not found."
        
        # Create header
        formatted_output = []
        formatted_output.append(f"{'ID':<4} {'Med_ID':<8} {'Name':<20} {'Generic':<15} {'Expiry':<12} {'Price':<8} {'Status':<10}")
        formatted_output.append("-" * 80)
        
        # Add the single medicine row
        expiry = medicine['expiry_date'].strftime('%Y-%m-%d') if medicine['expiry_date'] else 'N/A'
        status = medicine.get('status', 'active')
        generic_name = medicine.get('generic_name', 'N/A')[:13] if medicine.get('generic_name') else 'N/A'
        
        formatted_output.append(
            f"{medicine['medicine_auto_id']:<4} {medicine['medicine_id']:<8} {medicine['medicine_name'][:18]:<20} "
            f"{generic_name:<15} {expiry:<12} ${medicine['price']:<7.2f} {status:<10}"
        )
        
        return "\n".join(formatted_output)

    def search_medicine_by_name(self, med_name):
        medicine = self.dao.search_medicine_by_name(med_name)
        if not medicine:
            return "Medicine not found."
        
        # Create header
        formatted_output = []
        formatted_output.append(f"{'ID':<4} {'Med_ID':<8} {'Name':<20} {'Generic':<15} {'Expiry':<12} {'Price':<8} {'Status':<10}")
        formatted_output.append("-" * 80)
        
        # Add the single medicine row
        expiry = medicine['expiry_date'].strftime('%Y-%m-%d') if medicine['expiry_date'] else 'N/A'
        status = medicine.get('status', 'active')
        generic_name = medicine.get('generic_name', 'N/A')[:13] if medicine.get('generic_name') else 'N/A'
        
        formatted_output.append(
            f"{medicine['medicine_auto_id']:<4} {medicine['medicine_id']:<8} {medicine['medicine_name'][:18]:<20} "
            f"{generic_name:<15} {expiry:<12} ${medicine['price']:<7.2f} {status:<10}"
        )
        
        return "\n".join(formatted_output)

    # ---------- MEDICINES ----------
    def add_medicine_from_stock(self, medicine_id, medicine_name, generic_name, quantity, price):
        ok, msg = validate_medicine_input(medicine_id, quantity, price)
        if not ok:
            return False, msg
        return self.dao.add_medicine_from_stock(medicine_id, medicine_name, generic_name, quantity, price)

    def update_medicine(self, med_id, field, value):
        return self.dao.update_medicine(med_id, field, value)

    def disable_medicine(self, med_id):
        return self.dao.disable_medicine(med_id)