# models/doctor_models/doctor.py

class Doctor:
    def __init__(self, cons_id=None, appointment_id=None, staff_id=None, symptoms=None, diagnosis=None, notes=None, created_at=None):
        self.__cons_id = cons_id
        self.__appointment_id = appointment_id
        self.__staff_id = staff_id
        self.__symptoms = symptoms
        self.__diagnosis = diagnosis
        self.__notes = notes
        self.__created_at = created_at

    @property
    def cons_id(self):
        return self.__cons_id

    @cons_id.setter
    def cons_id(self, value):
        self.__cons_id = value

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
    def symptoms(self):
        return self.__symptoms

    @symptoms.setter
    def symptoms(self, value):
        self.__symptoms = value

    @property
    def diagnosis(self):
        return self.__diagnosis

    @diagnosis.setter
    def diagnosis(self, value):
        self.__diagnosis = value

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, value):
        self.__notes = value

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        self.__created_at = value

    def __str__(self):
        return f"Consultation ID: {self.__cons_id}, Appointment ID: {self.__appointment_id}, Staff ID: {self.__staff_id}, Symptoms: {self.__symptoms}, Diagnosis: {self.__diagnosis}, Notes: {self.__notes}, Date: {self.__created_at}"
