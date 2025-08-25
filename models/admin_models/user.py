from datetime import datetime

class UserCredentials:
    def __init__(self, user_id=None, staff_id=None, username=None, password=None, created_at=None):
        self.user_id = user_id
        self.staff_id = staff_id
        self.username = username
        self.password = password
        self.created_at = created_at

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        if user_id is not None and not isinstance(user_id, int):
            raise ValueError("user_id must be an integer")
        self._user_id = user_id

    @property
    def staff_id(self):
        return self._staff_id

    @staff_id.setter
    def staff_id(self, staff_id):
        if staff_id is not None and not isinstance(staff_id, int):
            raise ValueError("staff_id must be an integer")
        self._staff_id = staff_id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if not username or not isinstance(username, str):
            raise ValueError("username must be a non-empty string")
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        if not password or not isinstance(password, str):
            raise ValueError("password must be a non-empty string")
        self._password = password

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        if created_at and not isinstance(created_at, datetime):
            raise ValueError("created_at must be a datetime object")
        self._created_at = created_at

    def __str__(self):
        return f"User[{self.user_id}] Staff: {self.staff_id}, Username: {self.username}"