from datetime import date

class Staff:
    def __init__(self, staff_id=None, staff_name=None, dob=None, gender=None,
                 doj=None, blood_group=None, phone=None, email=None,
                 address=None, role_id=None, status="Active"):
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.dob = dob
        self.gender = gender
        self.doj = doj
        self.blood_group = blood_group
        self.phone = phone
        self.email = email
        self.address = address
        self.role_id = role_id
        self.status = status

    @property
    def staff_id(self):
        return self._staff_id

    @staff_id.setter
    def staff_id(self, staff_id):
        if staff_id is not None and not isinstance(staff_id, int):
            raise ValueError("staff_id must be an integer")
        self._staff_id = staff_id

    @property
    def staff_name(self):
        return self._staff_name

    @staff_name.setter
    def staff_name(self, staff_name):
        if not staff_name or not isinstance(staff_name, str):
            raise ValueError("staff_name must be a non-empty string")
        self._staff_name = staff_name

    @property
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, dob):
        if dob and not isinstance(dob, date):
            raise ValueError("dob must be a date object")
        self._dob = dob

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if gender not in (None, "Male", "Female", "Other"):
            raise ValueError("gender must be Male, Female, or Other")
        self._gender = gender

    @property
    def doj(self):
        return self._doj

    @doj.setter
    def doj(self, doj):
        if doj and not isinstance(doj, date):
            raise ValueError("doj must be a date object")
        self._doj = doj

    @property
    def blood_group(self):
        return self._blood_group

    @blood_group.setter
    def blood_group(self, blood_group):
        valid_groups = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}
        if blood_group and blood_group not in valid_groups:
            raise ValueError("Invalid blood group")
        self._blood_group = blood_group

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        if phone and (not phone.isdigit() or len(phone) < 7):
            raise ValueError("Phone must be numeric and at least 7 digits")
        self._phone = phone

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email and "@" not in email:
            raise ValueError("Invalid email format")
        self._email = email

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if address and not isinstance(address, str):
            raise ValueError("address must be a string")
        self._address = address

    @property
    def role_id(self):
        return self._role_id

    @role_id.setter
    def role_id(self, role_id):
        if role_id is not None and not isinstance(role_id, int):
            raise ValueError("role_id must be an integer")
        self._role_id = role_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status not in ("Active", "Inactive"):
            raise ValueError("status must be Active or Inactive")
        self._status = status

    def __str__(self):
        return f"Staff[{self.staff_id}] {self.staff_name}, Role: {self.role_id}, Status: {self.status}"