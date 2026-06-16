"""BIZ-CONNECT: AI Referral Matchmaker Agent"""
from openai import AsyncOpenAI
import json
import re
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from ..config import settings


class NetworkState(TypedDict):
    messages: Annotated[list, add_messages]
    employee_name: str
    employee_position: str
    department: str
    contacts: list[dict]
    target_profiles: list[dict]
    matches: list[dict]
    pitching_scripts: list[dict]
    step: str


class NetworkAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.llm_api_key, base_url=settings.openai_base_url)
        self.model = settings.openai_model
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(NetworkState)
        workflow.add_node("analyze_contacts", self._analyze_contacts)
        workflow.add_node("generate_scripts", self._generate_scripts)
        workflow.set_entry_point("analyze_contacts")
        workflow.add_edge("analyze_contacts", "generate_scripts")
        workflow.add_edge("generate_scripts", END)
        return workflow.compile()

    async def _analyze_contacts(self, state: NetworkState) -> dict:
        contacts_text = json.dumps(state["contacts"], ensure_ascii=False, indent=2)
        targets_text = json.dumps(state["target_profiles"], ensure_ascii=False, indent=2)

        prompt = f"""Bạn là AI Network Matcher chuyên phân tích mạng lưới quan hệ.

Nhân viên: {state["employee_name"]} - {state["employee_position"]} ({state["department"]})

Danh sách liên hệ của nhân viên:
{contacts_text}

Chân dung khách hàng mục tiêu (ICP) của Zalopay:
{targets_text}

Hãy phân tích và tìm ra các "Cặp trùng khớp hoàn hảo" (matches) giữa danh sách liên hệ và khách hàng mục tiêu.

Với mỗi match, hãy giải thích:
1. Tại sao đây là cơ hội tốt
2. Pain points của công ty họ mà Zalopay có thể giải quyết
3. Mức độ phù hợp (score 1-10)

**Lưu ý**: Tên thương hiệu "Zalopay" chỉ viết hoa chữ "Z" chữ "p" phải viết thường.

Trả về JSON:
{{
  "matches": [
    {{
      "contact_name": "...",
      "contact_company": "...",
      "contact_position": "...",
      "match_score": 8,
      "match_reason": "...",
      "pain_points": "...",
      "zalopay_solution": "..."
    }}
  ]
}}"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            response_format={"type": "json_object"},
        )

        text = response.choices[0].message.content or "{}"
        try:
            data = json.loads(text)
            matches = data.get("matches", [])
        except json.JSONDecodeError:
            matches = []

        return {"matches": matches, "step": "contacts_analyzed"}

    async def _generate_scripts(self, state: NetworkState) -> dict:
        scripts = []
        for m in state.get("matches", [])[:3]:
            prompt = f"""Tạo kịch bản mở lời (ice-breaker) và pitching script để {state["employee_name"]} kết nối với {m.get("contact_name")} - {m.get("contact_position")} tại {m.get("contact_company")}.

Lý do match: {m.get("match_reason")}
Pain points: {m.get("pain_points")}
Giải pháp Zalopay: {m.get("zalopay_solution")}

Tạo:
1. Ice-breaker message (tin nhắn đầu tiên, thân thiện, không bán hàng ngay) - 50-80 chữ
2. Pitching script (sau khi họ đồng ý nói chuyện) - 150-200 chữ

Trả về JSON:
{{
  "ice_breaker": "...",
  "pitching_script": "..."
}}"""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                response_format={"type": "json_object"},
            )

            text = response.choices[0].message.content or "{}"
            try:
                script_data = json.loads(text)
            except json.JSONDecodeError:
                script_data = {"ice_breaker": text, "pitching_script": ""}

            scripts.append({**m, **script_data})

        return {"pitching_scripts": scripts, "step": "completed"}

    async def match_and_generate(
        self,
        employee_name: str,
        employee_position: str,
        department: str,
        contacts: list[dict],
        target_profiles: list[dict] | None = None,
    ) -> dict:
        if not target_profiles:
            target_profiles = [
                {"type": "Doanh nghiệp SME", "size": "50-500 nhân viên", "need": "Quản lý thanh toán, chi lương"},
                {"type": "Startup Tech", "size": "10-100 nhân viên", "need": "Tích hợp payment gateway"},
                {"type": "Chuỗi bán lẻ", "size": "100+ cửa hàng", "need": "POS và thanh toán QR"},
            ]

        initial_state: NetworkState = {
            "messages": [],
            "employee_name": employee_name,
            "employee_position": employee_position,
            "department": department,
            "contacts": contacts,
            "target_profiles": target_profiles,
            "matches": [],
            "pitching_scripts": [],
            "step": "start",
        }
        result = await self.graph.ainvoke(initial_state)
        return {
            "matches": result.get("matches", []),
            "scripts": result.get("pitching_scripts", []),
        }
