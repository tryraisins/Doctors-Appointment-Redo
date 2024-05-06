from fastapi import HTTPException
from datetime import datetime
from schemas import Patients, Doctors, Appointment
from database import patients_data, doctors_data, appointment_data


class CRUDService:
    def create_patient(self, patient: Patients):
        if patient.id in patients_data:
            raise HTTPException(status_code=400, detail=f"Patient with id, {patient.id}, already exists")
        patients_data[patient.id] = patient
        return patient
    
    def get_all_patients(self, skip: int = 0, limit: int = 10):
        patients = list(patients_data.values())[skip:skip+limit]
        return patients

    def get_patient(self, patient_id: int):
        patient = patients_data.get(patient_id)
        if patient:
            return patient

        raise HTTPException(status_code=404, detail={"message": f"No Patients Data found for id, {patient_id}"})
    
    def update_patient(self, patient_id: int, patient: Patients):
        if patient_id not in patients_data:
            raise HTTPException(status_code=404, detail=f"No Patients Data found for id, {patient_id}")
        patients_data[patient.id] = patient
        return patient

    def delete_patient(self, patient_id: int):
        if patient_id not in patients_data:
            raise HTTPException(status_code=404, detail=f"No Patients Data found for id, {patient_id}")
        return patients_data.pop(patient_id)
    
    def create_doctor(self, doctor: Doctors):
        doctors_data[doctor.id] = doctor
        return  doctor

    def get_all_doctors(self, skip: int = 0, limit: int = 10):
        doctors = list(doctors_data.values())[skip:skip+limit]
        return doctors
    
    def update_doctor(self, doctor_id: int, doctor: Doctors):
        if doctor_id not in doctors_data:
            raise HTTPException(status_code=404, detail=f"No doctor data found for id, {doctor_id}")
        doctors_data[doctor_id] = doctor
        return doctor

    def delete_doctor(self, doctor_id: int):
        if doctor_id not in doctors_data:
            raise HTTPException(status_code=404, detail=f"No doctor data found for id, {doctor_id}")
        return doctors_data.pop(doctor_id)
    
    def get_doctor(self, doctor_id: int):
        doctor = doctors_data.get(doctor_id)
        if doctor:
            return doctor

        raise HTTPException(status_code=404, detail={"message": f"No Doctor Data found for id, {doctor_id}"})
    
    def create_appointment(self, patient_id: int, appointment_date: datetime, doctor_type: str):

        if appointment_date.date() < datetime.today():
            raise HTTPException(status_code=400, detail="You cannot set appointments for past dates")

        available_doctors = [doctor for doctor_id, doctor in doctors_data.items() if doctor.is_available and doctor.specialization == doctor_type]
        
        for doctor in available_doctors:
            existing_appointment = next((appointment for appointment in appointment_data.values() if appointment.doctor_id == doctor.id and appointment.date.date() == appointment_date.date() and not appointment.complete), None)
            
            if existing_appointment:
                raise HTTPException(status_code=400, detail=f"Appointment already scheduled with {doctor_type} on {appointment_date:%Y-%m-%d}.")

            new_id = len(appointment_data) + 1
            appointment = Appointment(
                id=new_id,
                patient_id=patient_id,
                doctor_id=doctor.id,
                date=appointment_date
            )
            appointment_data[new_id] = appointment
            return appointment

        
        raise HTTPException(status_code=404, detail=f"No {doctor_type} available for your appointment on {appointment_date:%Y-%m-%d}")

    def complete_appointment(self, appointment_id: int):
        if appointment_id not in appointment_data:
            raise HTTPException(status_code=404, detail=f"No Appointment found with id, {appointment_id}")
        if appointment_data[appointment_id].complete:
            raise HTTPException(status_code=404, detail=f"Appointment with id, {appointment_id}, already marked as completed")

        appointment = appointment_data[appointment_id]
        doctor_id = appointment.doctor_id
        doctor = doctors_data[doctor_id]
        appointment_data[appointment_id].complete = True

    def cancel_appointment(self, appointment_id: int):
        if appointment_id not in appointment_data:
            raise HTTPException(status_code=404, detail=f"No Appointment found with id, {appointment_id}")
        if not appointment_data[appointment_id].complete:
            appointment = appointment_data.pop(appointment_id)
            return
        else:
            raise HTTPException(status_code=404, detail=f"You cannot cancel Completed Appointment")

    def set_doctor_availability(self, doctor_id: int, is_available: bool):
        if doctor_id not in doctors_data:
            raise HTTPException(status_code=404, detail=f"No Doctor with id, {doctor_id}, was found")
        doctors_data[doctor_id].is_available = is_available

crud_service = CRUDService()
