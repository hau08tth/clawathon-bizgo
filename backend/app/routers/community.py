from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from pydantic import BaseModel
from datetime import datetime
import uuid

from ..database import get_db
from ..models.community import ChatMessage, MessageType
from ..models.gamification import Transaction, TransactionType
from ..models.employee import Employee
from ..agents.chat_agent import ChatAgent
from ..services.teams_notifier import notify_broadcast
from .auth import get_current_employee

router = APIRouter(prefix="/community", tags=["community"])
_chat_agent = ChatAgent()


class ChatRequest(BaseModel):
    message: str


class BroadcastRequest(BaseModel):
    content: str


def _fmt(msg: ChatMessage) -> dict:
    return {
        "id": msg.id,
        "type": msg.type,
        "sender_id": msg.sender_id,
        "sender_name": msg.sender_name,
        "content": msg.content,
        "is_broadcast": msg.is_broadcast,
        "created_at": msg.created_at.isoformat(),
    }


@router.get("/feed")
async def get_feed(
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(
        select(ChatMessage)
        .where(
            (ChatMessage.is_broadcast == True)
            | (ChatMessage.sender_id == current_employee.id)
        )
        .order_by(ChatMessage.created_at)
        .limit(100)
    )
    messages = result.scalars().all()
    return [_fmt(m) for m in messages]


@router.post("/chat")
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Tin nhắn không được để trống")

    # Save user message
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        type=MessageType.USER,
        sender_id=current_employee.id,
        sender_name=current_employee.full_name,
        content=req.message.strip(),
        is_broadcast=False,
    )
    db.add(user_msg)

    # Build context
    leaderboard_result = await db.execute(
        select(Employee)
        .where(Employee.is_active == True)
        .order_by(desc(Employee.bizcoins))
        .limit(10)
    )
    leaderboard = [
        {"full_name": e.full_name, "bizcoins": e.bizcoins or 0}
        for e in leaderboard_result.scalars().all()
    ]

    rank_result = await db.execute(
        select(func.count(Employee.id)).where(
            Employee.bizcoins > (current_employee.bizcoins or 0)
        )
    )
    user_rank = (rank_result.scalar() or 0) + 1

    # Hot trends: recent earn transactions
    trends_result = await db.execute(
        select(Transaction, Employee)
        .join(Employee, Transaction.employee_id == Employee.id)
        .where(Transaction.type == TransactionType.EARN)
        .order_by(desc(Transaction.created_at))
        .limit(5)
    )
    hot_trends = [
        f"{emp.full_name} vừa kiếm được {tx.amount} BizCoins ({tx.reason})"
        for tx, emp in trends_result.all()
    ]

    # Get recent conversation history for context
    history_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.sender_id == current_employee.id)
        .order_by(desc(ChatMessage.created_at))
        .limit(10)
    )
    history_msgs = list(reversed(history_result.scalars().all()))
    history = [
        {
            "role": "user" if m.type == MessageType.USER else "assistant",
            "content": m.content,
        }
        for m in history_msgs
    ]

    context = {
        "user_name": current_employee.full_name,
        "user_coins": current_employee.bizcoins or 0,
        "user_rank": user_rank,
        "leaderboard": leaderboard,
        "hot_trends": hot_trends,
    }

    ai_reply = await _chat_agent.respond(req.message.strip(), context, history)

    # Save AI response (linked to this user via sender_id)
    ai_msg = ChatMessage(
        id=str(uuid.uuid4()),
        type=MessageType.ASSISTANT,
        sender_id=current_employee.id,
        sender_name="BizGro",
        content=ai_reply,
        is_broadcast=False,
    )
    db.add(ai_msg)
    await db.commit()

    return {
        "user_message": _fmt(user_msg),
        "ai_message": _fmt(ai_msg),
    }


@router.post("/broadcast")
async def broadcast(
    req: BroadcastRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    if not current_employee.is_admin:
        raise HTTPException(status_code=403, detail="Chỉ admin mới có thể broadcast")

    msg = ChatMessage(
        id=str(uuid.uuid4()),
        type=MessageType.SYSTEM,
        sender_id=current_employee.id,
        sender_name="BizGro",
        content=req.content,
        is_broadcast=True,
    )
    db.add(msg)
    await db.commit()

    background_tasks.add_task(notify_broadcast, req.content)

    return _fmt(msg)
