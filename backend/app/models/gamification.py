from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Enum as SAEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from ..database import Base


class TransactionType(str, enum.Enum):
    EARN = "earn"
    SPEND = "spend"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    type = Column(SAEnum(TransactionType), nullable=False)
    amount = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    reference_id = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    employee = relationship("Employee", back_populates="transactions")


class Badge(Base):
    __tablename__ = "badges"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    icon = Column(String)
    color = Column(String, default="#6366f1")
    criteria = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    employee_badges = relationship("EmployeeBadge", back_populates="badge")


class EmployeeBadge(Base):
    __tablename__ = "employee_badges"

    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    badge_id = Column(String, ForeignKey("badges.id"), nullable=False)
    awarded_at = Column(DateTime, default=lambda: datetime.utcnow())

    employee = relationship("Employee", back_populates="badges")
    badge = relationship("Badge", back_populates="employee_badges")


class StoreItem(Base):
    __tablename__ = "store_items"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    image_url = Column(String)
    cost = Column(Integer, nullable=False)
    stock = Column(Integer, default=-1)
    is_active = Column(Boolean, default=True)
    category = Column(String, default="general")
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    redemptions = relationship("Redemption", back_populates="item")


class Redemption(Base):
    __tablename__ = "redemptions"

    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    item_id = Column(String, ForeignKey("store_items.id"), nullable=False)
    coins_spent = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    item = relationship("StoreItem", back_populates="redemptions")
