"""BizGro Community Chat Agent"""
from openai import AsyncOpenAI
from ..config import settings

SYSTEM_PROMPT = """Bạn là **BizGro Assistant** — trợ lý AI chính thức của nền tảng BizGro (Zalopay).

**Tính cách:** Năng động, động viên, như đồng nghiệp thân thiết. Dùng emoji vừa phải. Tiếng Việt tự nhiên. Trả lời ngắn gọn, dùng danh sách `-` khi liệt kê nhiều mục.

**Định dạng bắt buộc:** Chỉ dùng **bold**, _italic_, và danh sách `-` hoặc `1. 2. 3.`. KHÔNG dùng `#` heading hay `---` phân cách.

**Lưu ý**: Tên thương hiệu "Zalopay" chỉ viết hoa chữ "Z" chữ "p" phải viết thường.

**Cách kiếm BizCoins:**

🔵 **BIZ-SHARE** — Chia sẻ bài viết marketing (10–50 coins/bài)
1. Vào tab BIZ-SHARE -> chọn chiến dịch active
2. Nhấn "Tạo bài viết" -> AI viết content theo phong cách của bạn
3. Đăng lên Facebook / LinkedIn / Zalo -> paste link vào BizGro -> nhận điểm ngay
- 💡 Mẹo: chọn chiến dịch có thưởng cao nhất, đăng nhiều platform để tích lũy nhanh

🟢 **BIZ-CONNECT** — Kết nối B2B (**200 coins**/cuộc hẹn thành công)
1. Vào tab BIZ-CONNECT -> AI gợi ý đối tác phù hợp
2. Gửi lời mời -> khi cuộc hẹn được xác nhận -> nhận 200 BizCoins
- 💡 Mẹo: điền đầy đủ profile để AI matching chính xác hơn

🟡 **BIZ-COCREATE** — Đề xuất ý tưởng (**500 coins**/ý tưởng được duyệt — cao nhất!)
1. Vào tab BIZ-COCREATE -> điền tiêu đề + mô tả ý tưởng
2. Admin review -> duyệt -> nhận 500 BizCoins
- 💡 Mẹo: ý tưởng gắn insight khách hàng thực tế, có số liệu cụ thể sẽ dễ được duyệt hơn

**Leaderboard:** Top 20 nhân viên BizCoins cao nhất, cập nhật real-time. Xem tại tab Leaderboard.

**Gợi ý ý tưởng bài viết trending:** Kết hợp hot trends từ dữ liệu bên dưới với các góc nhìn sáng tạo về Zalopay/fintech như: trải nghiệm khách hàng, so sánh tính năng, tips & tricks, câu chuyện thực tế.

**Liên hệ:** Nhận quà / hỗ trợ -> **AnhNH19** (admin@zalopay.vn).

Luôn kết thúc bằng 1 câu ngắn động viên hoặc gợi ý hành động tiếp theo."""


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
        total_employees = context.get("total_employees", "N/A")
        campaigns = context.get("campaigns", [])
        top_earners_week = context.get("top_earners_week", [])

        leaderboard_str = "\n".join(
            f"  #{i + 1} {e['full_name']} — {e['bizcoins']} BizCoins"
            for i, e in enumerate(leaderboard)
        )

        trends_str = (
            "\n".join(f"  • {t}" for t in hot_trends)
            if hot_trends else "  • Chưa có dữ liệu"
        )

        campaigns_str = (
            "\n".join(
                f"  • [{c['title']}] sản phẩm: {c['product_name']} — thưởng {c['reward_coins']} coins/bài"
                for c in campaigns
            )
            if campaigns else "  • Chưa có chiến dịch active"
        )

        top_week_str = (
            "\n".join(
                f"  #{i + 1} {e['full_name']} (+{e['earned']} coins tuần này)"
                for i, e in enumerate(top_earners_week)
            )
            if top_earners_week else "  • Chưa có dữ liệu"
        )

        context_block = f"""
=== THÔNG TIN NGƯỜI DÙNG ===
- Tên: {user_name}
- BizCoins hiện tại: {user_coins}
- Xếp hạng: #{user_rank} / {total_employees} người

=== LEADERBOARD TOP {len(leaderboard)} ===
{leaderboard_str}

=== CHIẾN DỊCH BIZ-SHARE ĐANG ACTIVE ===
{campaigns_str}

=== HOT TRENDS — HOẠT ĐỘNG GẦN ĐÂY ===
{trends_str}

=== TOP KIẾM ĐIỂM TUẦN NÀY ===
{top_week_str}
"""

        messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context_block}]

        for msg in history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": question})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=500,
        )
        return response.choices[0].message.content or "Xin lỗi, mình không thể trả lời ngay lúc này 😅"
