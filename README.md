# BizGro - Business Growth from Within

> Every Employee a Growth Engine - Khi mỗi nhân viên là một động cơ tăng trưởng

## Tổng quan kiến trúc

```
BizGro Platform
├── Frontend (Next.js 14 + Tailwind CSS)
├── Backend (FastAPI + LangGraph Multi-Agent)
│   ├── ContentAgent      → BIZ-SHARE: Tạo nội dung AI
│   ├── NetworkAgent      → BIZ-CONNECT: Match & Pitching
│   ├── IdeaAgent         → BIZ-COCREATE: Enhance & Evaluate
│   └── Orchestrator      → Điều phối toàn bộ agents
├── PostgreSQL            → Persistent storage
├── Redis                 → Cache & Leaderboard
└── Nginx                 → Reverse proxy
```

## Các Module

### 1. BIZ-SHARE (AI Social Selling Hub)
- Chọn chiến dịch từ Commercial
- AI tạo 3 phiên bản bài viết (hài hước / chuyên nghiệp / tâm sự)
- Tự động cá nhân hóa theo phong cách social của nhân viên
- Generate mã affiliate cá nhân
- Track clicks & conversions
- **+10 BizCoins** mỗi lần chia sẻ

### 2. BIZ-CONNECT (AI Referral Matchmaker)
- Nhập danh sách liên hệ (tên, công ty, vị trí)
- AI phân tích và match với ICP (Ideal Customer Profile)
- Tự động generate Ice-breaker & Pitching Script
- Track trạng thái từ Matched → Introduced → Closed
- **+200 BizCoins** khi giới thiệu thành công

### 3. BIZ-COCREATE (AI Idea Incubator)
- Nhân viên gửi ý tưởng thô
- AI tăng cường thành Business Proposal hoàn chỉnh
- Phân tích thị trường + dự phóng doanh thu
- Chấm điểm tự động: Khả thi / Chi phí / Tiềm năng
- **+500 BizCoins** khi ý tưởng được duyệt

### 4. Gamification & Reward Engine
- **BizCoins**: Hệ thống điểm thưởng xuyên suốt
- **Leaderboard**: Bảng xếp hạng real-time
- **Badges**: Huy hiệu vinh danh (Chiến thần Lan tỏa, Đại sứ Kết nối...)
- **BizStore**: Đổi quà (ngày phép, voucher, tech gadgets, khóa học)

## Cài đặt & Chạy

### Prerequisites
- Docker & Docker Compose
- Anthropic API Key

### Bước 1: Clone và cấu hình

```bash
cp .env.example .env
# Điền OPENAI_API_KEY vào .env
```

### Bước 2: Chạy với Docker Compose

```bash
docker-compose up -d
```

### Bước 3: Truy cập

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Nginx (all-in-one)**: http://localhost:80

### Tài khoản demo

| Email | Password | Role |
|-------|----------|------|
| demo@zalopay.vn | demo123 | Employee |
| admin@zalopay.vn | admin123 | Admin |

## Chạy local (không Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL và Redis trước
# Sau đó:
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

## GreenNode AgentBase Deployment

Để deploy lên GreenNode Cloud:

```bash
# Install skills
git clone https://github.com/vngcloud/greennode-agentbase-skills.git
cp -r greennode-agentbase-skills/.claude/skills/* ~/.claude/skills/

# Set credentials
export GREENNODE_CLIENT_ID="your-client-id"
export GREENNODE_CLIENT_SECRET="your-client-secret"

# Deploy via wizard
/agentbase-wizard init bizgro --langgraph
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Zustand |
| Backend | FastAPI, Python 3.12 |
| AI Agents | LangGraph, OpenAI GPT-4o mini |
| Database | PostgreSQL 16 + SQLAlchemy |
| Cache | Redis 7 |
| Proxy | Nginx |
| Deploy | Docker Compose |

## API Endpoints

```
POST   /auth/register        → Đăng ký
POST   /auth/token           → Đăng nhập
GET    /auth/me              → Thông tin user

GET    /bizshare/campaigns   → Danh sách chiến dịch
POST   /bizshare/generate-content → Tạo nội dung AI
POST   /bizshare/share       → Đánh dấu đã chia sẻ

POST   /bizconnect/match     → Phân tích & match contacts
GET    /bizconnect/opportunities → Danh sách cơ hội
PATCH  /bizconnect/opportunities/{id} → Cập nhật trạng thái

POST   /bizcocreate/ideas    → Gửi & AI enhance idea
GET    /bizcocreate/ideas    → Ý tưởng của tôi

GET    /gamification/leaderboard → Bảng xếp hạng
GET    /gamification/my-stats    → Thống kê cá nhân
GET    /gamification/store       → Danh sách quà
POST   /gamification/redeem      → Đổi quà
```
