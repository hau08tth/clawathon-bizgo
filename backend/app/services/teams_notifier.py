import httpx
import logging
from ..config import settings

logger = logging.getLogger(__name__)


async def send_to_teams(text: str, title: str = "BizGro") -> bool:
    """Send a notification to the Teams channel via Incoming Webhook."""
    url = settings.teams_incoming_webhook_url
    if not url:
        logger.warning("Teams notification skipped: TEAMS_INCOMING_WEBHOOK_URL not set")
        return False

    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0B47D9",
        "summary": title,
        "title": title,
        "text": text,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            logger.warning("Teams notification sent: status=%s body=%s", resp.status_code, resp.text[:200])
            resp.raise_for_status()
            return True
    except Exception as exc:
        logger.error("Teams notification failed: %s", exc)
        return False


async def notify_broadcast(content: str) -> bool:
    return await send_to_teams(content, title="📢 Thông báo BizGro")


async def notify_coin_award(employee_name: str, coins: int, reason: str) -> bool:
    text = f"🎉 **{employee_name}** vừa nhận được **{coins} BizCoins**!\n\n_{reason}_"
    return await send_to_teams(text, title="🏆 BizGro — Điểm thưởng mới")


async def notify_leaderboard_update(top3: list[dict]) -> bool:
    lines = "\n\n".join(
        f"{i + 1}. **{e['full_name']}** — {e['bizcoins']} BizCoins"
        for i, e in enumerate(top3)
    )
    text = f"Bảng xếp hạng Top 3 hiện tại:\n\n{lines}"
    return await send_to_teams(text, title="🥇 BizGro — Cập nhật BXH")
