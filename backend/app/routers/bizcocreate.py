from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

from ..database import get_db
from ..models.idea import Idea, IdeaStatus
from ..models.gamification import Transaction, TransactionType
from ..models.employee import Employee
from ..agents.orchestrator import orchestrator
from .auth import get_current_employee

router = APIRouter(prefix="/bizcocreate", tags=["biz-cocreate"])


class IdeaSubmitRequest(BaseModel):
    title: str
    raw_idea: str


@router.post("/ideas")
async def submit_idea(
    req: IdeaSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    idea = Idea(
        id=str(uuid.uuid4()),
        employee_id=current_employee.id,
        title=req.title,
        raw_idea=req.raw_idea,
        status=IdeaStatus.ENHANCING,
    )
    db.add(idea)
    await db.commit()
    await db.refresh(idea)

    try:
        ai_result = await orchestrator.process_idea(
            raw_idea=req.raw_idea,
            employee_name=current_employee.full_name,
            department=str(current_employee.department or "tech"),
        )

        idea.enhanced_proposal = ai_result.get("enhanced_proposal", "")
        idea.market_analysis = ai_result.get("market_analysis", "")
        evaluation = ai_result.get("evaluation", {})
        idea.feasibility_score = evaluation.get("feasibility_score", 0)
        idea.cost_score = evaluation.get("cost_score", 0)
        idea.revenue_potential_score = evaluation.get("revenue_potential_score", 0)
        idea.total_score = evaluation.get("total_score", 0)

        verdict = evaluation.get("verdict", "REVIEWING")
        if verdict == "APPROVED":
            idea.status = IdeaStatus.APPROVED
            coins = 500
            tx = Transaction(
                id=str(uuid.uuid4()),
                employee_id=current_employee.id,
                type=TransactionType.EARN,
                amount=coins,
                reason=f"Ý tưởng được duyệt: {req.title}",
                reference_id=idea.id,
            )
            db.add(tx)
            current_employee.bizcoins = (current_employee.bizcoins or 0) + coins
        else:
            idea.status = IdeaStatus.ENHANCED

        idea.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(idea)

        return _idea_dict(idea, evaluation.get("feedback", ""))
    except Exception as e:
        idea.status = IdeaStatus.ENHANCED
        await db.commit()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ideas")
async def list_ideas(
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(
        select(Idea).where(Idea.employee_id == current_employee.id)
    )
    ideas = result.scalars().all()
    return [_idea_dict(i) for i in ideas]


@router.get("/ideas/all")
async def list_all_ideas(
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(select(Idea))
    ideas = result.scalars().all()
    return [_idea_dict(i) for i in ideas]


@router.get("/ideas/{idea_id}")
async def get_idea(
    idea_id: str,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(select(Idea).where(Idea.id == idea_id))
    idea = result.scalar_one_or_none()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return _idea_dict(idea)


def _idea_dict(idea: Idea, feedback: str = "") -> dict:
    return {
        "id": idea.id,
        "title": idea.title,
        "raw_idea": idea.raw_idea,
        "enhanced_proposal": idea.enhanced_proposal,
        "market_analysis": idea.market_analysis,
        "feasibility_score": idea.feasibility_score,
        "cost_score": idea.cost_score,
        "revenue_potential_score": idea.revenue_potential_score,
        "total_score": idea.total_score,
        "status": idea.status,
        "feedback": feedback,
        "created_at": idea.created_at,
        "updated_at": idea.updated_at,
    }
