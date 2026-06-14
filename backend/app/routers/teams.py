"""Microsoft Teams Outgoing Webhook handler."""
from fastapi import APIRouter, BackgroundTasks, Request, HTTPException
from sqlalchemy import select, desc, func
import hmac as hmac_lib
import hashlib
import base64
import re

from datetime import datetime, timedelta

from ..database import AsyncSessionLocal
from ..models.employee import Employee
from ..models.gamification import Transaction, TransactionType
from ..models.campaign import Campaign
from ..agents.chat_agent import ChatAgent
from ..services.teams_notifier import send_to_teams, send_chat_answer
from ..config import settings

router = APIRouter(prefix="/teams", tags=["teams"])
_chat_agent = ChatAgent()


def _verify_hmac(body: bytes, authorization: str | None, secret: str) -> bool:
    if not authorization or not authorization.startswith("HMAC "):
        return False
    received = authorization[5:].strip()
    key = base64.b64decode(secret)
    expected = base64.b64encode(
        hmac_lib.new(key, body, hashlib.sha256).digest()
    ).decode()
    return hmac_lib.compare_digest(received, expected)


def _strip_mentions(text: str) -> str:
    return re.sub(r"<at>[^<]*</at>", "", text).strip()


async def _build_context() -> dict:
    async with AsyncSessionLocal() as db:
        # Full top-10 leaderboard
        lb_result = await db.execute(
            select(Employee)
            .where(Employee.is_active == True, Employee.is_admin == False)
            .order_by(desc(Employee.bizcoins))
            .limit(10)
        )
        leaderboard = [
            {"full_name": e.full_name, "bizcoins": e.bizcoins or 0}
            for e in lb_result.scalars().all()
        ]

        # Total employee count
        count_result = await db.execute(
            select(func.count(Employee.id))
            .where(Employee.is_active == True, Employee.is_admin == False)
        )
        total_employees = count_result.scalar() or 0

        # Recent hot trends (last 10 earn transactions)
        tx_result = await db.execute(
            select(Transaction, Employee)
            .join(Employee, Transaction.employee_id == Employee.id)
            .where(Transaction.type == TransactionType.EARN)
            .order_by(desc(Transaction.created_at))
            .limit(10)
        )
        hot_trends = [
            f"{emp.full_name} kiếm {tx.amount} coins — {tx.reason}"
            for tx, emp in tx_result.all()
        ]

        # Active campaigns for BIZ-SHARE
        camp_result = await db.execute(
            select(Campaign).where(Campaign.is_active == True).limit(5)
        )
        campaigns = [
            {
                "title": c.title,
                "product_name": c.product_name,
                "reward_coins": c.reward_coins,
            }
            for c in camp_result.scalars().all()
        ]

        # Top earners this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_result = await db.execute(
            select(Employee.full_name, func.sum(Transaction.amount).label("earned"))
            .join(Transaction, Transaction.employee_id == Employee.id)
            .where(
                Transaction.type == TransactionType.EARN,
                Transaction.created_at >= week_ago,
                Employee.is_admin == False,
            )
            .group_by(Employee.id, Employee.full_name)
            .order_by(desc("earned"))
            .limit(5)
        )
        top_earners_week = [
            {"full_name": row.full_name, "earned": row.earned}
            for row in week_result.all()
        ]

    return {
        "user_name": "Teams User",
        "user_coins": "Đăng nhập BizGro để xem điểm cá nhân",
        "user_rank": "N/A",
        "leaderboard": leaderboard,
        "total_employees": total_employees,
        "hot_trends": hot_trends,
        "campaigns": campaigns,
        "top_earners_week": top_earners_week,
    }


async def _answer_and_notify(question: str, user_name: str) -> None:
    """Call LLM in background, then push answer to Teams via Incoming Webhook."""
    context = await _build_context()
    context["user_name"] = user_name
    answer = await _chat_agent.respond(question, context, [])
    await send_chat_answer(question, user_name, answer)


@router.post("/webhook")
async def teams_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()

    # Verify HMAC signature if secret is configured
    if settings.teams_webhook_secret:
        auth = request.headers.get("Authorization", "")
        if not _verify_hmac(body, auth, settings.teams_webhook_secret):
            raise HTTPException(status_code=401, detail="Invalid Teams signature")

    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Only handle message events
    if data.get("type") != "message":
        return {"type": "message", "text": ""}

    user_name = data.get("from", {}).get("name", "bạn")
    raw_text = data.get("text", "")
    question = _strip_mentions(raw_text)

    if not question:
        return {
            "type": "message",
            "text": (
                f"Chào {user_name}! 👋 Mình là **BizGro AI**.\n\n"
                "Hỏi mình về:\n"
                "• 🏆 Bảng xếp hạng BizCoins\n"
                "• 🔥 Hot trends đang nổi\n"
                "• 🎁 Cách đổi quà & nhận thưởng\n"
                "• 💡 Tính năng BIZ-SHARE, BIZ-CONNECT, BIZ-COCREATE"
            ),
        }

    # Respond immediately (Teams 5s timeout), process LLM in background
    background_tasks.add_task(_answer_and_notify, question, user_name)

    return {
        "type": "message",
        "text": f"⏳ Đang xử lý câu hỏi của **{user_name}**...",
    }
