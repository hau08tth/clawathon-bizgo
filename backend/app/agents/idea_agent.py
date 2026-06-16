"""BIZ-COCREATE: AI Idea Incubator Agent"""
from openai import AsyncOpenAI
import json
import re
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from ..config import settings


class IdeaState(TypedDict):
    messages: Annotated[list, add_messages]
    raw_idea: str
    employee_name: str
    department: str
    enhanced_proposal: str
    market_analysis: str
    revenue_projection: str
    evaluation: dict
    step: str


class IdeaAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.llm_api_key, base_url=settings.openai_base_url)
        self.model = settings.openai_model
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(IdeaState)
        workflow.add_node("enhance_idea", self._enhance_idea)
        workflow.add_node("market_analysis", self._market_analysis)
        workflow.add_node("evaluate_idea", self._evaluate_idea)
        workflow.set_entry_point("enhance_idea")
        workflow.add_edge("enhance_idea", "market_analysis")
        workflow.add_edge("market_analysis", "evaluate_idea")
        workflow.add_edge("evaluate_idea", END)
        return workflow.compile()

    async def _enhance_idea(self, state: IdeaState) -> dict:
        prompt = f"""Bạn là AI Business Analyst chuyên nghiệp cho Zalopay Fintech.

Nhân viên: {state["employee_name"]} ({state["department"]})
Ý tưởng thô: {state["raw_idea"]}

Hãy "nhào nặn" ý tưởng này thành một Business Proposal hoàn chỉnh bao gồm:
1. Tóm tắt điều hành (Executive Summary) - 2-3 câu súc tích
2. Vấn đề hiện tại (Problem Statement) - mô tả pain point cụ thể
3. Giải pháp đề xuất (Proposed Solution) - chi tiết cách thực hiện
4. Đối tượng hưởng lợi (Target Beneficiaries) - ai được lợi
5. Tính khả thi kỹ thuật (Technical Feasibility) - có thể làm không, cần gì
6. Các bước triển khai (Implementation Roadmap) - 3 giai đoạn chính

Viết bằng tiếng Việt, chuyên nghiệp nhưng dễ hiểu. Khoảng 400-500 chữ."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
        )

        return {
            "enhanced_proposal": response.choices[0].message.content or "",
            "step": "idea_enhanced",
        }

    async def _market_analysis(self, state: IdeaState) -> dict:
        prompt = f"""Dựa trên ý tưởng: {state["raw_idea"]}

Hãy phân tích thị trường và tạo dự phóng doanh thu cho Zalopay với:

1. Quy mô thị trường (Market Size)
   - TAM (Total Addressable Market)
   - SAM (Serviceable Addressable Market)
   - SOM (Serviceable Obtainable Market)

2. Dự phóng tác động kinh doanh:
   - Tháng 1-3: Quick wins
   - Tháng 4-6: Growth phase
   - Tháng 7-12: Scale phase
   - Tăng trưởng Sales Volume dự kiến: X%
   - Số người dùng mới ước tính

3. Chi phí triển khai ước tính (Development + Operations)

4. ROI dự kiến trong 12 tháng

Dùng số liệu thực tế của thị trường Fintech Việt Nam. Viết ngắn gọn, có số liệu cụ thể."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
        )

        return {
            "market_analysis": response.choices[0].message.content or "",
            "step": "market_analyzed",
        }

    async def _evaluate_idea(self, state: IdeaState) -> dict:
        prompt = f"""Đánh giá ý tưởng sau theo tiêu chí của Zalopay Ban Giám Đốc:

Ý tưởng: {state["raw_idea"]}
Proposal: {state["enhanced_proposal"][:500]}

Chấm điểm (1-10) theo 3 tiêu chí:
1. Tính khả thi (Feasibility): Có thể triển khai trong 3 tháng không?
2. Chi phí - Hiệu quả (Cost-Efficiency): ROI > 3x trong 1 năm?
3. Tiềm năng doanh số (Revenue Potential): Tác động đến Sales Volume > 5%?

**Lưu ý**: Tên thương hiệu "Zalopay" chỉ viết hoa chữ "Z" chữ "p" phải viết thường.

Trả về JSON:
{{
  "feasibility_score": 7.5,
  "cost_score": 8.0,
  "revenue_potential_score": 6.5,
  "total_score": 7.3,
  "verdict": "APPROVED/REVIEWING/REJECTED",
  "feedback": "Nhận xét ngắn gọn của hội đồng..."
}}"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            response_format={"type": "json_object"},
        )

        text = response.choices[0].message.content or "{}"
        try:
            evaluation = json.loads(text)
        except json.JSONDecodeError:
            evaluation = {
                "feasibility_score": 7.0,
                "cost_score": 7.0,
                "revenue_potential_score": 7.0,
                "total_score": 7.0,
                "verdict": "REVIEWING",
                "feedback": text,
            }

        return {"evaluation": evaluation, "step": "completed"}

    async def enhance_and_evaluate(
        self,
        raw_idea: str,
        employee_name: str,
        department: str,
    ) -> dict:
        initial_state: IdeaState = {
            "messages": [],
            "raw_idea": raw_idea,
            "employee_name": employee_name,
            "department": department,
            "enhanced_proposal": "",
            "market_analysis": "",
            "revenue_projection": "",
            "evaluation": {},
            "step": "start",
        }
        result = await self.graph.ainvoke(initial_state)
        return {
            "enhanced_proposal": result.get("enhanced_proposal", ""),
            "market_analysis": result.get("market_analysis", ""),
            "evaluation": result.get("evaluation", {}),
        }
