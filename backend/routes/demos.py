
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Demo, Lead, Tutor
from schemas import DemoCreate, DemoResponse

router = APIRouter(prefix="/api/demos", tags=["Demos"])


@router.get("/", response_model=List[DemoResponse])
def get_demos(db: Session = Depends(get_db)):
    return db.query(Demo).order_by(Demo.id.desc()).all()

@router.get("/{demo_id}", response_model=DemoResponse)
def get_demo(demo_id: int, db: Session = Depends(get_db)):
    demo = db.query(Demo).filter(Demo.id == demo_id).first()

    if not demo:
        raise HTTPException(status_code=404, detail="Demo not found")
    return demo


@router.post("/", response_model=DemoResponse, status_code=201)
def create_demo(data: DemoCreate, db: Session = Depends(get_db)):
    if not db.query(Lead).filter(Lead.id == data.lead_id).first():
        raise HTTPException(status_code=404, detail="Lead not found")

    if data.tutor_id is not None:
        if not db.query(Tutor).filter(Tutor.id == data.tutor_id).first():
            raise HTTPException(status_code=404, detail="Tutor not found")
    demo = Demo(**data.model_dump())
    db.add(demo)
    try:
        db.commit()
        db.refresh(demo)
        return demo
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Demo save nahi ho saka. Database error check karein."
        )


@router.patch("/{demo_id}", response_model=DemoResponse)
def update_demo(
    demo_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    demo = db.query(Demo).filter(Demo.id == demo_id).first()

    if not demo:
        raise HTTPException(status_code=404, detail="Demo not found")
    allowed = {
        "tutor_id", "demo_date", "demo_time", "status",
        "parent_confirmed", "tutor_confirmed", "result", "notes"
    }

    for key, value in data.items():
        if key in allowed:
            setattr(demo, key, value)

    try:
        db.commit()
        db.refresh(demo)
        return demo
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Demo update failed")
