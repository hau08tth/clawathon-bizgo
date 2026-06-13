from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Enum as SAEnum, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from ..database import Base


class IdeaStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    ENHANCING = "enhancing"
    ENHANCED = "enhanced"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    IMPLEMENTING = "implementing"
    COMPLETED = "completed"
    REJECTED = "rejected"


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    title = Column(String, nullable=False)
    raw_idea = Column(Text, nullable=False)
    enhanced_proposal = Column(Text)
    market_analysis = Column(Text)
    revenue_projection = Column(Text)
    feasibility_score = Column(Float)
    cost_score = Column(Float)
    revenue_potential_score = Column(Float)
    total_score = Column(Float)
    status = Column(SAEnum(IdeaStatus), default=IdeaStatus.SUBMITTED)
    reward_coins = Column(Integer, default=500)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow())

    employee = relationship("Employee", back_populates="ideas")
