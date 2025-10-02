from pydantic import BaseModel, Field, ConfigDict

class TherapistInfo(BaseModel):
    id: int
    name: str
    age: int
    specialty: str
    model_config = ConfigDict(from_attributes=True)

class PatientInfo(BaseModel):
    id: int
    name: str
    age: int
    model_config = ConfigDict(from_attributes=True)

class Therapist(TherapistInfo):
    patients: list[PatientInfo] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

class Patient(PatientInfo):
    therapists: list[TherapistInfo] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

class TherapistCreate(BaseModel):
    name: str
    age: int
    specialty: str

class PatientCreate(BaseModel):
    name: str
    age: int
