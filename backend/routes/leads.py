from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Lead
from schemas import LeadCreate, LeadUpdate, LeadResponse


router = APIRouter(
    prefix="/api/leads",
    tags=["Leads"]
)


LEAD_STATUSES = [
    "New Lead",
    "Parent Not Responding",
    "Cancelled / Not Interested",
]


@router.get("/", response_model=List[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).order_by(Lead.id.desc()).all()


@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):

    lead = Lead(
        lead_code="HT-" + datetime.now().strftime("%Y%m%d%H%M%S%f"),
        parent_name=lead_data.parent_name,
        parent_phone=lead_data.parent_phone,
        student_class=lead_data.student_class,
        subjects=lead_data.subjects,
        location=lead_data.location,
        monthly_budget=lead_data.monthly_budget,
        notes=lead_data.notes,
        status="New Lead",
    )

    try:
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return lead

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Lead save nahi ho saki. Database error check karein."
        )


@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    db: Session = Depends(get_db)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead nahi mili.")

    update_data = lead_data.model_dump(exclude_unset=True)

    if "status" in update_data and update_data["status"] not in LEAD_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid lead status."
        )

    for field, value in update_data.items():
        setattr(lead, field, value)

    try:
        db.commit()
        db.refresh(lead)
        return lead

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Lead update nahi ho saki."
        )


@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead nahi mili.")

    try:
        db.delete(lead)
        db.commit()
        return {"message": "Lead successfully delete ho gayi."}

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Lead delete nahi ho saki. Related records check karein."
        )