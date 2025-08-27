class Doctor_details:
    def __init__(self, doctor_id=None, staff_id=None, specialization=None, consultation_fee=None,
                 working_days=None, working_hours=None):
        self.doctor_id = doctor_id
        self.staff_id = staff_id
        self.specialization = specialization
        self.consultation_fee = consultation_fee
        self.working_days = working_days
        self.working_hours = working_hours

    @property
    def doctor_id(self):
        return self._doctor_id

    @doctor_id.setter
    def doctor_id(self, doctor_id):
        if doctor_id is not None and not isinstance(doctor_id, int):
            raise ValueError("doctor_id must be an integer")
        self._doctor_id = doctor_id