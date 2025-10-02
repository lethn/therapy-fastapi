from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

therapist_patient = Table(
    "therapist_patient",
    Base.metadata,
    Column("therapist_id", Integer, ForeignKey("therapists.id")),
    Column("patient_id", Integer, ForeignKey("patients.id")),
)

class Therapist(Base):
    __tablename__ = "therapists"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    specialty = Column(String, nullable=False)

    patients = relationship("Patient", secondary=therapist_patient, back_populates="therapists")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    therapists = relationship("Therapist", secondary=therapist_patient, back_populates="patients")
