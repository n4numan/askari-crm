from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Lead
from schemas import LeadCreate, LeadResponse


router = APIRouter(
    prefix="/api/leads",
    tags=["Leads"]
)


@router.get("/", response_model=List[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).order_by(Lead.id.desc()).all()


@router.post("/", response_model=LeadResponse, status_code=201)
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
