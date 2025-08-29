# models/doctor_models/appointment.py

class Appointment:
    def __init__(self, appointment_id=None, staff_id=None, patient_id=None, date=None, time=None, status=None, created_at=None):
        self.__appointment_id = appointment_id
        self.__staff_id = staff_id
        self.__patient_id = patient_id
        self.__date = date
        self.__time = time
        self.__status = status
        self.__created_at = created_at

    @property
    def appointment_id(self):
        return self.__appointment_id

    @appointment_id.setter
    def appointment_id(self, value):
        self.__appointment_id = value

    @property
    def staff_id(self):
        return self.__staff_id

    @staff_id.setter
    def staff_id(self, value):
        self.__staff_id = value

    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        self.__created_at = value

    def __str__(self):
        return f"Appointment ID: {self.__appointment_id}, Patient ID: {self.__patient_id}, Staff ID: {self.__staff_id}, Date: {self.__date}, Time: {self.__time}, Status: {self.__status}, Created At: {self.__created_at}"
