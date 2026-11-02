# askari-crm/backend/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal

# Lead SCHEMAS
class LeadCreate(BaseModel):
    parent_name: str | None = None
    parent_phone: str
    student_class: str | None = None
    subjects: str | None = None
    location: str
    monthly_budget: int | None = None
    notes: str | None = None


class LeadUpdate(BaseModel):
    parent_name: str | None = None
    parent_phone: str | None = None
    student_class: str | None = None
    subjects: str | None = None
    location: str | None = None
    monthly_budget: int | None = None
    notes: str | None = None
    status: str | None = None


class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_code: str
    parent_name: str | None = None
    parent_phone: str
    student_class: str | None = None
    subjects: str | None = None
    location: str
    monthly_budget: int | None = None
    status: str
    tutor_id: int | None = None
    notes: str | None = None
    next_follow_up: datetime | None = None
    created_at: datetime
    updated_at: datetime

# Tutor SCHEMAS
class TutorCreate(BaseModel):
    full_name: str
    phone: str
    email: str | None = None
    subjects: str | None = None
    areas: str | None = None
    monthly_fee: int | None = None
    cnic_image: str | None = None
    cv: str | None = None


class TutorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone: str
    email: str | None = None
    cnic_image: str | None = None
    cv: str | None = None
    subjects: str | None = None
    areas: str | None = None
    monthly_fee: int | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime



DemoStatus = Literal[
    "Scheduled",
    "Rescheduled",
    "Cancelled",
    "Demo Done"
]


# DEMO SCHEMAS
class DemoCreate(BaseModel):
    lead_id: int
    tutor_id: Optional[int] = None
    demo_date: date
    demo_time: Optional[time] = None
    status: DemoStatus = "Scheduled"
    parent_confirmed: bool = False
    tutor_confirmed: bool = False
    result: Optional[str] = None
    notes: Optional[str] = None


class DemoUpdate(BaseModel):
    tutor_id: Optional[int] = None
    demo_date: Optional[date] = None
    demo_time: Optional[time] = None
    status: Optional[DemoStatus] = None
    parent_confirmed: Optional[bool] = None
    tutor_confirmed: Optional[bool] = None
    result: Optional[str] = None
    notes: Optional[str] = None


class DemoResponse(DemoCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# FOLLOW-UP SCHEMAS
class FollowUpCreate(BaseModel):
    lead_id: int
    tutor_id: int | None = None
    follow_up_at: datetime
    method: str | None = None
    status: str = "Pending"
    outcome: str | None = None
    next_action: str | None = None
    next_action_at: datetime | None = None


class FollowUpResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    tutor_id: int | None = None
    follow_up_at: datetime
    method: str | None = None
    status: str
    outcome: str | None = None
    next_action: str | None = None
    next_action_at: datetime | None = None
    created_at: datetime


# TUITION SCHEMAS
class TuitionCreate(BaseModel):
    lead_id: int
    tutor_id: int | None = None
    monthly_fee: int
    academy_commission: int | None = None
    closing_date: date | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str = "Active"
    notes: str | None = None


class TuitionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    tutor_id: int | None = None
    monthly_fee: int
    academy_commission: int | None = None
    closing_date: date | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
