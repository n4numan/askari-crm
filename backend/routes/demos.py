from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Demo, Lead, Tutor
from schemas import DemoCreate, DemoUpdate, DemoResponse


router = APIRouter(prefix="/api/demos", tags=["Demos"])


VALID_DEMO_STATUSES = {
    "Scheduled",
    "Rescheduled",
    "Cancelled",
    "Demo Done"
}


# GET ALL DEMOS
@router.get("/", response_model=List[DemoResponse])
def get_demos(db: Session = Depends(get_db)):
    return (
        db.query(Demo)
        .order_by(Demo.id.desc())
        .all()
    )


# GET SINGLE DEMO
@router.get("/{demo_id}", response_model=DemoResponse)
def get_demo(demo_id: int, db: Session = Depends(get_db)):

    demo = db.query(Demo).filter(
        Demo.id == demo_id
    ).first()

    if not demo:
        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    return demo


# CREATE DEMO
@router.post("/", response_model=DemoResponse, status_code=201)
def create_demo(
    data: DemoCreate,
    db: Session = Depends(get_db)
):

    # Check lead
    lead = db.query(Lead).filter(
        Lead.id == data.lead_id
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    # Only New Lead can be scheduled
    if lead.status != "New Lead":
        raise HTTPException(
            status_code=400,
            detail="Only New Lead can be scheduled for a demo"
        )

    # Check tutor
    if data.tutor_id is not None:

        tutor = db.query(Tutor).filter(
            Tutor.id == data.tutor_id
        ).first()

        if not tutor:
            raise HTTPException(
                status_code=404,
                detail="Tutor not found"
            )

        if not tutor.is_active:
            raise HTTPException(
                status_code=400,
                detail="Selected tutor is not active"
            )

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


# UPDATE DEMO
@router.patch("/{demo_id}", response_model=DemoResponse)
def update_demo(
    demo_id: int,
    data: DemoUpdate,
    db: Session = Depends(get_db)
):

    demo = db.query(Demo).filter(
        Demo.id == demo_id
    ).first()

    if not demo:
        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    # Check tutor if provided
    if "tutor_id" in update_data:

        tutor_id = update_data["tutor_id"]

        if tutor_id is not None:

            tutor = db.query(Tutor).filter(
                Tutor.id == tutor_id
            ).first()

            if not tutor:
                raise HTTPException(
                    status_code=404,
                    detail="Tutor not found"
                )

            if not tutor.is_active:
                raise HTTPException(
                    status_code=400,
                    detail="Selected tutor is not active"
                )

    # Update only provided fields
    for key, value in update_data.items():
        setattr(demo, key, value)

    try:
        db.commit()
        db.refresh(demo)

        return demo

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Demo update failed"
        )