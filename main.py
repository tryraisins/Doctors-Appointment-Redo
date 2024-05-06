from fastapi import FastAPI
from datetime import datetime
from crud import crud_service
from schemas import Patients, Doctors, Appointment

app = FastAPI()


@app.post("/patients", response_model=Patients)
def create_patient(patient: Patients):
    patient_saved = crud_service.create_patient(patient)
    print(f"message: Patient Data created successfully! \n data: ${patient_saved}")
    return {"message": "Patient Data created successfully!", "data": patient_saved}



@app.get("/patients", response_model=list[Patients])
def get_all_patients(skip: int = 0, limit: int = 10):
    patients = crud_service.get_all_patients(skip, limit)
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    patient = crud_service.get_patient(patient_id)
    return patient


@app.put("/patients/{patient_id}", response_model=Patients)
def update_patient(patient_id: int, patient: Patients):
    patient = crud_service.update_patient(patient_id, patient)
    return {"message": "Patient Data updated successfully", "data": patient}


@app.delete("/patients/{patient_id}", response_model=Patients)
def delete_patient(patient_id: int):
    crud_service.delete_patient(patient_id)
    return {"message": "Patient Data deleted successfully"}

@app.post("/doctors", response_model=Doctors)
def create_doctor(doctor: Doctors):
    doctor = crud_service.create_doctor(doctor)
    return {"message": "Doctor Data created successfully!", "data": doctor}



@app.get("/doctors", response_model=list[Doctors])
def get_all_doctors(skip: int = 0, limit: int = 10):
    doctors = crud_service.get_all_doctors(skip, limit)
    return doctors

@app.get("/doctors/{doctor_id}", response_model=Doctors)
def get_doctor(doctor_id: int):
    doctor = crud_service.get_doctor(doctor_id)
    return doctor

@app.put("/doctors/{doctor_id}", response_model=Doctors)
def update_doctor(doctor_id: int, doctor: Doctors):
    doctor = crud_service.update_doctor(doctor_id, doctor)
    return {"message": "Doctor Data updated successfully", "data": doctor}


@app.delete("/doctors/{doctor_id}", response_model=Doctors)
def delete_doctor(doctor_id: int):
      crud_service.delete_doctor(doctor_id)
      return {"message": "Doctor Data deleted successfully"}

@app.post("/appointments", response_model=Appointment)
def create_appointment(patient_id: int, appointment_date: datetime, doctor_type: str):
    appointment = crud_service.create_appointment( patient_id, appointment_date, doctor_type)
    return {"message": "Appointment created successfully!", "data": appointment}

    

@app.put("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int):
    crud_service.update_patient(appointment_id)
    return {"message": "Appointment marked as Completed"}

@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int):
    crud_service.cancel_appointment(appointment_id)
    return {"message": "Appointment canceled"}
    

@app.put("/doctors/{doctor_id}/availability")
def set_doctor_availability(doctor_id: int, is_available: bool):
    crud_service.set_doctor_availability(doctor_id, is_available)
    return {"message": "Doctor availability updated"}
