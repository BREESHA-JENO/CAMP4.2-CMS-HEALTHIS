from dao.pharmacist.AbstractPharmacistDao import MedicineDAO
from db.db_connection import DBConnection
from models.pharmacist_models.pharmacist import Medicine

class MedicineDAOMySQL(MedicineDAO):

    def add_medicine(self, medicine):
        conn = DBConnection().get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO medicines (medicine_id, name, category, price, stock_qty, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            medicine.medicine_id,
            medicine.name,
            medicine.category,
            medicine.price,
            medicine.stock_qty,
            medicine.is_active
        ))
        conn.commit()
        return True

    def list_medicines(self):
        conn = DBConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT medicine_id, name, category, price, stock_qty, is_active FROM medicines")
        rows = cursor.fetchall()

        medicines = []
        for row in rows:
            medicines.append(Medicine(*row))
        return medicines
