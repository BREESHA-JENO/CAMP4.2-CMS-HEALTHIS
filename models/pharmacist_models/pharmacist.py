from typing import Optional

class StockMedicine:
    def __init__(self, stock_id: Optional[int] = None,
                 medicine_id: Optional[str] = None,
                 medicine_name: Optional[str] = None,
                 received_date: Optional[str] = None,
                 expiry_date: Optional[str] = None,
                 quantity: int = 0,
                 reorder_level: Optional[int] = None):
        self.stock_id = stock_id
        self.medicine_id = medicine_id
        self.medicine_name = medicine_name
        self.received_date = received_date
        self.expiry_date = expiry_date
        self.quantity = quantity
        self.reorder_level = reorder_level

class Medicine:
    def __init__(self, medicine_auto_id: Optional[int] = None,
                 medicine_id: Optional[str] = None,
                 medicine_name: Optional[str] = None,
                 generic_name: Optional[str] = None,
                 expiry_date: Optional[str] = None,
                 price: float = 0.0):
        self.medicine_auto_id = medicine_auto_id
        self.medicine_id = medicine_id
        self.medicine_name = medicine_name
        self.generic_name = generic_name
        self.expiry_date = expiry_date
        self.price = price
