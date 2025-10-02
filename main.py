# Run `fastapi dev main.py`
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Create new therapist
@app.post("/therapists", response_model=schemas.Therapist)
def create_therapist(therapist: schemas.TherapistCreate, db: Session = Depends(get_db)):
    db_therapist = models.Therapist(**therapist.model_dump())
    db.add(db_therapist)
    db.commit()
    db.refresh(db_therapist)
    return db_therapist

# Get all therapists
@app.get("/therapists", response_model=list[schemas.Therapist])
def get_all_therapists(db: Session = Depends(get_db)):
    return db.query(models.Therapist).all()

# Get specific therapist by id
@app.get("/therapists/{therapist_id}", response_model=schemas.Therapist)
def get_therapist(therapist_id: int, db: Session = Depends(get_db)):
    therapist = db.get(models.Therapist, therapist_id)
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist

@app.get("/therapists/{therapist_id}/patients", response_model=list[schemas.PatientInfo])
def get_patients_for_therapist(therapist_id: int, db: Session = Depends(get_db)):
    therapist = db.get(models.Therapist, therapist_id)
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist.patients

# Create new patient
@app.post("/patients", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# Get all patients
@app.get("/patients", response_model=list[schemas.Patient])
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()

# Get specific patient by id
@app.get("/patients/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Assign a therapist to a patient
@app.put("/patients/{patient_id}/assign/{therapist_id}", response_model=schemas.Patient)
def assign_therapist(patient_id: int, therapist_id: int, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    therapist = db.get(models.Therapist, therapist_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")

    if therapist not in patient.therapists:
        patient.therapists.append(therapist)
        db.commit()
        db.refresh(patient)

    return patient
