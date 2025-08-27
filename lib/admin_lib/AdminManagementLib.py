from dao.admin.AbstractAdminDao import AdminDaoService
from dao.admin.StaffDao import StaffDAO
from models.admin_models.staff import Staff
from datetime import datetime, date
from models.admin_models.user import UserCredentials
from dao.admin.UserDao import UserDAO
from validation.admin_val.staff_validation import validate_staff_input


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

        staff_name = input("Enter the Name of the Employee:")
        dob = input("Enter the date of Birth(dd/MM/YYYY):") or date.today()
        if isinstance(dob, str):
            util_date = datetime.strptime(dob, "%d/%m/%Y")
            conv_dob = util_date.date()
        else:
            conv_dob = dob

        gender = input("Enter the Gender:")

        doj = input("Enter the date of Joining(dd/MM/YYYY):") or date.today()
        if isinstance(doj, str):
            util_date = datetime.strptime(doj, "%d/%m/%Y")
            conv_doj = util_date.date()
        else:
            conv_doj = doj

        blood_group = input("Enter the blood Group:")
        phone = input("Enter the Phone Number:")
        email = input("Enter the Email:")
        address = input("Enter the Address:")
        role_id = int(input("Enter the role ID:"))

        # Validate only after all inputs have been collected
        try:
            validate_staff_input(staff_name, phone, email, role_id, conv_dob, blood_group)
        except ValueError as ve:
            print("Validation error:", ve)
            return  # Stop processing

        # Assign validated values
        staff.staff_name = staff_name
        staff.dob = conv_dob
        staff.gender = gender
        staff.doj = conv_doj
        staff.blood_group = blood_group
        staff.phone = phone
        staff.email = email
        staff.address = address
        staff.role_id = role_id

        # Generate staff_id before inserting
        role_map = {
            1: "Admin",
            2: "Receptionist",
            3: "Doctor",
            4: "Lab Technician",
            5: "Pharmacist"
        }
        role_name = role_map.get(role_id, "Staff")
        staff_id = StaffManagementLib.dao_service.generate_staff_id(role_name)
        staff.staff_id = staff_id
        staff.isActive = 'Y'

        if StaffManagementLib.dao_service.add_staff(staff):
            print("added staff successfully....")
            print("Now create user login credentials:")
            username = input("Enter username for login: ")
            password = input("Enter password for login: ")

            print(f"DEBUG: staff_id for new user credentials: {staff.staff_id}")

            user = UserCredentials(
                staff_id=staff.staff_id,
                username=username,
                password=password,  # raw password, will be hashed in UserDAO
                created_at=datetime.now()
            )
            UserDAO().create_user(user)
            print("User credentials created successfully!")
        else:
            print("Something went wrong while adding staff.")


class AdminService:
    def __init__(self):
        self.admin_dao = AdminDaoService()

    def view_admin(self, staff_id):
        return self.admin_dao.get_admin_by_id(staff_id)
