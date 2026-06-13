from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

from ..database import get_db
from ..models.connection import Connection, Opportunity, OpportunityStatus
from ..models.gamification import Transaction, TransactionType
from ..models.employee import Employee
from ..agents.orchestrator import orchestrator
from .auth import get_current_employee

router = APIRouter(prefix="/bizconnect", tags=["biz-connect"])


class ContactItem(BaseModel):
    name: str
    company: str
    position: str = ""
    email: str = ""
    relationship: str = "colleague"


class MatchRequest(BaseModel):
    contacts: list[ContactItem]


class UpdateOpportunityStatus(BaseModel):
    status: OpportunityStatus


@router.post("/match")
async def match_contacts(
    req: MatchRequest,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    contacts_data = [c.model_dump() for c in req.contacts]

    ai_result = await orchestrator.match_network(
        employee_name=current_employee.full_name,
        employee_position=current_employee.position or "Employee",
        department=str(current_employee.department or "tech"),
        contacts=contacts_data,
    )

    saved_connections = []
    for contact in req.contacts:
        conn = Connection(
            id=str(uuid.uuid4()),
            employee_id=current_employee.id,
            contact_name=contact.name,
            contact_company=contact.company,
            contact_position=contact.position,
            contact_email=contact.email,
            relationship_type=contact.relationship,
        )
        db.add(conn)
        saved_connections.append(conn)

    await db.flush()

    opportunities_created = []
    for script in ai_result.get("scripts", []):
        conn = next(
            (c for c in saved_connections if c.contact_name == script.get("contact_name")),
            saved_connections[0] if saved_connections else None,
        )
        if not conn:
            continue

        opp = Opportunity(
            id=str(uuid.uuid4()),
            connection_id=conn.id,
            employee_id=current_employee.id,
            match_reason=script.get("match_reason", ""),
            pitching_script=script.get("pitching_script", ""),
            ice_breaker=script.get("ice_breaker", ""),
            status=OpportunityStatus.MATCHED,
        )
        db.add(opp)
        opportunities_created.append({
            "id": opp.id,
            "contact_name": script.get("contact_name", ""),
            "contact_company": script.get("contact_company", ""),
            "contact_position": script.get("contact_position", ""),
            "match_score": script.get("match_score", 0),
            "match_reason": script.get("match_reason", ""),
            "ice_breaker": script.get("ice_breaker", ""),
            "pitching_script": script.get("pitching_script", ""),
        })

    await db.commit()
    return {
        "total_contacts": len(req.contacts),
        "matches_found": len(opportunities_created),
        "opportunities": opportunities_created,
    }


@router.get("/opportunities")
async def list_opportunities(
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(
        select(Opportunity).where(Opportunity.employee_id == current_employee.id)
    )
    opps = result.scalars().all()

    enriched = []
    for opp in opps:
        conn_result = await db.execute(select(Connection).where(Connection.id == opp.connection_id))
        conn = conn_result.scalar_one_or_none()
        enriched.append({
            "id": opp.id,
            "contact_name": conn.contact_name if conn else "",
            "contact_company": conn.contact_company if conn else "",
            "contact_position": conn.contact_position if conn else "",
            "match_reason": opp.match_reason,
            "ice_breaker": opp.ice_breaker,
            "pitching_script": opp.pitching_script,
            "status": opp.status,
            "reward_coins": opp.reward_coins,
            "created_at": opp.created_at,
        })

    return enriched


@router.patch("/opportunities/{opp_id}")
async def update_opportunity(
    opp_id: str,
    req: UpdateOpportunityStatus,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(select(Opportunity).where(Opportunity.id == opp_id))
    opp = result.scalar_one_or_none()
    if not opp or opp.employee_id != current_employee.id:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    old_status = opp.status
    opp.status = req.status
    opp.updated_at = datetime.utcnow()

    coins_earned = 0
    if req.status == OpportunityStatus.INTRODUCED and old_status == OpportunityStatus.MATCHED:
        coins_earned = 200
        tx = Transaction(
            id=str(uuid.uuid4()),
            employee_id=current_employee.id,
            type=TransactionType.EARN,
            amount=coins_earned,
            reason="Giới thiệu thành công cuộc hẹn B2B",
            reference_id=opp.id,
        )
        db.add(tx)
        current_employee.bizcoins = (current_employee.bizcoins or 0) + coins_earned

    await db.commit()
    return {"status": opp.status, "coins_earned": coins_earned}
