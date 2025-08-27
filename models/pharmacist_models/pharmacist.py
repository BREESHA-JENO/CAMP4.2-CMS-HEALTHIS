from typing import Optional

class Medicine:
    def __init__(self, medicine_id: str, medicine_name: str, generic_name: str, expiry_date: Optional[str], price: float):
        self.medicine_id = medicine_id
        self.medicine_name = medicine_name
        self.generic_name = generic_name
        self.expiry_date = expiry_date
        self.price = price

    def __str__(self):
        return (f"[{self.medicine_id}] {self.medicine_name} "
                f"(Generic: {self.generic_name}) | Exp: {self.expiry_date} | Price: {self.price}")

class StockMedicine:
    def __init__(self, stock_id: Optional[int], medicine_id: str, received_date: str, expiry_date: Optional[str], quantity: int, reorder_level: int):
        self.stock_id = stock_id
        self.medicine_id = medicine_id
        self.received_date = received_date
        self.expiry_date = expiry_date
        self.quantity = quantity
        self.reorder_level = reorder_level

    def __str__(self):
        return (f"StockID: {self.stock_id} | Med: {self.medicine_id} | "
                f"Recv: {self.received_date} | Exp: {self.expiry_date} | "
                f"Qty: {self.quantity} | Reorder: {self.reorder_level}")

class Billing:
    def __init__(self, bill_id: Optional[int], prescription_id: int, patient_id: int, medicine_id: str, amount: float, status: str, quantity: int, created_at: Optional[str]):
        self.bill_id = bill_id
        self.prescription_id = prescription_id
        self.patient_id = patient_id
        self.medicine_id = medicine_id
        self.amount = amount
        self.status = status
        self.quantity = quantity
        self.created_at = created_at

    def __str__(self):
        return (f"BillID: {self.bill_id} | Rx: {self.prescription_id} | Patient: {self.patient_id} | "
                f"Med: {self.medicine_id} | Qty: {self.quantity} | Amount: {self.amount} | Status: {self.status}")
