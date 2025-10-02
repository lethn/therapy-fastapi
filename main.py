# Run `fastapi dev main.py`
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Therapist(BaseModel):
    id: int
    name: str
    age: int
    specialty: str
    list_of_patients: list[int] = []

class Patient(BaseModel):
    id: int
    name: str
    age: int
    list_of_therapists: list[int] = []

therapist_list = {
    1: Therapist(id=1, name="Alice", age=40, specialty="Physical Therapy", list_of_patients=[101, 102]),
    2: Therapist(id=2, name="Bob", age=35, specialty="Speech Therapy", list_of_patients=[101]),
    3: Therapist(id=3, name="Carol", age=45, specialty="Occupational Therapy", list_of_patients=[]),
}

patient_list = {
    101: Patient(id=101, name="John Doe", age=30, list_of_therapists=[1, 2]),
    102: Patient(id=102, name="Mary Smith", age=25, list_of_therapists=[1]),
    103: Patient(id=103, name="David Johnson", age=50, list_of_therapists=[]),
}

# Create new therapist
@app.post("/therapists", response_model=Therapist)
async def create_therapist(therapist: Therapist):
    if therapist.id in therapist_list:
        raise HTTPException(status_code=400, detail="Therapist already exists")
    therapist_list[therapist.id] = therapist
    return therapist

# Get all therapists
@app.get("/therapists")
async def get_all_therapists():
    return therapist_list

# Get specific therapist by id
@app.get("/therapists/{therapist_id}")
async def get_therapist(therapist_id: int):
    if therapist_id not in therapist_list:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist_list[therapist_id]

# Get all patients from specific therapist
@app.get("/therapists/{therapist_id}/patients")
async def get_patients_for_therapist(therapist_id: int):
    if therapist_id not in therapist_list:
        raise HTTPException(status_code=404, detail="Therapist not found")
    
    patients_array = []
    patient_id_list = therapist_list[therapist_id].list_of_patients
    for patient_id in patient_id_list:
        if patient_id in patient_list:
            patient = patient_list[patient_id]
            patients_array.append({
                "id": patient.id,
                "name": patient.name,
                "age": patient.age
            })

    return patients_array

# Create new patient
@app.post("/patients", response_model=Patient)
async def create_patient(patient: Patient):
    if patient.id in patient_list:
        raise HTTPException(status_code=400, detail="Patient already exists")
    patient_list[patient.id] = patient
    return patient

# Get all patients
@app.get("/patients")
async def get_all_patients():
    return patient_list

# Get specific patient by id
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    if patient_id not in patient_list:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_list[patient_id]

# Assign a theparist to a patient
@app.put("/patients/{patient_id}/assign/{therapist_id}", response_model=Patient)
async def assign_therapist(patient_id: int, therapist_id: int):
    if patient_id not in patient_list:
        raise HTTPException(status_code=404, detail="Patient not found")
    if therapist_id not in therapist_list:
        raise HTTPException(status_code=404, detail="Therapist not found")
    
    patient = patient_list[patient_id]
    if therapist_id not in patient.list_of_therapists:
        patient.list_of_therapists.append(therapist_id)

    therapist = therapist_list[therapist_id]
    if patient_id not in therapist.list_of_patients:
        therapist.list_of_patients.append(patient_id)
    
    return patient
