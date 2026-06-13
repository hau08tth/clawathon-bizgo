from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from ..database import Base


class Department(str, enum.Enum):
    TECH = "tech"
    HR = "hr"
    SALES = "sales"
    MARKETING = "marketing"
    OPERATIONS = "operations"
    FINANCE = "finance"
    PRODUCT = "product"


class SocialStyle(str, enum.Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    HUMOROUS = "humorous"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    department = Column(SAEnum(Department), default=Department.TECH)
    position = Column(String)
    avatar_url = Column(String)
    bio = Column(Text)
    social_style = Column(SAEnum(SocialStyle), default=SocialStyle.PROFESSIONAL)
    linkedin_url = Column(String)
    facebook_url = Column(String)
    hashed_password = Column(String, nullable=False)
    bizcoins = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())

    posts = relationship("Post", back_populates="employee", lazy="selectin")
    connections = relationship("Connection", back_populates="employee", lazy="selectin")
    ideas = relationship("Idea", back_populates="employee", lazy="selectin")
    transactions = relationship("Transaction", back_populates="employee", lazy="selectin")
    badges = relationship("EmployeeBadge", back_populates="employee", lazy="selectin")
