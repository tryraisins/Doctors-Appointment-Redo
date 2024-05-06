from pydantic import BaseModel
from datetime import datetime


class Patients(BaseModel):
    id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: str

class Doctors(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    is_available: bool = True

class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: datetime
    complete: bool = False

