class Doctor:
    def __init__(self, cons_id=None, appointment_id=None, staff_id=None, symptoms=None, diagnosis=None, notes=None, created_at=None):
        self.cons_id = cons_id
        self.appointment_id = appointment_id
        self.staff_id = staff_id
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.notes = notes
        self.created_at = created_at
        
    @property
    def get_cons_id(self):
        return self.cons_id
    @get_cons_id.setter
    def get_cons_id(self, cons_id):
        self.cons_id = cons_id
        
    @property
    def get_appointment_id(self):
        return self.appointment_id
    @get_appointment_id.setter
    def get_appointment_id(self, appointment_id):
        self.appointment_id = appointment_id
        
    @property
    def get_staff_id(self):
        return self.staff_id
    @get_staff_id.setter
    def get_staff_id(self, staff_id):
        self.staff_id = staff_id
        
    @property
    def get_symptoms(self):
        return self.symptoms
    @get_symptoms.setter
    def get_symptoms(self, symptoms):
        self.symptoms = symptoms
        
    @property
    def get_diagnosis(self):
        return self.diagnosis
    @get_diagnosis.setter
    def get_diagnosis(self, diagnosis):
        self.diagnosis = diagnosis
        
    @property
    def get_notes(self):
        return self.notes
    @get_notes.setter
    def get_notes(self, notes):
        self.notes = notes
        
    @property
    def get_created_at(self):
        return self.created_at
    @get_created_at.setter
    def get_created_at(self, created_at):
        self.created_at = created_at
