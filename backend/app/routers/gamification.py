from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from pydantic import BaseModel
from collections import defaultdict
from datetime import datetime, timezone
import uuid

from ..database import get_db
from ..models.gamification import (
    Transaction, TransactionType, Badge, EmployeeBadge,
    StoreItem, Redemption
)
from ..models.employee import Employee
from ..services.teams_notifier import send_to_teams
from .auth import get_current_employee

router = APIRouter(prefix="/gamification", tags=["gamification"])


class RedeemRequest(BaseModel):
    item_id: str


@router.get("/leaderboard")
async def leaderboard(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Employee)
        .where(Employee.is_active == True, Employee.is_admin == False)
        .order_by(desc(Employee.bizcoins))
        .limit(20)
    )
    employees = result.scalars().all()
    if not employees:
        return []

    # Fetch all badges in ONE query instead of N queries
    emp_ids = [e.id for e in employees]
    badges_result = await db.execute(
        select(EmployeeBadge, Badge)
        .join(Badge, EmployeeBadge.badge_id == Badge.id)
        .where(EmployeeBadge.employee_id.in_(emp_ids))
    )
    badges_by_emp: dict = defaultdict(list)
    for eb, b in badges_result.all():
        badges_by_emp[eb.employee_id].append(
            {"name": b.name, "icon": b.icon, "color": b.color}
        )

    return [
        {
            "rank": idx + 1,
            "id": e.id,
            "full_name": e.full_name,
            "department": e.department,
            "position": e.position,
            "avatar_url": e.avatar_url,
            "bizcoins": e.bizcoins or 0,
            "badges": badges_by_emp[e.id],
        }
        for idx, e in enumerate(employees)
    ]


@router.get("/my-stats")
async def my_stats(
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    tx_result = await db.execute(
        select(Transaction).where(Transaction.employee_id == current_employee.id)
    )
    transactions = tx_result.scalars().all()

    total_earned = sum(t.amount for t in transactions if t.type == TransactionType.EARN)
    total_spent = sum(t.amount for t in transactions if t.type == TransactionType.SPEND)

    badges_result = await db.execute(
        select(EmployeeBadge, Badge)
        .join(Badge, EmployeeBadge.badge_id == Badge.id)
        .where(EmployeeBadge.employee_id == current_employee.id)
    )
    badges = [
        {"name": b.name, "icon": b.icon, "color": b.color, "awarded_at": eb.awarded_at}
        for eb, b in badges_result.all()
    ]

    rank_result = await db.execute(
        select(func.count(Employee.id)).where(Employee.bizcoins > (current_employee.bizcoins or 0))
    )
    rank = (rank_result.scalar() or 0) + 1

    return {
        "bizcoins": current_employee.bizcoins or 0,
        "total_earned": total_earned,
        "total_spent": total_spent,
        "rank": rank,
        "badges": badges,
        "recent_transactions": [
            {
                "type": t.type,
                "amount": t.amount,
                "reason": t.reason,
                "created_at": t.created_at,
            }
            for t in sorted(transactions, key=lambda x: x.created_at, reverse=True)[:10]
        ],
    }


@router.get("/store")
async def list_store(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StoreItem).where(StoreItem.is_active == True))
    items = result.scalars().all()
    return [
        {
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "image_url": i.image_url,
            "cost": i.cost,
            "stock": i.stock,
            "category": i.category,
        }
        for i in items
    ]


@router.post("/redeem")
async def redeem_item(
    req: RedeemRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(select(StoreItem).where(StoreItem.id == req.item_id))
    item = result.scalar_one_or_none()
    if not item or not item.is_active:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.stock == 0:
        raise HTTPException(status_code=400, detail="Out of stock")
    if (current_employee.bizcoins or 0) < item.cost:
        raise HTTPException(status_code=400, detail="Insufficient BizCoins")

    current_employee.bizcoins -= item.cost
    if item.stock > 0:
        item.stock -= 1

    redemption = Redemption(
        id=str(uuid.uuid4()),
        employee_id=current_employee.id,
        item_id=item.id,
        coins_spent=item.cost,
    )
    tx = Transaction(
        id=str(uuid.uuid4()),
        employee_id=current_employee.id,
        type=TransactionType.SPEND,
        amount=item.cost,
        reason=f"Đổi quà: {item.name}",
        reference_id=redemption.id,
    )
    db.add(redemption)
    db.add(tx)
    await db.commit()

    notify_text = (
        f"🎁 **{current_employee.full_name}** vừa đổi thành công **{item.name}** "
        f"với {item.cost} BizCoins! 🎉"
    )
    background_tasks.add_task(send_to_teams, notify_text, "🛍️ BizGro — Đổi quà thành công")

    return {
        "message": f"Đổi quà thành công: {item.name}",
        "coins_spent": item.cost,
        "remaining_coins": current_employee.bizcoins,
    }


@router.get("/badges")
async def list_badges(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Badge))
    badges = result.scalars().all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "description": b.description,
            "icon": b.icon,
            "color": b.color,
            "criteria": b.criteria,
        }
        for b in badges
    ]
