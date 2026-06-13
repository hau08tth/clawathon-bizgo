from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from ..database import Base


class Platform(str, enum.Enum):
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"


class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    SHARED = "shared"
    TRACKED = "tracked"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    description = Column(Text)
    target_platform = Column(JSON, default=list)
    reward_coins = Column(Integer, default=10)
    commission_rate = Column(Integer, default=5)
    image_url = Column(String)
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    posts = relationship("Post", back_populates="campaign", lazy="selectin")


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    platform = Column(SAEnum(Platform), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String)
    affiliate_code = Column(String, unique=True, index=True)
    post_url = Column(String)
    status = Column(SAEnum(PostStatus), default=PostStatus.DRAFT)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    shared_at = Column(DateTime)

    employee = relationship("Employee", back_populates="posts")
    campaign = relationship("Campaign", back_populates="posts")
