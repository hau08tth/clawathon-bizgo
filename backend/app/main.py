from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uuid

from .database import init_db, AsyncSessionLocal
from .config import settings
from .routers import (
    auth_router, bizshare_router, bizconnect_router,
    bizcocreate_router, gamification_router, community_router
)


async def seed_data():
    """Seed initial data for demo."""
    from .models.campaign import Campaign
    from .models.gamification import Badge, StoreItem
    from .models.employee import Employee, Department, SocialStyle
    from passlib.context import CryptContext
    from sqlalchemy import select

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async with AsyncSessionLocal() as db:
        # Seed admin user
        result = await db.execute(select(Employee).where(Employee.email == "admin@zalopay.vn"))
        if not result.scalar_one_or_none():
            admin = Employee(
                id=str(uuid.uuid4()),
                email="admin@zalopay.vn",
                full_name="BizGro Admin",
                department=Department.HR,
                position="HR Manager",
                hashed_password=pwd_context.hash("admin123"),
                bizcoins=9999,
                is_admin=True,
            )
            db.add(admin)

        # Seed demo employee
        result = await db.execute(select(Employee).where(Employee.email == "demo@zalopay.vn"))
        if not result.scalar_one_or_none():
            demo = Employee(
                id=str(uuid.uuid4()),
                email="demo@zalopay.vn",
                full_name="Nguyen Van Demo",
                department=Department.TECH,
                position="Software Engineer",
                social_style=SocialStyle.PROFESSIONAL,
                hashed_password=pwd_context.hash("demo123"),
                bizcoins=350,
            )
            db.add(demo)

        # Seed campaigns
        result = await db.execute(select(Campaign))
        if not result.scalars().all():
            campaigns = [
                Campaign(
                    id=str(uuid.uuid4()),
                    title="ZaloPay Số Dư Sinh Lời",
                    product_name="Số Dư Sinh Lời",
                    description="Tính năng giúp người dùng tích lũy lãi suất cao lên đến 5.5%/năm ngay trong ví ZaloPay, không cần chuyển tiền đi đâu hết.",
                    reward_coins=10,
                    commission_rate=5,
                    image_url="https://picsum.photos/seed/zalopay1/400/300",
                ),
                Campaign(
                    id=str(uuid.uuid4()),
                    title="ZaloPay Business - Giải pháp thanh toán doanh nghiệp",
                    product_name="ZaloPay Business",
                    description="Nền tảng thanh toán B2B toàn diện: quản lý chi lương, thanh toán nhà cung cấp, báo cáo tài chính real-time. Phù hợp cho doanh nghiệp 50-500 nhân viên.",
                    reward_coins=15,
                    commission_rate=8,
                    image_url="https://picsum.photos/seed/zalopay2/400/300",
                ),
                Campaign(
                    id=str(uuid.uuid4()),
                    title="ZaloPay QR - Thanh toán không tiền mặt",
                    product_name="ZaloPay QR Payment",
                    description="Giải pháp QR code thanh toán tức thì cho cửa hàng, nhà hàng, dịch vụ. Không cần máy POS, chỉ cần điện thoại.",
                    reward_coins=10,
                    commission_rate=6,
                    image_url="https://picsum.photos/seed/zalopay3/400/300",
                ),
            ]
            for c in campaigns:
                db.add(c)

        # Seed badges
        result = await db.execute(select(Badge))
        if not result.scalars().all():
            badges = [
                Badge(id=str(uuid.uuid4()), name="Chiến thần Lan tỏa", description="Chia sẻ 10+ bài viết", icon="🔥", color="#ef4444", criteria="posts_shared >= 10"),
                Badge(id=str(uuid.uuid4()), name="Đại sứ Kết nối", description="Giới thiệu thành công 5 cơ hội B2B", icon="🤝", color="#3b82f6", criteria="b2b_introductions >= 5"),
                Badge(id=str(uuid.uuid4()), name="Nhà phát minh BizGro", description="Có ý tưởng được duyệt", icon="💡", color="#f59e0b", criteria="ideas_approved >= 1"),
                Badge(id=str(uuid.uuid4()), name="Top Earner", description="Kiếm được 1000+ BizCoins", icon="👑", color="#8b5cf6", criteria="total_coins >= 1000"),
                Badge(id=str(uuid.uuid4()), name="ZaloPay Star", description="Thành viên xuất sắc tháng", icon="⭐", color="#06b6d4", criteria="monthly_top_10"),
            ]
            for b in badges:
                db.add(b)

        # Seed store items
        result = await db.execute(select(StoreItem))
        if not result.scalars().all():
            items = [
                StoreItem(id=str(uuid.uuid4()), name="1 Ngày Phép Đặc Biệt", description="Ngày nghỉ thêm không cần lý do", image_url="https://picsum.photos/seed/store1/200/200", cost=500, stock=10, category="time_off"),
                StoreItem(id=str(uuid.uuid4()), name="Voucher Grab 200k", description="Voucher đặt xe/đồ ăn Grab", image_url="https://picsum.photos/seed/store2/200/200", cost=200, stock=50, category="voucher"),
                StoreItem(id=str(uuid.uuid4()), name="Khóa học Udemy", description="1 khóa học Udemy tự chọn", image_url="https://picsum.photos/seed/store3/200/200", cost=300, stock=20, category="learning"),
                StoreItem(id=str(uuid.uuid4()), name="AirPods Pro", description="Tai nghe Apple AirPods Pro", image_url="https://picsum.photos/seed/store4/200/200", cost=2000, stock=3, category="tech"),
                StoreItem(id=str(uuid.uuid4()), name="Voucher Spa 500k", description="Voucher spa thư giãn cuối tuần", image_url="https://picsum.photos/seed/store5/200/200", cost=400, stock=15, category="wellness"),
                StoreItem(id=str(uuid.uuid4()), name="Chứng chỉ AWS Cloud", description="Thi chứng chỉ AWS do công ty tài trợ", image_url="https://picsum.photos/seed/store6/200/200", cost=800, stock=5, category="learning"),
            ]
            for i in items:
                db.add(i)

        await db.commit()

    # Seed broadcast messages
    from .models.community import ChatMessage, MessageType
    result = await db.execute(select(ChatMessage).where(ChatMessage.is_broadcast == True))
    if not result.scalars().all():
        broadcasts = [
            ChatMessage(
                id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                sender_name="BizGro",
                content="🎉 Chào mừng đến với BizGro Community! Đây là nơi bạn có thể theo dõi tin tức, hỏi về điểm số, hot trends và nhận hỗ trợ từ BizGro AI.",
                is_broadcast=True,
            ),
            ChatMessage(
                id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                sender_name="BizGro",
                content="🔥 Hot trend tuần này: ZaloPay Số Dư Sinh Lời đang được chia sẻ nhiều nhất! Tham gia BIZ-SHARE ngay để kiếm thêm BizCoins 💰",
                is_broadcast=True,
            ),
            ChatMessage(
                id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                sender_name="BizGro",
                content="👑 Bảng xếp hạng tháng này đang được cập nhật! Ai đạt Top 3 sẽ nhận phần thưởng đặc biệt. Hãy tích cực chia sẻ và kết nối nhé!",
                is_broadcast=True,
            ),
        ]
        for b in broadcasts:
            db.add(b)
        await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_data()
    yield


app = FastAPI(
    title="BizGro API",
    description="Business Growth from Within - Multi-Agent AI Platform",
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(bizshare_router)
app.include_router(bizconnect_router)
app.include_router(bizcocreate_router)
app.include_router(gamification_router)
app.include_router(community_router)


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


@app.get("/")
async def root():
    return {
        "app": "BizGro - Business Growth from Within",
        "slogan": "Every Employee a Growth Engine",
        "modules": ["BIZ-SHARE", "BIZ-CONNECT", "BIZ-COCREATE"],
        "docs": "/docs",
    }
