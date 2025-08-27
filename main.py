from lib.doctor_lib.DoctorManagementLib import DoctorManagementLib

def main():
       
    while True:
        print("==========welcome to doctor dashboard==========")
        print("1. list appoinment")
        print("2. prescribe medicine")
        print("3. priscription for lab")        
        choice = input("enter your choice")
        if choice == "1":
            DoctorManagementLib.display_all()

if __name__=="__main__":
    main()
    print("hello")



            
        
        
    