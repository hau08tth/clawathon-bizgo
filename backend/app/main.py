from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uuid

from .database import init_db, AsyncSessionLocal
from .config import settings
from .routers import (
    auth_router, bizshare_router, bizconnect_router,
    bizcocreate_router, gamification_router, community_router,
    teams_router
)


async def seed_data():
    """Seed initial data for demo."""
    from .models.campaign import Campaign
    from .models.gamification import Badge, StoreItem, Transaction, TransactionType
    from .models.employee import Employee, Department, SocialStyle
    from .models.community import ChatMessage, MessageType
    from passlib.context import CryptContext
    from sqlalchemy import select
    from datetime import datetime, timedelta

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async with AsyncSessionLocal() as db:
        # ── Admin ────────────────────────────────────────────────────────────
        result = await db.execute(select(Employee).where(Employee.email == "admin@zalopay.vn"))
        if not result.scalar_one_or_none():
            db.add(Employee(
                id=str(uuid.uuid4()),
                email="admin@zalopay.vn",
                full_name="BizGro Admin",
                department=Department.HR,
                position="HR Manager",
                hashed_password=pwd_context.hash("admin123"),
                bizcoins=9999,
                is_admin=True,
            ))

        # ── Demo user (rank ~#16 to feel progress) ───────────────────────────
        result = await db.execute(select(Employee).where(Employee.email == "demo@zalopay.vn"))
        demo_row = result.scalar_one_or_none()
        if not demo_row:
            demo_id = str(uuid.uuid4())
            db.add(Employee(
                id=demo_id,
                email="demo@zalopay.vn",
                full_name="Nguyen Van Demo",
                department=Department.TECH,
                position="Software Engineer",
                social_style=SocialStyle.PROFESSIONAL,
                hashed_password=pwd_context.hash("demo123"),
                bizcoins=350,
            ))
            db.add(Transaction(
                id=str(uuid.uuid4()),
                employee_id=demo_id,
                type=TransactionType.EARN,
                amount=200,
                reason="Chia sẻ bài viết Zalopay Số Dư Sinh Lời",
                created_at=datetime.utcnow() - timedelta(days=3),
            ))
            db.add(Transaction(
                id=str(uuid.uuid4()),
                employee_id=demo_id,
                type=TransactionType.EARN,
                amount=150,
                reason="Giới thiệu cơ hội B2B thành công",
                created_at=datetime.utcnow() - timedelta(days=1),
            ))

        # ── 19 leaderboard sample employees ─────────────────────────────────
        SAMPLE = [
            # (email, full_name, dept, position, coins, transactions)
            ("anhnv@zalopay.vn",   "Nguyễn Thị Anh",    Department.MARKETING,   "Marketing Lead",       2450,
             [("Chia sẻ 45 bài viết viral về Zalopay", 800), ("Giới thiệu 8 đối tác B2B", 600), ("Nộp 3 ý tưởng sản phẩm", 500), ("Hoàn thành chiến dịch Q4", 550)]),
            ("tuantm@zalopay.vn",  "Trần Minh Tuấn",    Department.TECH,        "Senior Engineer",      2180,
             [("Chia sẻ Zalopay Business lên LinkedIn", 700), ("Kết nối B2B với TechCorp", 480), ("Ý tưởng tối ưu thanh toán QR", 600), ("Hoàn thành challenge tháng 11", 400)]),
            ("namlh@zalopay.vn",   "Lê Hoàng Nam",      Department.SALES,       "Sales Manager",        1920,
             [("Chia sẻ chiến dịch QR Payment", 600), ("Giới thiệu 6 khách hàng doanh nghiệp", 700), ("Đề xuất tính năng mới", 420), ("Top Sales tháng 10", 200)]),
            ("huongpt@zalopay.vn", "Phạm Thu Hương",    Department.PRODUCT,     "Product Manager",      1740,
             [("Chia sẻ roadmap Zalopay 2025", 500), ("Kết nối 4 cơ hội B2B", 440), ("Nộp ý tưởng gamification", 600), ("Workshop nội bộ", 200)]),
            ("duchv@zalopay.vn",   "Hoàng Văn Đức",     Department.TECH,        "Tech Lead",            1580,
             [("Chia sẻ bài viết kỹ thuật Zalopay", 480), ("Giới thiệu vendor B2B", 350), ("Ý tưởng tối ưu hiệu năng", 500), ("Mentor junior dev", 250)]),
            ("lanvt@zalopay.vn",   "Vũ Thị Lan",        Department.MARKETING,   "Brand Manager",        1380,
             [("Tạo content viral Zalopay", 450), ("Kết nối agency B2B", 330), ("Chiến dịch brand awareness", 400), ("Sự kiện offline", 200)]),
            ("khoaDM@zalopay.vn",  "Đặng Minh Khoa",    Department.TECH,        "Backend Engineer",     1200,
             [("Chia sẻ tech blog Zalopay", 400), ("Giới thiệu đối tác fintech", 300), ("Ý tưởng API mới", 350), ("Hackathon nội bộ", 150)]),
            ("hoabt@zalopay.vn",   "Bùi Thị Hoa",       Department.HR,          "HR Business Partner",  1020,
             [("Chia sẻ văn hoá Zalopay", 350), ("Kết nối talent B2B", 270), ("Chương trình wellness", 250), ("Referral nhân sự", 150)]),
            ("huynq@zalopay.vn",   "Ngô Quang Huy",     Department.OPERATIONS,  "Ops Manager",          860,
             [("Chia sẻ quy trình vận hành", 300), ("Kết nối nhà cung cấp", 260), ("Tối ưu workflow", 200), ("Đào tạo nội bộ", 100)]),
            ("nhunglt@zalopay.vn", "Lý Thị Nhung",      Department.FINANCE,     "Finance Analyst",      730,
             [("Chia sẻ báo cáo tài chính", 250), ("Giới thiệu đối tác kiểm toán", 230), ("Phân tích xu hướng", 150), ("Workshop Excel", 100)]),
            ("kientv@zalopay.vn",  "Trịnh Văn Kiên",    Department.TECH,        "Frontend Engineer",    640,
             [("Chia sẻ UI/UX Zalopay", 220), ("Kết nối designer B2B", 180), ("Cải thiện accessibility", 200), ("Code review", 40)]),
            ("maipt@zalopay.vn",   "Phan Thị Mai",      Department.PRODUCT,     "UX Designer",          560,
             [("Chia sẻ design system", 200), ("Workshop UX với khách hàng", 160), ("Ý tưởng cải thiện onboarding", 200)]),
            ("binhdv@zalopay.vn",  "Dương Văn Bình",    Department.SALES,       "Sales Executive",      490,
             [("Chia sẻ case study Zalopay", 180), ("Giới thiệu SME B2B", 170), ("Cold calling thành công", 140)]),
            ("trimt@zalopay.vn",   "Cao Minh Trí",      Department.TECH,        "Data Engineer",        430,
             [("Chia sẻ data insight Zalopay", 160), ("Kết nối đối tác data", 150), ("Dashboard nội bộ", 120)]),
            ("thuvt@zalopay.vn",   "Vũ Thị Thu",        Department.HR,          "Recruiter",            390,
             [("Chia sẻ employer branding", 150), ("Giới thiệu ứng viên tốt", 140), ("Job fair Zalopay", 100)]),
            ("tainhv@zalopay.vn",  "Nguyễn Văn Tài",    Department.MARKETING,   "Content Creator",      300,
             [("Chia sẻ video Zalopay TikTok", 130), ("Collab với KOL", 100), ("Bài viết blog", 70)]),
            ("vylt@zalopay.vn",    "Lê Thị Vy",         Department.FINANCE,     "Accountant",           250,
             [("Chia sẻ mẹo tài chính cá nhân", 100), ("Giới thiệu đối tác", 90), ("Báo cáo tháng", 60)]),
            ("dathm@zalopay.vn",   "Hồ Minh Đạt",       Department.TECH,        "QA Engineer",          190,
             [("Chia sẻ bug bounty Zalopay", 80), ("Kết nối tester B2B", 70), ("Test automation", 40)]),
            ("xuandt@zalopay.vn",  "Đinh Thị Xuân",     Department.OPERATIONS,  "Operations Analyst",   130,
             [("Chia sẻ tips vận hành", 60), ("Hỗ trợ đồng nghiệp", 40), ("Báo cáo KPI", 30)]),
        ]

        result = await db.execute(select(Employee).where(Employee.email == SAMPLE[0][0]))
        if not result.scalar_one_or_none():
            for email, name, dept, pos, coins, txs in SAMPLE:
                emp_id = str(uuid.uuid4())
                db.add(Employee(
                    id=emp_id,
                    email=email,
                    full_name=name,
                    department=dept,
                    position=pos,
                    hashed_password=pwd_context.hash("demo123"),
                    bizcoins=coins,
                    social_style=SocialStyle.PROFESSIONAL,
                ))
                total = 0
                for i, (reason, amount) in enumerate(txs):
                    total += amount
                    db.add(Transaction(
                        id=str(uuid.uuid4()),
                        employee_id=emp_id,
                        type=TransactionType.EARN,
                        amount=amount,
                        reason=reason,
                        created_at=datetime.utcnow() - timedelta(days=30 - i * 5),
                    ))

        # ── Campaigns ────────────────────────────────────────────────────────
        result = await db.execute(select(Campaign))
        if not result.scalars().all():
            for c in [
                Campaign(id=str(uuid.uuid4()), title="Zalopay Số Dư Sinh Lời", product_name="Số Dư Sinh Lời",
                         description="Tính năng giúp người dùng tích lũy lãi suất cao lên đến 5.5%/năm ngay trong ví Zalopay.",
                         reward_coins=10, commission_rate=5, image_url="https://picsum.photos/seed/zalopay1/400/300"),
                Campaign(id=str(uuid.uuid4()), title="Zalopay Business - Giải pháp thanh toán doanh nghiệp", product_name="Zalopay Business",
                         description="Nền tảng thanh toán B2B toàn diện: quản lý chi lương, thanh toán nhà cung cấp, báo cáo tài chính real-time.",
                         reward_coins=15, commission_rate=8, image_url="https://picsum.photos/seed/zalopay2/400/300"),
                Campaign(id=str(uuid.uuid4()), title="Zalopay QR - Thanh toán không tiền mặt", product_name="Zalopay QR Payment",
                         description="Giải pháp QR code thanh toán tức thì cho cửa hàng, nhà hàng. Không cần máy POS.",
                         reward_coins=10, commission_rate=6, image_url="https://picsum.photos/seed/zalopay3/400/300"),
            ]:
                db.add(c)

        # ── Badges ───────────────────────────────────────────────────────────
        result = await db.execute(select(Badge))
        if not result.scalars().all():
            for b in [
                Badge(id=str(uuid.uuid4()), name="Chiến thần Lan tỏa", description="Chia sẻ 10+ bài viết", icon="🔥", color="#ef4444", criteria="posts_shared >= 10"),
                Badge(id=str(uuid.uuid4()), name="Đại sứ Kết nối", description="Giới thiệu thành công 5 cơ hội B2B", icon="🤝", color="#3b82f6", criteria="b2b_introductions >= 5"),
                Badge(id=str(uuid.uuid4()), name="Nhà phát minh BizGro", description="Có ý tưởng được duyệt", icon="💡", color="#f59e0b", criteria="ideas_approved >= 1"),
                Badge(id=str(uuid.uuid4()), name="Top Earner", description="Kiếm được 1000+ BizCoins", icon="👑", color="#8b5cf6", criteria="total_coins >= 1000"),
                Badge(id=str(uuid.uuid4()), name="Zalopay Star", description="Thành viên xuất sắc tháng", icon="⭐", color="#06b6d4", criteria="monthly_top_10"),
            ]:
                db.add(b)

        # ── Store items ───────────────────────────────────────────────────────
        result = await db.execute(select(StoreItem))
        if not result.scalars().all():
            for i in [
                StoreItem(id=str(uuid.uuid4()), name="1 Ngày Phép Đặc Biệt", description="Ngày nghỉ thêm không cần lý do", image_url="https://picsum.photos/seed/store1/200/200", cost=500, stock=10, category="time_off"),
                StoreItem(id=str(uuid.uuid4()), name="Voucher Grab 200k", description="Voucher đặt xe/đồ ăn Grab", image_url="https://picsum.photos/seed/store2/200/200", cost=200, stock=50, category="voucher"),
                StoreItem(id=str(uuid.uuid4()), name="Khóa học Udemy", description="1 khóa học Udemy tự chọn", image_url="https://picsum.photos/seed/store3/200/200", cost=300, stock=20, category="learning"),
                StoreItem(id=str(uuid.uuid4()), name="AirPods Pro", description="Tai nghe Apple AirPods Pro", image_url="https://picsum.photos/seed/store4/200/200", cost=2000, stock=3, category="tech"),
                StoreItem(id=str(uuid.uuid4()), name="Voucher Spa 500k", description="Voucher spa thư giãn cuối tuần", image_url="https://picsum.photos/seed/store5/200/200", cost=400, stock=15, category="wellness"),
                StoreItem(id=str(uuid.uuid4()), name="Chứng chỉ AWS Cloud", description="Thi chứng chỉ AWS do công ty tài trợ", image_url="https://picsum.photos/seed/store6/200/200", cost=800, stock=5, category="learning"),
            ]:
                db.add(i)

        # ── Broadcasts ───────────────────────────────────────────────────────
        result = await db.execute(select(ChatMessage).where(ChatMessage.is_broadcast == True))
        if not result.scalars().all():
            for b in [
                ChatMessage(id=str(uuid.uuid4()), type=MessageType.SYSTEM, sender_name="BizGro",
                            content="🎉 Chào mừng đến với BizGro Community! Đây là nơi bạn theo dõi tin tức, hỏi về điểm số, hot trends và nhận hỗ trợ từ BizGro AI.",
                            is_broadcast=True,
                            created_at=datetime.utcnow() - timedelta(days=7)),
                ChatMessage(id=str(uuid.uuid4()), type=MessageType.SYSTEM, sender_name="BizGro",
                            content="🏆 Bảng xếp hạng tháng này: Nguyễn Thị Anh đang dẫn đầu với 2.450 BizCoins! Trần Minh Tuấn bám sát ở vị trí #2 với 2.180 coins. Ai sẽ là người bứt phá tiếp theo? 🚀",
                            is_broadcast=True,
                            created_at=datetime.utcnow() - timedelta(days=3)),
                ChatMessage(id=str(uuid.uuid4()), type=MessageType.SYSTEM, sender_name="BizGro",
                            content="🔥 Hot trend tuần này: Zalopay Số Dư Sinh Lời đang được chia sẻ nhiều nhất! Top sharer đang kiếm 800 BizCoins/tuần. Tham gia BIZ-SHARE ngay 💰",
                            is_broadcast=True,
                            created_at=datetime.utcnow() - timedelta(days=2)),
                ChatMessage(id=str(uuid.uuid4()), type=MessageType.SYSTEM, sender_name="BizGro",
                            content="🎁 Nhắc nhở: Bạn có thể đổi BizCoins lấy AirPods Pro (2.000 coins), 1 Ngày Phép (500 coins) và nhiều quà hấp dẫn khác tại BizStore!",
                            is_broadcast=True,
                            created_at=datetime.utcnow() - timedelta(hours=12)),
            ]:
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
app.include_router(teams_router)


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
