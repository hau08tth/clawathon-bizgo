from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid
import random
import string

from ..database import get_db
from ..models.campaign import Campaign, Post, Platform, PostStatus
from ..models.gamification import Transaction, TransactionType
from ..models.employee import Employee
from ..agents.orchestrator import orchestrator
from .auth import get_current_employee

router = APIRouter(prefix="/bizshare", tags=["biz-share"])


class GenerateContentRequest(BaseModel):
    campaign_id: str
    platform: str
    use_profile_url: str = ""


class SharePostRequest(BaseModel):
    post_id: str
    post_url: str


class CampaignCreate(BaseModel):
    title: str
    product_name: str
    description: str
    reward_coins: int = 10
    commission_rate: int = 5
    image_url: str = ""


def _gen_affiliate_code(employee_id: str, campaign_id: str) -> str:
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"BG-{employee_id[:4].upper()}-{suffix}"


@router.get("/campaigns")
async def list_campaigns(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Campaign).where(Campaign.is_active == True))
    campaigns = result.scalars().all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "product_name": c.product_name,
            "description": c.description,
            "reward_coins": c.reward_coins,
            "commission_rate": c.commission_rate,
            "image_url": c.image_url,
        }
        for c in campaigns
    ]


@router.post("/campaigns", status_code=201)
async def create_campaign(
    req: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    if not current_employee.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    campaign = Campaign(
        id=str(uuid.uuid4()),
        title=req.title,
        product_name=req.product_name,
        description=req.description,
        reward_coins=req.reward_coins,
        commission_rate=req.commission_rate,
        image_url=req.image_url,
    )
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return {"id": campaign.id, "title": campaign.title}


@router.post("/generate-content")
async def generate_content(
    req: GenerateContentRequest,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(select(Campaign).where(Campaign.id == req.campaign_id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    ai_result = await orchestrator.generate_content(
        product_name=campaign.product_name,
        product_description=campaign.description,
        platform=req.platform,
        social_style=str(current_employee.social_style.value if hasattr(current_employee.social_style, 'value') else current_employee.social_style or "professional"),
        employee_name=current_employee.full_name,
        department=str(current_employee.department or "tech"),
    )

    affiliate_code = _gen_affiliate_code(current_employee.id, campaign.id)

    posts_created = []
    for post_data in ai_result.get("posts", []):
        post = Post(
            id=str(uuid.uuid4()),
            employee_id=current_employee.id,
            campaign_id=campaign.id,
            platform=Platform(req.platform),
            content=post_data.get("content", ""),
            affiliate_code=affiliate_code + f"-{post_data.get('style', 'std')[:3].upper()}",
            status=PostStatus.DRAFT,
        )
        db.add(post)
        posts_created.append({
            "id": post.id,
            "style": post_data.get("style", ""),
            "content": post.content,
            "hashtags": post_data.get("hashtags", []),
            "affiliate_code": post.affiliate_code,
            "platform": req.platform,
        })

    await db.commit()
    return {
        "posts": posts_created,
        "recommended": ai_result.get("recommended", ""),
        "affiliate_code": affiliate_code,
    }


@router.post("/share")
async def share_post(
    req: SharePostRequest,
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(select(Post).where(Post.id == req.post_id))
    post = result.scalar_one_or_none()
    if not post or post.employee_id != current_employee.id:
        raise HTTPException(status_code=404, detail="Post not found")

    post.status = PostStatus.SHARED
    post.post_url = req.post_url
    post.shared_at = datetime.utcnow()

    result2 = await db.execute(select(Campaign).where(Campaign.id == post.campaign_id))
    campaign = result2.scalar_one_or_none()
    coins = campaign.reward_coins if campaign else 10

    tx = Transaction(
        id=str(uuid.uuid4()),
        employee_id=current_employee.id,
        type=TransactionType.EARN,
        amount=coins,
        reason=f"Chia sẻ bài viết chiến dịch: {campaign.title if campaign else 'N/A'}",
        reference_id=post.id,
    )
    db.add(tx)
    current_employee.bizcoins = (current_employee.bizcoins or 0) + coins

    await db.commit()
    return {"message": "Post shared successfully", "coins_earned": coins, "total_coins": current_employee.bizcoins}


@router.get("/my-posts")
async def my_posts(
    db: AsyncSession = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    result = await db.execute(
        select(Post).where(Post.employee_id == current_employee.id)
    )
    posts = result.scalars().all()
    return [
        {
            "id": p.id,
            "campaign_id": p.campaign_id,
            "platform": p.platform,
            "content": p.content,
            "affiliate_code": p.affiliate_code,
            "status": p.status,
            "clicks": p.clicks,
            "conversions": p.conversions,
            "shared_at": p.shared_at,
        }
        for p in posts
    ]


@router.get("/track/{affiliate_code}")
async def track_click(affiliate_code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.affiliate_code == affiliate_code))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Invalid affiliate code")
    post.clicks += 1
    await db.commit()
    return {"message": "Tracked", "clicks": post.clicks}
