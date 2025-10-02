from database import Base, engine, SessionLocal
from models import Therapist, Patient

# Reset & create tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create therapists and patients
therapist1 = Therapist(name="Alice", age=40, specialty="Physical Therapy")
therapist2 = Therapist(name="Bob", age=35, specialty="Speech Therapy")
therapist3 = Therapist(name="Carol", age=45, specialty="Occupational Therapy")
patient1 = Patient(name="John Doe", age=30)
patient2 = Patient(name="Mary Smith", age=25)
patient3 = Patient(name="David Johnson", age=50)

# Link many-to-many
therapist1.patients.append(patient1)
therapist1.patients.append(patient2)
therapist2.patients.append(patient1)
therapist3.patients.append(patient3)

db.add_all([therapist1, therapist2, therapist3, patient1, patient2, patient3])
db.commit()

therapists = db.query(Therapist).all()
for t in therapists:
    print("\nTherapist:", t.name)
    print("Patients:")
    for p in t.patients:
        print(" -", p.name)

patients = db.query(Patient).all()
for p in patients:
    print("\nPatient:", p.name)
    print("Therapists:")
    for t in p.therapists:
        print(" -", t.name)

db.close()
