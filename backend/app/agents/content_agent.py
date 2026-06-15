"""BIZ-SHARE: AI Content Personalized Generator Agent"""
from openai import AsyncOpenAI
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from ..config import settings


class ContentState(TypedDict):
    messages: Annotated[list, add_messages]
    product_name: str
    product_description: str
    platform: str
    social_style: str
    employee_name: str
    department: str
    generated_posts: list[dict]
    selected_post: str
    step: str


PLATFORM_PROMPTS = {
    "facebook": "Facebook - mạng xã hội cá nhân, thân thiện, gần gũi",
    "linkedin": "LinkedIn - mạng chuyên nghiệp, tập trung vào giá trị kinh doanh",
    "tiktok": "TikTok - vui nhộn, ngắn gọn, trendy, có hook mạnh",
}

STYLE_PROMPTS = {
    "professional": "chuyên nghiệp, đáng tin cậy, dùng số liệu và lợi ích cụ thể",
    "casual": "thân thiện, gần gũi như chia sẻ với bạn bè",
    "humorous": "hài hước, dí dỏm, tạo sự bất ngờ thú vị",
}


class ContentAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.llm_api_key, base_url=settings.openai_base_url)
        self.model = settings.openai_model
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(ContentState)
        workflow.add_node("generate_posts", self._generate_posts)
        workflow.add_node("optimize_post", self._optimize_post)
        workflow.set_entry_point("generate_posts")
        workflow.add_edge("generate_posts", "optimize_post")
        workflow.add_edge("optimize_post", END)
        return workflow.compile()

    async def _generate_posts(self, state: ContentState) -> dict:
        platform_desc = PLATFORM_PROMPTS.get(state["platform"], state["platform"])
        style_desc = STYLE_PROMPTS.get(state["social_style"], state["social_style"])

        prompt = f"""Bạn là AI Content Creator chuyên nghiệp cho Zalopay.

Thông tin nhân viên:
- Tên: {state["employee_name"]}
- Phòng ban: {state["department"]}
- Phong cách viết: {style_desc}

Sản phẩm cần quảng bá:
- Tên: {state["product_name"]}
- Mô tả: {state["product_description"]}

Nền tảng đăng: {platform_desc}

Hãy tạo ra 3 phiên bản bài đăng khác nhau (hài hước, chuyên nghiệp, tâm sự cá nhân) phù hợp với nền tảng {state["platform"]} và phong cách {state["social_style"]} của nhân viên.

Mỗi bài phải:
1. Tự nhiên như chính người dùng viết, không phải quảng cáo cứng
2. Có hook mạnh ở đầu
3. Kết thúc bằng CTA (call-to-action) nhẹ nhàng
4. Phù hợp với Zalopay Fintech context
5. Độ dài: Facebook 150-200 chữ, LinkedIn 200-300 chữ, TikTok 80-120 chữ

**Lưu ý**: Tên thương hiệu "Zalopay" chỉ viết hoa chữ "Z" chữ "p" phải viết thường.

Trả về JSON với format:
{{
  "posts": [
    {{"style": "hài hước", "content": "...", "hashtags": ["#tag1", "#tag2"]}},
    {{"style": "chuyên nghiệp", "content": "...", "hashtags": ["#tag1", "#tag2"]}},
    {{"style": "tâm sự", "content": "...", "hashtags": ["#tag1", "#tag2"]}}
  ]
}}"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            response_format={"type": "json_object"},
        )

        import json
        text = response.choices[0].message.content or "{}"
        try:
            data = json.loads(text)
            posts = data.get("posts", [])
        except json.JSONDecodeError:
            posts = [{"style": "chuyên nghiệp", "content": text, "hashtags": []}]

        return {"generated_posts": posts, "step": "posts_generated"}

    async def _optimize_post(self, state: ContentState) -> dict:
        if not state.get("generated_posts"):
            return {"step": "completed"}

        best_post = state["generated_posts"][0]
        style = state.get("social_style", "professional")
        for post in state["generated_posts"]:
            if style in post.get("style", "").lower():
                best_post = post
                break

        return {
            "selected_post": best_post.get("content", ""),
            "step": "completed",
        }

    async def generate(
        self,
        product_name: str,
        product_description: str,
        platform: str,
        social_style: str,
        employee_name: str,
        department: str,
    ) -> dict:
        initial_state: ContentState = {
            "messages": [],
            "product_name": product_name,
            "product_description": product_description,
            "platform": platform,
            "social_style": social_style,
            "employee_name": employee_name,
            "department": department,
            "generated_posts": [],
            "selected_post": "",
            "step": "start",
        }
        result = await self.graph.ainvoke(initial_state)
        return {
            "posts": result.get("generated_posts", []),
            "recommended": result.get("selected_post", ""),
        }
