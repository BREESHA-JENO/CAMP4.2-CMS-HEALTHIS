class Pharmacist:
    def __init__(self, medicine_id, name, category, price, stock_qty, is_active="Y"):
        self.medicine_id = medicine_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_qty = stock_qty
        self.is_active = is_active

    def __str__(self):
        return (f"ID: {self.medicine_id}, Name: {self.name}, "
                f"Category: {self.category}, Price: {self.price}, "
                f"Stock: {self.stock_qty}, Active: {self.is_active}")
