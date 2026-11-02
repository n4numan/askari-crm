
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import FollowUp, Lead, Tutor
from schemas import FollowUpCreate, FollowUpResponse

router = APIRouter(
    prefix="/api/follow-ups",
    tags=["Follow-ups"]
)


@router.get("/", response_model=List[FollowUpResponse])
def get_follow_ups(db: Session = Depends(get_db)):
    return db.query(FollowUp).order_by(
        FollowUp.follow_up_at.asc()
    ).all()

@router.get("/{follow_up_id}", response_model=FollowUpResponse)
def get_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db)
):
    follow_up = db.query(FollowUp).filter(
        FollowUp.id == follow_up_id
    ).first()

    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow-up not found")

    return follow_up


@router.post("/", response_model=FollowUpResponse, status_code=201)
def create_follow_up(
    data: FollowUpCreate,
    db: Session = Depends(get_db)
):
    if not db.query(Lead).filter(Lead.id == data.lead_id).first():
        raise HTTPException(status_code=404, detail="Lead not found")

    if data.tutor_id is not None:
        if not db.query(Tutor).filter(Tutor.id == data.tutor_id).first():
            raise HTTPException(status_code=404, detail="Tutor not found")

    follow_up = FollowUp(**data.model_dump())
    db.add(follow_up)
    try:
        db.commit()
        db.refresh(follow_up)
        return follow_up
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Follow-up save nahi ho saka."
        )



