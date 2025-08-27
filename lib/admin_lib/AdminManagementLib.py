from dao.admin.AbstractAdminDao import AdminDaoService
from dao.admin.StaffDao import StaffDAO
from models.admin_models.staff import Staff
from datetime import datetime, date
from models.admin_models.user import UserCredentials
from dao.admin.UserDao import UserDAO
from validation.admin_val.staff_validation import validate_staff_input,calculate_age


class StaffManagementLib:
    'handles CRUD logic'

    dao_service: AdminDaoService = StaffDAO()

    @staticmethod
    def display_all():
        staffs = StaffManagementLib.dao_service.view_all_staff()
        for staff in staffs:
            print(staff)

    @staticmethod
    def add_staff():
        staff = Staff()

        # staff_name input validation loop
        while True:
            staff_name = input("Enter the Name of the Employee: ")
            try:
                # minimal validation for name only here
                if not staff_name or not staff_name.isalpha() or len(staff_name) < 3:
                    raise ValueError("Staff name must contain only alphabets and be at least 3 letters long")
            except ValueError as ve:
                print(f"Validation error: {ve}. Please try again.")
                continue
            break

        # dob input validation loop
        while True:
            dob_str = input("Enter the date of Birth (dd/MM/YYYY): ") or date.today().strftime("%d/%m/%Y")
            try:
                dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
                age = calculate_age(dob)

                # Role unknown yet, so just check general age 18-80 now
                if not (18 < age < 80):
                    raise ValueError("Age must be between 18 and 80 years")
            except ValueError as ve:
                print(f"Validation error: {ve}. Please try again.")
                continue
            break

        # gender input - simple, no validation loop shown but can be added similarly
        gender = input("Enter the Gender (Male/Female/Other): ")

        # doj input validation loop
        while True:
            doj_str = input("Enter the date of Joining (dd/MM/YYYY): ") or date.today().strftime("%d/%m/%Y")
            try:
                doj = datetime.strptime(doj_str, "%d/%m/%Y").date()
            except ValueError as ve:
                print(f"Invalid date format: {ve}. Please try again.")
                continue
            break

        # blood_group validation loop
        valid_blood_groups = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}
        while True:
            blood_group = input("Enter the Blood Group: ")
            if blood_group not in valid_blood_groups:
                print("Invalid blood group, please enter one of:", ", ".join(valid_blood_groups))
                continue
            break

        # phone input validation loop
        while True:
            phone = input("Enter the Phone Number: ")
            if not (phone.isdigit() and len(phone) == 10 and phone[0] in "6789"):
                print("Phone must be 10 digits and start with 6, 7, 8 or 9. Please try again.")
                continue
            break

        # email input validation loop
        while True:
            email = input("Enter the Email: ")
            if "@" not in email or "." not in email:
                print("Invalid email format. Please try again.")
                continue
            break

        # address input (optional, no validation here)
        address = input("Enter the Address: ")

        # role_id input validation loop
        valid_roles = {1, 2, 3, 4, 5}
        while True:
            try:
                role_id = int(input("Enter the Role ID (1-Admin, 2-Receptionist, 3-Doctor, 4-Lab Technician, 5-Pharmacist): "))
                if role_id not in valid_roles:
                    raise ValueError("Role ID must be between 1 and 5")
            except ValueError as ve:
                print(f"Invalid role ID: {ve}. Please try again.")
                continue
            break

        # Additional validation for doctor age if role is doctor
        if role_id == 3:
            age = calculate_age(dob)
            if not (25 < age < 80):
                print("Doctor age must be between 26 and 79 years. Please start over.")
                return

        # Assign validated fields to staff model
        staff.staff_name = staff_name
        staff.dob = dob
        staff.gender = gender
        staff.doj = doj
        staff.blood_group = blood_group
        staff.phone = phone
        staff.email = email
        staff.address = address
        staff.role_id = role_id

        # Generate staff_id using role_name map
        role_map = {1: "Admin", 2: "Receptionist", 3: "Doctor", 4: "Lab Technician", 5: "Pharmacist"}
        role_name = role_map.get(role_id, "Staff")
        staff_id = StaffManagementLib.dao_service.generate_staff_id(role_name)
        staff.staff_id = staff_id
        staff.isActive = 'Y'

        # Store staff in database
        if StaffManagementLib.dao_service.add_staff(staff):
            print("Added staff successfully.")
            print("Now create user login credentials:")
            username = input("Enter username for login: ")
            password = input("Enter password for login: ")

            user = UserCredentials(
                staff_id=staff.staff_id,
                username=username,
                password=password,  # will be hashed in UserDAO
                created_at=datetime.now()
            )
            UserDAO().create_user(user)
            print("User credentials created successfully!")
        else:
            print("Something went wrong while adding staff.")

    
    @staticmethod
    def find_by_staff_id(staff_id):
        staff_id=staff_id.upper()
        staff = StaffManagementLib.dao_service.find_by_staff_id(staff_id)
        if staff:
            print(staff)
        else:
            print("Staff not found.")

    @staticmethod
    def update_staff(staff_id):
        staff_id=staff_id.upper()
        staff = StaffManagementLib.dao_service.find_by_staff_id(staff_id)
        if not staff:
            print("Staff not found.")
            return

        # Update staff_name with validation
        while True:
            staff_name = input(f"Staff Name [{staff.staff_name}]: ") or staff.staff_name
            if staff_name.isalpha() and len(staff_name) >= 3:
                staff.staff_name = staff_name
                break
            else:
                print("Name must contain only alphabets and be at least 3 letters long. Please try again.")

        # Update gender (simple check)
        gender = input(f"Gender [{staff.gender}]: ") or staff.gender
        if gender in ("Male", "Female", "Other"):
            staff.gender = gender
        else:
            print(f"Invalid gender input, keeping existing value: {staff.gender}")

        # Update dob with validation
        while True:
            dob_str = input(f"Date of Birth (dd/MM/YYYY) [{staff.dob.strftime('%d/%m/%Y')}]: ") or staff.dob.strftime('%d/%m/%Y')
            try:
                dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
                age = calculate_age(dob)
                if not (18 < age < 80):
                    print("Age must be between 18 and 80 years. Please try again.")
                    continue
                staff.dob = dob
                break
            except ValueError:
                print("Invalid date format. Please try again.")

        # Update doj with validation
        while True:
            doj_str = input(f"Date of Joining (dd/MM/YYYY) [{staff.doj.strftime('%d/%m/%Y')}]: ") or staff.doj.strftime('%d/%m/%Y')
            try:
                doj = datetime.strptime(doj_str, "%d/%m/%Y").date()
                staff.doj = doj
                break
            except ValueError:
                print("Invalid date format. Please try again.")

        # Update blood group with validation
        valid_blood_groups = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}
        while True:
            blood_group = input(f"Blood Group [{staff.blood_group}]: ") or staff.blood_group
            if blood_group in valid_blood_groups:
                staff.blood_group = blood_group
                break
            else:
                print("Invalid blood group. Please try again.")

        # Update phone with validation
        while True:
            phone = input(f"Phone Number [{staff.phone}]: ") or staff.phone
            if phone.isdigit() and len(phone) == 10 and phone[0] in "6789":
                staff.phone = phone
                break
            else:
                print("Phone must be 10 digits and start with 6, 7, 8 or 9. Please try again.")

        # Update email with validation
        while True:
            email = input(f"Email [{staff.email}]: ") or staff.email
            if "@" in email and "." in email:
                staff.email = email
                break
            else:
                print("Invalid email format. Please try again.")

        # Update address (optional)
        address = input(f"Address [{staff.address}]: ") or staff.address
        staff.address = address

        # Update role_id with validation
        valid_roles = {1, 2, 3, 4, 5}
        while True:
            role_input = input(f"Role ID [{staff.role_id}]: ") or str(staff.role_id)
            try:
                role_id = int(role_input)
                if role_id in valid_roles:
                    staff.role_id = role_id
                    break
                else:
                    print("Role ID must be between 1 and 5. Please try again.")
            except ValueError:
                print("Invalid role ID. Please enter a number between 1 and 5.")

        # Additional doctor age check if role is doctor
        if staff.role_id == 3:
            age = calculate_age(staff.dob)
            if not (25 < age < 80):
                print("Doctor age must be between 26 and 79 years. Update cancelled.")
                return

        # Save updated staff to DB
        success = StaffManagementLib.dao_service.update_staff(staff)
        print("Update successful." if success else "Update failed.")


    @staticmethod
    def disable_staff(staff_id):
        staff_id=staff_id.upper()
        result = StaffManagementLib.dao_service.disable_staff(staff_id)
        print("Staff disabled." if result else "Disable failed.")



class AdminService:
    def __init__(self):
        self.admin_dao = AdminDaoService()

    def view_admin(self, staff_id):
        return self.admin_dao.get_admin_by_id(staff_id)

print("hello")