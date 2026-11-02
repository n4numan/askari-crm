
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Tuition, Lead, Tutor
from schemas import TuitionCreate, TuitionResponse


router = APIRouter(prefix="/api/tuitions", tags=["Tuitions"])


@router.get("/", response_model=List[TuitionResponse])
def get_tuitions(db: Session = Depends(get_db)):
    return db.query(Tuition).order_by(Tuition.id.desc()).all()

@router.get("/{tuition_id}", response_model=TuitionResponse)
def get_tuition(tuition_id: int, db: Session = Depends(get_db)):
    tuition = db.query(Tuition).filter(
        Tuition.id == tuition_id
    ).first()

    if not tuition:
        raise HTTPException(status_code=404, detail="Tuition not found")

    return tuition

@router.post("/", response_model=TuitionResponse, status_code=201)
def create_tuition(data: TuitionCreate, db: Session = Depends(get_db)):
    if not db.query(Lead).filter(Lead.id == data.lead_id).first():
        raise HTTPException(status_code=404, detail="Lead not found")

    if data.tutor_id is not None:
        if not db.query(Tutor).filter(Tutor.id == data.tutor_id).first():
            raise HTTPException(status_code=404, detail="Tutor not found")

    existing = db.query(Tuition).filter(
        Tuition.lead_id == data.lead_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Is lead ki tuition pehle se record hai."
        )

    tuition = Tuition(**data.model_dump())
    db.add(tuition)

    try:
        db.commit()
        db.refresh(tuition)
        return tuition
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Tuition save nahi ho saki."
        )



