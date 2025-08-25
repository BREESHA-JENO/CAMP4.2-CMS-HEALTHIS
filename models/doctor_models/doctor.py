class Consultation:
    def __init__(self, consultation_id=None, appointment_id=None, staff_id=None, symptoms=None, diagnosis=None, notes=None, created_at=None):
        self.consultation_id = consultation_id
        self.appointment_id = appointment_id
        self.staff_id = staff_id
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.notes = notes
        self.created_at = created_at
        
    @property
    def get_consultation_id(self):
        return self.consultation_id
    @get_consultation_id.setter
    def get_consultation_id(self, consultation_id):
        self.consultation_id = consultation_id
        
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
