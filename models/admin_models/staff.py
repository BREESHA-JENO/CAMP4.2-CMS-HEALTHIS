from datetime import date

class Staff:
    'Python OOPS applied'
    def __init__(self, staff_id=None, staff_name=None, dob=None, gender=None,
                 doj=None, blood_group=None, phone=None, email=None,
                 address=None, role_id=None, isActive="Y"):
        self.__staff_id=staff_id
        self.__staff_name = staff_name
        self.__dob = dob
        self.__gender = gender
        self.__doj = doj
        self.__blood_group = blood_group
        self.__phone = phone
        self.__email = email
        self.__address = address
        self.__role_id = role_id
        self.__isActive = isActive

    @property
    def staff_id(self):
        return self.__staff_id

    @staff_id.setter
    def staff_id(self, staff_id):
        if staff_id is not None and not isinstance(staff_id, str):
            raise ValueError("staff_id must be a string like AD001, DOC002")
        self.__staff_id = staff_id

    @property
    def staff_name(self):
        return self.__staff_name

    @staff_name.setter
    def staff_name(self, staff_name):
        if not staff_name or not isinstance(staff_name, str):
            raise ValueError("staff_name must be a non-empty string")
        self.__staff_name = staff_name

    @property
    def dob(self):
        return self.__dob

    @dob.setter
    def dob(self, dob):
        if dob and not isinstance(dob, date):
            raise ValueError("dob must be a date object")
        self.__dob = dob

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender):
        if gender not in (None, "Male", "Female", "Other"):
            raise ValueError("gender must be Male, Female, or Other")
        self.__gender = gender

    @property
    def doj(self):
        return self.__doj

    @doj.setter
    def doj(self, doj):
        if doj and not isinstance(doj, date):
            raise ValueError("doj must be a date object")
        self.__doj = doj

    @property
    def blood_group(self):
        return self.__blood_group

    @blood_group.setter
    def blood_group(self, blood_group):
        valid_groups = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}
        if blood_group and blood_group not in valid_groups:
            raise ValueError("Invalid blood group")
        self.__blood_group = blood_group

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        if phone and (not phone.isdigit() or len(phone) < 10):
            raise ValueError("Phone must be numeric and at least 10 digits")
        self.__phone = phone

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if email and "@" not in email:
            raise ValueError("Invalid email format")
        self.__email = email

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        if address and not isinstance(address, str):
            raise ValueError("address must be a string")
        self.__address = address

    @property
    def role_id(self):
        return self.__role_id

    @role_id.setter
    def role_id(self, role_id):
        if role_id is not None and not isinstance(role_id, int):
            raise ValueError("role_id must be an integer")
        self.__role_id = role_id

    @property
    def isActive(self):
        return self.__isActive

    @isActive.setter
    def isActive(self, isActive):
        self.__isActive = isActive

    def __str__(self):
        return f"Staff:{self.__staff_id},Name:{self.__staff_name},gender:{self.__gender},DOJ:{self.__doj},Phone No:{self.__phone},Role: {self.__role_id},IsActive: {self.__isActive}"

print("hello")