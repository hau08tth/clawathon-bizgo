from sqlalchemy import Column, String, DateTime, Text, Boolean, Enum as SAEnum
from datetime import datetime
import enum
from ..database import Base


class MessageType(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True)
    type = Column(SAEnum(MessageType), nullable=False)
    sender_id = Column(String, nullable=True)
    sender_name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_broadcast = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
