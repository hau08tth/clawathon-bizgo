import httpx
import logging
from ..config import settings

logger = logging.getLogger(__name__)


async def _post(payload: dict) -> bool:
    url = settings.teams_incoming_webhook_url
    if not url:
        logger.warning("Teams notification skipped: TEAMS_INCOMING_WEBHOOK_URL not set")
        return False
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            logger.warning("Teams sent: status=%s body=%s", resp.status_code, resp.text[:100])
            resp.raise_for_status()
            return True
    except Exception as exc:
        logger.error("Teams notification failed: %s", exc)
        return False


async def send_to_teams(text: str, title: str = "BizGro") -> bool:
    """Generic notification — dùng sections để markdown render đúng."""
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0B47D9",
        "summary": title,
        "sections": [
            {
                "activityTitle": title,
                "activityText": text,
                "markdown": True,
            }
        ],
    }
    return await _post(payload)


async def send_chat_answer(question: str, user_name: str, answer: str) -> bool:
    """Chatbot reply — tách question và answer thành 2 section rõ ràng."""
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0B47D9",
        "summary": f"BizGro trả lời {user_name}",
        "sections": [
            {
                "activityTitle": f"❓ {user_name} hỏi:",
                "activityText": question,
                "markdown": True,
            },
            {
                "activityTitle": "🤖 BizGro AI:",
                "activityText": answer,
                "markdown": True,
            },
        ],
    }
    return await _post(payload)


async def notify_broadcast(content: str) -> bool:
    return await send_to_teams(content, title="📢 Thông báo BizGro")


async def notify_coin_award(employee_name: str, coins: int, reason: str) -> bool:
    text = f"🎉 **{employee_name}** vừa nhận được **{coins} BizCoins**!\n\n_{reason}_"
    return await send_to_teams(text, title="🏆 BizGro — Điểm thưởng mới")
