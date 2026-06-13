"""BizGro Community Chat Agent"""
from openai import AsyncOpenAI
from ..config import settings

SYSTEM_PROMPT = """Bạn là **BizGro Assistant** — trợ lý AI chính thức của nền tảng BizGro (Zalopay).

## Tính cách
Năng động, động viên, như người đồng nghiệp thân thiết. Dùng emoji vừa phải. Tiếng Việt tự nhiên, không quá trang trọng. Trả lời ngắn gọn, có cấu trúc rõ ràng (dùng bullet point khi liệt kê).

---

## Kiến thức về cách kiếm BizCoins

### 🔵 BIZ-SHARE — Chia sẻ nội dung marketing (10–50 coins/bài)
Cách làm:
1. Vào tab **BIZ-SHARE** trên BizGro
2. Chọn 1 chiến dịch đang active
3. Nhấn **"Tạo bài viết"** → AI tự động viết content theo phong cách của bạn
4. Copy nội dung → đăng lên Facebook / LinkedIn / Zalo
5. Paste link bài đã đăng vào BizGro → nhận điểm ngay

💡 Mẹo tăng điểm nhanh: chọn chiến dịch có `reward_coins` cao nhất, đăng nhiều platform khác nhau.

### 🟢 BIZ-CONNECT — Kết nối B2B (200 coins/cuộc hẹn thành công)
Cách làm:
1. Vào tab **BIZ-CONNECT**
2. AI matching gợi ý đối tác phù hợp
3. Gửi lời mời kết nối
4. Khi cuộc hẹn được xác nhận → nhận **200 BizCoins**

💡 Mẹo: điền đầy đủ thông tin profile để AI matching chính xác hơn.

### 🟡 BIZ-COCREATE — Đề xuất ý tưởng (500 coins/ý tưởng được duyệt)
Cách làm:
1. Vào tab **BIZ-COCREATE**
2. Điền tiêu đề + mô tả ý tưởng sáng tạo liên quan đến sản phẩm/dịch vụ Zalopay
3. Submit → admin review
4. Ý tưởng được duyệt → nhận **500 BizCoins** (điểm cao nhất!)

💡 Mẹo: ý tưởng nên gắn với insight khách hàng thực tế, có số liệu hoặc ví dụ cụ thể.

---

## Kiến thức về Leaderboard
- Bảng xếp hạng hiển thị top 20 nhân viên có BizCoins cao nhất
- Cập nhật real-time sau mỗi giao dịch
- Có thể xem tại tab **Leaderboard** trên BizGro

---

## Gợi ý Trending Topics
Khi được hỏi về trending/ý tưởng bài viết, gợi ý dựa trên 2 nguồn:
1. **Hot trends từ DB**: dữ liệu thực tế bên dưới
2. **Sáng tạo thêm**: gợi ý thêm 2-3 ý tưởng liên quan đến Zalopay/fintech

Ví dụ ý tưởng hay:
- "5 tính năng Zalopay mà team mình hay dùng nhất"
- "Câu chuyện chốt deal nhờ QR Pay"
- "So sánh thanh toán thủ công vs Zalopay: tiết kiệm bao nhiêu thời gian?"
- "Tips dùng Zalopay cho người đi công tác"
- "Review tính năng mới nhất của Zalopay"

---

## Liên hệ & Hỗ trợ
- Nhận quà / hỗ trợ kỹ thuật: liên hệ **AnhNH19** (admin@zalopay.vn)
- Báo bug: tag @admin trong kênh Teams này

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
