from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas import TutorCreate, TutorResponse
from database import get_db
from models import Tutor

router = APIRouter(
    prefix="/api/tutors",
    tags=["Tutors"]
)


@router.get("/", response_model=List[TutorResponse])
def get_tutors(db: Session = Depends(get_db)):
    return db.query(Tutor).order_by(Tutor.id.desc()).all()


@router.post("/", response_model=TutorResponse, status_code=201)
def create_tutor(tutor: TutorCreate, db: Session = Depends(get_db)):
    new_tutor = Tutor(
        full_name=tutor.full_name,
        phone=tutor.phone,
        email=tutor.email,
        subjects=tutor.subjects,
        areas=tutor.areas,
        monthly_fee=tutor.monthly_fee
    )

    try:
        db.add(new_tutor)
        db.commit()
        db.refresh(new_tutor)
        return new_tutor
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Tutor save nahi ho saka. Database error check karein."
        )


@router.get("/{tutor_id}", response_model=TutorResponse)
def get_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()

    if not tutor:
        raise HTTPException(
            status_code=404,
            detail="Tutor not found"
        )

    return tutor