from dao.doctor.DoctorDaoImplementation import DoctorDaoImplementation
from dao.doctor.AbstractDoctorDao import DoctorDaoService
from models.doctor_models.doctor import Doctor


class DoctorManagementLib:
    
    'handels crud logic'
    
    dao_service:DoctorDaoService=DoctorDaoImplementation()
    
    @staticmethod
    def display_all():
        doctors = DoctorManagementLib.dao_service.view_all_appointments()
        for doctor in doctors:
            print(doctor)
            