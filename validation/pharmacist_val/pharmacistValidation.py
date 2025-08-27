from datetime import datetime, date

DATE_FMT = "%Y-%m-%d"

def parse_date(s: str):
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except Exception:
        return None

def validate_stock_input(medicine_name: str, received_date: str, expiry_date: str, quantity: int):
    if not medicine_name.strip():
        return False, "Medicine name required"
    rcv = parse_date(received_date)
    exp = parse_date(expiry_date)
    if not rcv or not exp:
        return False, "Dates must be YYYY-MM-DD"
    if exp <= rcv or exp <= date.today():
        return False, "Expiry must be future date > received date"
    if quantity <= 0:
        return False, "Quantity must be > 0"
    return True, None

def validate_medicine_input(medicine_id: str, quantity: int, price: float):
    if not medicine_id.strip():
        return False, "Medicine ID required"
    if quantity <= 0:
        return False, "Quantity must be > 0"
    if price < 0:
        return False, "Price must be >= 0"
    return True, None
