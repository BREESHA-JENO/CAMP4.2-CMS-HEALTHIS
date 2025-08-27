class Admin:
    def __init__(self, staff_id, name, email, role_id):
        self.staff_id = staff_id
        self.name = name
        self.email = email
        self.role_id = role_id

    def __str__(self):
        return f"Admin({self.staff_id}, {self.name}, {self.email}, Role: {self.role_id})"
