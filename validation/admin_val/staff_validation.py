from datetime import datetime, date

def calculate_age(dob: date) -> int:
    """Helper: calculate age from DOB"""
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


def validate_staff_input(name, phone, email, role_id, dob, blood_group):
    # 1. Name Validation
    if not name or not name.isalpha() or len(name) < 3:
        raise ValueError("Staff name must contain only alphabets and be at least 3 letters long")

    # 2. Phone Validation
    if not phone.isdigit() or len(phone) != 10 or phone[0] not in "6789":
        raise ValueError("Phone must be 10 digits and start with 6,7,8 or 9")

    # 3. Email Validation
    if "@" not in email or "." not in email:
        raise ValueError("Invalid email format")

    # 4. Role Validation
    if role_id not in (1, 2, 3, 4, 5):
        raise ValueError("Invalid role ID (must be 1–5)")

    # 5. DOB and Age Validation
    if not isinstance(dob, date):
        raise ValueError("DOB must be a valid date object")

    age = calculate_age(dob)

    if role_id == 3:  # Doctor
        if not (25 < age < 80):
            raise ValueError("Doctor must be above 25 and below 80 years")
    else:  # Other staff
        if not (18 < age < 80):
            raise ValueError("Staff must be above 18 and below 80 years")

    # 6. Blood Group Validation
    valid_groups = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}
    if blood_group not in valid_groups:
        raise ValueError("Invalid blood group")
    return True
