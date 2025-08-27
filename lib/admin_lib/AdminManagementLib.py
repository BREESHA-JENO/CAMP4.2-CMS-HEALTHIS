from dao.admin.AbstractAdminDao import AdminDaoService
from dao.admin.StaffDao import StaffDAO
from dao.admin.UserDao import UserDAO
from dao.admin.DoctorDao import DoctorDAO

from models.admin_models.staff import Staff
from models.admin_models.user import UserCredentials
from models.admin_models.doctor_details import Doctor_details

from validation.admin_val.staff_validation import calculate_age

from datetime import datetime, date


class StaffManagementLib:
    """Handles Staff CRUD logic"""

    dao_service: AdminDaoService = StaffDAO()
    role_map = {1: "Admin", 2: "Receptionist", 3: "Doctor", 4: "Lab Technician", 5: "Pharmacist"}
    valid_blood_groups = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}

    # ---------------- MAIN CRUD ----------------

    @staticmethod
    def display_all():
        staffs = StaffManagementLib.dao_service.view_all_staff()
        for staff in staffs:
            print(staff)

    @staticmethod
    def add_staff():
        staff = Staff()

        # Input collection with validation loops
        staff.role_id = StaffManagementLib._input_role()
        staff.staff_name = StaffManagementLib._input_name()
        staff.dob = StaffManagementLib._input_dob(staff.role_id)
        staff.gender = StaffManagementLib._input_gender()
        staff.doj = StaffManagementLib._input_doj()
        staff.blood_group = StaffManagementLib._input_blood_group()
        staff.phone = StaffManagementLib._input_phone()
        staff.email = StaffManagementLib._input_email()
        staff.address = input("Enter the Address: ")

        # Doctor-specific age check
        if staff.role_id == 3:
            age = calculate_age(staff.dob)
            if not (25 < age < 80):
                print("Doctor age must be between 26 and 79 years. Please start over.")
                return

        # Generate staff_id
        role_name = StaffManagementLib.role_map.get(staff.role_id, "Staff")
        staff.staff_id = StaffManagementLib.dao_service.generate_staff_id(role_name)
        
        # Check if staff_id was generated successfully
        if not staff.staff_id:
            print("Failed to generate staff ID. Please try again.")
            return
            
        staff.isActive = 'Y'

        # Store staff in DB
        result = StaffManagementLib.dao_service.add_staff(staff)
        if not result:
            print("Something went wrong while adding staff.")
            return

        print("Staff added successfully.")

        # If doctor, collect doctor details
        if staff.role_id == 3:
            print("Enter Doctor Specific Details:")
            specialization = input("Enter Specialization: ")
            consultation_fee = StaffManagementLib._input_fee()
            working_days = input("Enter Working Days (e.g. Mon-Fri): ")
            working_hours = input("Enter Working Hours (e.g. 9AM-5PM): ")

            doctor = Doctor_details(
                staff_id=staff.staff_id,
                specialization=specialization,
                consultation_fee=consultation_fee,
                working_days=working_days,
                working_hours=working_hours
            )

            if DoctorDAO().add_doctor(doctor):
                print("Doctor details added successfully.")
            else:
                print("Failed to add doctor details.")
                return

        # Create user credentials for any role
        username = StaffManagementLib._input_username()
        password = StaffManagementLib._input_password()
        user = UserCredentials(
            staff_id=staff.staff_id,
            username=username,
            password=password,
            created_at=datetime.now()
        )
        UserDAO().create_user(user)
        print("User credentials created successfully!")

    @staticmethod
    def find_by_staff_id(staff_id):
        staff = StaffManagementLib.dao_service.find_by_staff_id(staff_id.upper())
        print(staff if staff else "Staff not found.")

    @staticmethod
    def update_staff(staff_id):
        staff = StaffManagementLib.dao_service.find_by_staff_id(staff_id.upper())
        if not staff:
            print("Staff not found.")
            return

        # Update fields (loops ensure correctness)
        staff.staff_name = StaffManagementLib._input_name(default=staff.staff_name)
        staff.gender = StaffManagementLib._input_gender(default=staff.gender)
        staff.dob = StaffManagementLib._input_dob(default=staff.dob)
        staff.doj = StaffManagementLib._input_doj(default=staff.doj)
        staff.blood_group = StaffManagementLib._input_blood_group(default=staff.blood_group)
        staff.phone = StaffManagementLib._input_phone(default=staff.phone)
        staff.email = StaffManagementLib._input_email(default=staff.email)
        staff.address = input(f"Address [{staff.address}]: ") or staff.address
        staff.role_id = StaffManagementLib._input_role(default=staff.role_id)

        # Doctor-specific age check
        if staff.role_id == 3:
            age = calculate_age(staff.dob)
            if not (25 < age < 80):
                print("Doctor age must be between 26 and 79 years. Update cancelled.")
                return

        success = StaffManagementLib.dao_service.update_staff(staff)
        print("Update successful." if success else "Update failed.")

    @staticmethod
    def disable_staff(staff_id):
        result = StaffManagementLib.dao_service.disable_staff(staff_id.upper())
        print("Staff disabled." if result else "Disable failed.")

    # ---------------- VALIDATION HELPERS ----------------

    @staticmethod
    def _input_name(default=None):
        while True:
            val = input(f"Enter Name [{default}]: ") if default else input("Enter Name: ")
            val = val or default
            if val and val.isalpha() and len(val) >= 3:
                return val
            print("Name must contain only alphabets and be at least 3 letters long.")

    @staticmethod
    def _input_dob(role_id, default=None):
        while True:
            prompt = f"Date of Birth (dd/MM/YYYY) [{default.strftime('%d/%m/%Y')}]:" if default else "Date of Birth (dd/MM/YYYY): "
            dob_str = input(prompt) or (default.strftime("%d/%m/%Y") if default else None)
            try:
                dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
                age = calculate_age(dob)

                # Doctor rule
                if role_id == 3:
                    if 25 < age < 80:
                        return dob
                    print("Doctor age must be between 26 and 79 years.")
                    continue

                # Other staff rule
                if 18 < age < 80:
                    return dob
                print("Staff age must be between 19 and 79 years.")
            except Exception:
                print("Invalid date format. Please use dd/MM/YYYY.")


    @staticmethod
    def _input_gender(default=None):
        while True:
            val = input(f"Gender (Male/Female/Other) [{default}]: ") if default else input("Gender (Male/Female/Other): ")
            val = val or default
            if val in ("Male", "Female", "Other"):
                return val
            print("Invalid gender. Enter Male, Female, or Other.")

    @staticmethod
    def _input_doj(default=None):
        while True:
            prompt = f"Date of Joining (dd/MM/YYYY) [{default.strftime('%d/%m/%Y')}]:" if default else "Date of Joining (dd/MM/YYYY): "
            doj_str = input(prompt) or (default.strftime("%d/%m/%Y") if default else None)
            try:
                return datetime.strptime(doj_str, "%d/%m/%Y").date()
            except Exception:
                print("Invalid DOJ format. Please use dd/MM/YYYY.")

    @staticmethod
    def _input_blood_group(default=None):
        while True:
            val = input(f"Blood Group [{default}]: ") if default else input("Blood Group: ")
            val = val or default
            if val in StaffManagementLib.valid_blood_groups:
                return val
            print("Invalid blood group. Choose from:", ", ".join(StaffManagementLib.valid_blood_groups))

    @staticmethod
    def _input_phone(default=None):
        while True:
            val = input(f"Phone [{default}]: ") if default else input("Phone: ")
            val = val or default
            if val and val.isdigit() and len(val) == 10 and val[0] in "6789":
                return val
            print("Phone must be 10 digits and start with 6, 7, 8 or 9.")

    @staticmethod
    def _input_email(default=None):
        while True:
            val = input(f"Email [{default}]: ") if default else input("Email: ")
            val = val or default
            if val and "@" in val and "." in val:
                return val
            print("Invalid email format.")

    @staticmethod
    def _input_role(default=None):
        while True:
            try:
                val = input(f"Role ID (1-Admin,2-Receptionist,3-Doctor,4-Lab,5-Pharma) [{default}]: ") if default else input("Role ID (1-5): ")
                val = int(val or default)
                if val in StaffManagementLib.role_map:
                    return val
            except Exception:
                pass
            print("Invalid role ID. Must be 1–5.")

    @staticmethod
    def _input_fee():
        while True:
            try:
                fee = float(input("Enter Consultation Fee: "))
                if fee >= 100:   # enforce min fee
                    return fee
                print("Consultation fee must be at least 100.")
            except ValueError:
                print("Please enter a valid number for fee.")

    @staticmethod
    def _input_username():
        while True:
            username = input("Enter username for login: ")
            if username and len(username) >= 4:
                return username
            print("Username must be at least 4 characters.")

    @staticmethod
    def _input_password():
        while True:
            password = input("Enter password for login: ")
            if password and len(password) >= 6:
                return password
            print("Password must be at least 6 characters.")


class AdminService:
    """Wrapper for admin-related services"""
    def __init__(self):
        self.admin_dao = StaffDAO()   # use StaffDAO or another proper implementation

    def view_admin(self, staff_id):
        return self.admin_dao.find_by_staff_id(staff_id.upper())
