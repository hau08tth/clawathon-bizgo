"""BizGro Community Chat Agent"""
from openai import AsyncOpenAI
from ..config import settings

SYSTEM_PROMPT = """Bạn là BizGro Assistant - trợ lý AI thông minh, thân thiện của nền tảng BizGro (Zalopay).

Tính cách: Vui vẻ, động viên, chuyên nghiệp nhưng gần gũi như đồng nghiệp thân thiết. Dùng emoji phù hợp.
Ngôn ngữ: Tiếng Việt tự nhiên, không dùng ngôn ngữ quá trang trọng.
Độ dài: Ngắn gọn, súc tích (1-4 câu). Không nói dài dòng.

Bạn có thể trả lời về:
- Điểm BizCoin của người dùng và bảng xếp hạng
- Hot trends: những hoạt động đang nổi trên BizGro
- Quà tặng và cách nhận quà sau khi đổi ở BizStore
- Hướng dẫn các tính năng BIZ-SHARE, BIZ-CONNECT, BIZ-COCREATE
- Thông tin liên hệ admin khi cần hỗ trợ

Khi được hỏi về nhận quà/phần thưởng: luôn hướng về liên hệ admin AnhNH19 (admin@zalopay.vn).
Kết thúc tin nhắn bằng 1 câu khuyến khích ngắn liên quan đến Zalopay."""


class ChatAgent:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.openai_base_url,
        )
        self.model = settings.openai_model

    async def respond(self, question: str, context: dict, history: list[dict]) -> str:
        user_name = context.get("user_name", "bạn")
        user_coins = context.get("user_coins", 0)
        user_rank = context.get("user_rank", "N/A")
        leaderboard = context.get("leaderboard", [])
        hot_trends = context.get("hot_trends", [])

        top5 = "\n".join(
            f"  #{i + 1} {e['full_name']} - {e['bizcoins']} BizCoins"
            for i, e in enumerate(leaderboard[:5])
        )

        trends_str = "\n".join(f"  • {t}" for t in hot_trends) if hot_trends else "  • Chưa có dữ liệu"

        context_block = f"""
=== THÔNG TIN NGƯỜI DÙNG HIỆN TẠI ===
- Tên: {user_name}
- BizCoins: {user_coins} coins
- Xếp hạng: #{user_rank}

=== TOP 5 LEADERBOARD ===
{top5}

=== HOT TRENDS GẦN ĐÂY ===
{trends_str}

=== LIÊN HỆ ADMIN ===
- AnhNH19 (admin@zalopay.vn) - phụ trách trao phần thưởng và hỗ trợ
"""

        messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n" + context_block}]

        for msg in history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": question})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=300,
        )
        return response.choices[0].message.content or "Xin lỗi, tôi không thể trả lời ngay lúc này 😅"
