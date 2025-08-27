def role_redirect(role_id):
    role_map = {
        1: "Admin",
        2: "Receptionist",
        3: "Doctor",
        4: "Lab Technician",
        5: "Pharmacist"
    }
    return role_map.get(role_id, "Unknown Role")