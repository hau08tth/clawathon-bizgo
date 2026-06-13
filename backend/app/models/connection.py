from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from ..database import Base


class OpportunityStatus(str, enum.Enum):
    MATCHED = "matched"
    INTRODUCED = "introduced"
    IN_PROGRESS = "in_progress"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class Connection(Base):
    __tablename__ = "connections"

    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    contact_name = Column(String, nullable=False)
    contact_company = Column(String, nullable=False)
    contact_position = Column(String)
    contact_email = Column(String)
    relationship_type = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    employee = relationship("Employee", back_populates="connections")
    opportunities = relationship("Opportunity", back_populates="connection", lazy="selectin")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(String, primary_key=True)
    connection_id = Column(String, ForeignKey("connections.id"), nullable=False)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    match_reason = Column(Text)
    pitching_script = Column(Text)
    ice_breaker = Column(Text)
    status = Column(SAEnum(OpportunityStatus), default=OpportunityStatus.MATCHED)
    reward_coins = Column(Integer, default=200)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow())

    connection = relationship("Connection", back_populates="opportunities")
