from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
)
from sqlalchemy.orm import relationship

from database import Base


# 1. LEADS
class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    lead_code = Column(String(30), unique=True, index=True, nullable=False)
    # Parent information
    parent_name = Column(String(100), nullable=True)
    parent_phone = Column(String(20), nullable=False)
    # Student requirements
    student_class = Column(String(100), nullable=True)
    subjects = Column(Text, nullable=True)
    location = Column(String(200), nullable=False)
    monthly_budget = Column(Integer, nullable=True)
    # Lead tracking
    status = Column(String(50),default="New Lead",nullable=False,index=True)
    # Currently assigned tutor
    tutor_id = Column(Integer,ForeignKey("tutors.id", ondelete="SET NULL"),nullable=True,index=True)
    notes = Column(Text, nullable=True)
    next_follow_up = Column(DateTime, nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
    # Relationships
    tutor = relationship("Tutor",back_populates="assigned_leads",foreign_keys=[tutor_id])
    demos = relationship("Demo",back_populates="lead",cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp",back_populates="lead",cascade="all, delete-orphan")
    tuition = relationship("Tuition",back_populates="lead",uselist=False,cascade="all, delete-orphan")


# 2. TUTORS
class Tutor(Base):
    __tablename__ = "tutors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, index=True)
    email = Column(String(150), nullable=True)
    cnic_image = Column(String(255), nullable=True)
    cv = Column(String(255), nullable=True)
    subjects = Column(Text, nullable=True)
    areas = Column(Text, nullable=True)
    monthly_fee = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
    # Leads assigned to this tutor
    assigned_leads = relationship("Lead",back_populates="tutor",foreign_keys="Lead.tutor_id")
    demos = relationship("Demo",back_populates="tutor")
    tuitions = relationship("Tuition",back_populates="tutor")
    follow_ups = relationship("FollowUp",back_populates="tutor")


# 3. DEMOS
class Demo(Base):
    __tablename__ = "demos"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer,ForeignKey("leads.id", ondelete="CASCADE"),nullable=False,index=True )
    tutor_id = Column(Integer,ForeignKey("tutors.id", ondelete="SET NULL"),nullable=True,index=True)
    demo_date = Column(Date, nullable=False)
    demo_time = Column(Time, nullable=True)
    # Scheduled, Rescheduled, Cancelled, Demo Done
    status = Column(String(50),default="Scheduled",nullable=False)
    parent_confirmed = Column(Boolean, default=False, nullable=False)
    tutor_confirmed = Column(Boolean, default=False, nullable=False)
    # Demo outcome
    result = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    lead = relationship("Lead", back_populates="demos")
    tutor = relationship("Tutor", back_populates="demos")


# 4. FOLLOW-UPS
class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer,ForeignKey("leads.id", ondelete="CASCADE"),nullable=False,index=True)
    tutor_id = Column(Integer,ForeignKey("tutors.id", ondelete="SET NULL"),nullable=True,index=True)
    follow_up_at = Column(DateTime, nullable=False)
    # Call, WhatsApp, Message, Other
    method = Column(String(30), nullable=True)
    # Pending, Completed, Missed, Rescheduled
    status = Column(String(30),default="Pending",nullable=False)
    outcome = Column(Text, nullable=True)
    next_action = Column(Text, nullable=True)
    next_action_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    lead = relationship("Lead", back_populates="follow_ups")
    tutor = relationship("Tutor", back_populates="follow_ups")


# 5. TUITIONS
class Tuition(Base):
    __tablename__ = "tuitions"

    id = Column(Integer, primary_key=True, index=True)
    # One tuition record per lead
    lead_id = Column(Integer,ForeignKey("leads.id", ondelete="CASCADE"),unique=True,nullable=False,index=True)
    tutor_id = Column(Integer,ForeignKey("tutors.id", ondelete="SET NULL"), nullable=True,index=True)
    monthly_fee = Column(Integer, nullable=False)
    academy_commission = Column(Integer, nullable=True)
    closing_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    # Active, Completed, Cancelled, On Hold
    status = Column(String(30),default="Active",nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False )
    lead = relationship("Lead", back_populates="tuition")
    tutor = relationship("Tutor", back_populates="tuitions")
