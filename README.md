# BizGro — Business Growth from Within

> Every Employee a Growth Engine — Khi mỗi nhân viên là một động cơ tăng trưởng

BizGro là nền tảng gamification giúp nhân viên Zalopay tham gia vào tăng trưởng kinh doanh thông qua 3 module AI và một cộng đồng chatbot tương tác — tất cả được điều phối bởi kiến trúc multi-agent.

---

## Kiến trúc tổng quan

```
BizGro Platform
├── Frontend (Next.js 14 + Tailwind CSS)
│
├── Backend (FastAPI + LangGraph Multi-Agent)
│   ├── ContentAgent   → BIZ-SHARE: Tạo nội dung mạng xã hội
│   ├── IdeaAgent      → BIZ-COCREATE: Phân tích & đánh giá ý tưởng
│   ├── NetworkAgent   → BIZ-CONNECT: Match & tạo Pitching Script
│   ├── ChatAgent      → Community Chatbot & Microsoft Teams Bot
│   └── Orchestrator   → Điều phối toàn bộ agents
│
├── SQLite (aiosqlite)  → Persistent storage
└── Nginx              → Reverse proxy (port 8080)
```

### Luồng xử lý

```
Browser / Teams
      │
      ▼
  nginx :8080
      │
      ├─ /bizshare/*, /bizcocreate/*, /auth/*, ...  ──▶  FastAPI :8000
      │                                                        │
      │                                              BizGroOrchestrator
      │                                     ┌──────┬──────────┼──────────┐
      │                               ContentAgent  IdeaAgent  NetworkAgent  ChatAgent
      │                               (LangGraph)  (LangGraph)  (LangGraph)   (LLM)
      │
      └─ /  ──────────────────────────────────────────────▶  Next.js :3000
```

---

## Các Module

### 1. BIZ-SHARE — AI Social Selling Hub

Nhân viên chọn chiến dịch từ Commercial, AI tự động tạo 3 phiên bản bài viết phù hợp với phong cách cá nhân, kèm mã affiliate để track chuyển đổi.

- Chọn chiến dịch (Số Dư Sinh Lời, Business, QR Payment...)
- Chọn nền tảng: Facebook / LinkedIn / TikTok
- AI sinh 3 biến thể: hài hước · chuyên nghiệp · tâm sự
- Tự động sinh mã affiliate cá nhân
- Track clicks & conversions
- **+10 BizCoins** khi chia sẻ

**Agent**: `ContentAgent` — LangGraph pipeline: `generate_posts → optimize_post`

### 2. BIZ-CONNECT — AI Referral Matchmaker

Nhân viên nhập danh sách liên hệ, AI phân tích và match với Ideal Customer Profile của Zalopay, tự động tạo Ice-breaker và Pitching Script.

- Nhập danh sách contact (tên, công ty, vị trí)
- AI match với ICP (SME / Startup / Retail)
- Tạo Ice-breaker ngắn & Pitching Script đầy đủ
- Track trạng thái: Matched → Introduced → Closed
- **+200 BizCoins** khi giới thiệu thành công

**Agent**: `NetworkAgent` — LangGraph pipeline: `analyze_contacts → generate_scripts`

### 3. BIZ-COCREATE — AI Idea Incubator

Nhân viên gửi ý tưởng thô, AI qua 3 bước tự động nâng cấp thành Business Proposal hoàn chỉnh kèm phân tích thị trường và điểm đánh giá.

- Gửi ý tưởng ngắn bằng ngôn ngữ tự nhiên
- AI **tăng cường** thành Business Proposal (400–500 từ)
- AI **phân tích thị trường**: TAM/SAM/SOM, dự phóng doanh thu 12 tháng
- AI **chấm điểm**: Khả thi · Chi phí · Tiềm năng doanh số (1–10)
- Verdict: APPROVED / REVIEWING / REJECTED
- **+500 BizCoins** khi ý tưởng được duyệt

**Agent**: `IdeaAgent` — LangGraph pipeline: `enhance_idea → analyze_market → evaluate_idea`

### 4. Community Chatbot — BizGro AI Assistant

Kênh chat cộng đồng trong ứng dụng và tích hợp Microsoft Teams. Chatbot có context về leaderboard, hot trends, chiến dịch đang chạy và hướng dẫn kiếm BizCoins.

- Chat real-time trong ứng dụng (`/community`)
- Nhận broadcast từ admin
- Polling 10 giây để cập nhật tin nhắn mới
- **Teams Outgoing Webhook**: HMAC-verified, trả lời ngay trong Teams channel
- Teams callback URL: `https://endpoint-487619c8-18ad-448f-8267-268ddce4aae7.agentbase-runtime.aiplatform.vngcloud.vn/teams/webhook`

**Agent**: `ChatAgent` — Direct LLM call với system prompt chứa context (leaderboard top 5, trends, campaigns)

### 5. Gamification & Reward Engine

- **BizCoins**: Hệ thống điểm thưởng xuyên suốt
- **Leaderboard**: Bảng xếp hạng top 20 real-time
- **Badges**: Chiến thần Lan tỏa · Đại sứ Kết nối · Nhà phát minh · Top Earner · Zalopay Star
- **BizStore**: Đổi quà — Ngày phép (500 coins) · AirPods Pro (2000 coins) · Grab voucher · AWS cert...

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Zustand |
| Backend | FastAPI 0.115, Python 3.12, uvicorn |
| AI Agents | LangGraph 0.2, OpenAI SDK (OpenAI-compatible) |
| LLM | `google/gemma-4-31b-it` via GreenNode MAAS |
| Database | SQLite + SQLAlchemy 2.0 async (aiosqlite) |
| Auth | JWT (HS256) + bcrypt, Teams HMAC-SHA256 |
| Process mgmt | supervisord (backend + frontend + nginx) |
| Proxy | Nginx 8080 → uvicorn 8000 / Next.js 3000 |
| Container | Single Docker image (Python 3.12 base) |
| Deploy | GreenNode AgentBase Runtime |

---

## Deployment Architecture

Toàn bộ ứng dụng chạy trong **một Docker container duy nhất**:

```
Docker Container (port 8080 exposed)
├── supervisord
│   ├── nginx        :8080  — public entry point, reverse proxy
│   ├── uvicorn      :8000  — FastAPI backend (2 workers)
│   └── node         :3000  — Next.js frontend (standalone)
└── bizgro.db               — SQLite database
```

### GreenNode AgentBase Runtimes

| Runtime | URL | Dùng cho |
|---------|-----|----------|
| `clawathon-bizgo` | `https://endpoint-487619c8-18ad-448f-8267-268ddce4aae7.agentbase-runtime.aiplatform.vngcloud.vn` | Backend + Frontend combined |
| `clawathon-bizgo-ui` | `https://endpoint-c807eb5c-098b-4a49-852a-3bc459004060.agentbase-runtime.aiplatform.vngcloud.vn` | Frontend only (trỏ vào backend trên) |

Container Registry: `vcr.vngcloud.vn/111480-abp111947`

### Nginx timeout configuration

| Route | Timeout | Lý do |
|-------|---------|-------|
| `POST /bizshare/generate-content` | 300s | 1 LLM call, token count lớn |
| `~ ^/bizcocreate` | 300s | 3 LLM calls tuần tự |
| Các route còn lại | 120s | Standard |

---

## API Endpoints

```
# Auth
POST   /auth/register
POST   /auth/token               → JWT login
GET    /auth/me

# BIZ-SHARE
GET    /bizshare/campaigns
POST   /bizshare/generate-content    → ContentAgent (300s timeout)
POST   /bizshare/share
GET    /bizshare/my-posts
GET    /bizshare/track/{affiliate_code}

# BIZ-CONNECT
POST   /bizconnect/match             → NetworkAgent
GET    /bizconnect/opportunities
PATCH  /bizconnect/opportunities/{id}

# BIZ-COCREATE
POST   /bizcocreate/ideas            → IdeaAgent (300s timeout)
GET    /bizcocreate/ideas            → ý tưởng của tôi
GET    /bizcocreate/ideas/all        → tất cả (admin)
GET    /bizcocreate/ideas/{id}

# Gamification
GET    /gamification/leaderboard
GET    /gamification/my-stats
GET    /gamification/store
GET    /gamification/badges
POST   /gamification/redeem

# Community Chat
GET    /community/feed
POST   /community/chat               → ChatAgent
POST   /community/broadcast          → admin only

# Microsoft Teams
POST   /teams/webhook                → HMAC-verified, ChatAgent

# System
GET    /health
GET    /docs                         → Swagger UI
```

---

## Cài đặt & Chạy local

### Prerequisites

- Python 3.12+
- Node.js 20+
- GreenNode MAAS API key (hoặc bất kỳ OpenAI-compatible endpoint)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Điền OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

Truy cập: `http://localhost:3000` · API docs: `http://localhost:8000/docs`

### Tài khoản demo

| Email | Password | Role |
|-------|----------|------|
| demo@zalopay.vn | demo123 | Employee |
| admin@zalopay.vn | admin123 | Admin |

---

## Deploy lên GreenNode AgentBase

### Yêu cầu

```bash
git clone https://github.com/vngcloud/greennode-agentbase-skills.git
cp -r greennode-agentbase-skills/.claude/skills/* ~/.claude/skills/

export GREENNODE_CLIENT_ID="your-client-id"
export GREENNODE_CLIENT_SECRET="your-client-secret"
```

### Build & Push

```bash
# Login Container Registry
bash .claude/skills/agentbase/scripts/cr.sh credentials docker-login

# Combined image (backend + frontend + nginx)
docker build --platform linux/amd64 \
  -t vcr.vngcloud.vn/111480-abp111947/clawathon-bizgo:latest .

# Frontend-only image
docker build --platform linux/amd64 \
  --build-arg NEXT_PUBLIC_API_URL=https://endpoint-487619c8-18ad-448f-8267-268ddce4aae7.agentbase-runtime.aiplatform.vngcloud.vn \
  -t vcr.vngcloud.vn/111480-abp111947/clawathon-bizgo-ui:latest \
  -f frontend/Dockerfile frontend/

docker push vcr.vngcloud.vn/111480-abp111947/clawathon-bizgo:latest
docker push vcr.vngcloud.vn/111480-abp111947/clawathon-bizgo-ui:latest
```

### Update runtimes

```bash
bash .claude/skills/agentbase/scripts/runtime.sh update runtime-909ff08b-37e6-4b4f-af16-f237ba4d35d0 \
  --image vcr.vngcloud.vn/111480-abp111947/clawathon-bizgo:latest \
  --from-cr --env-file .env.deploy
```

---

## Microsoft Teams Integration

| Loại | Hướng | Mục đích |
|------|-------|---------|
| Incoming Webhook | BizGro → Teams | Thông báo: leaderboard, broadcast, coin award |
| Outgoing Webhook | Teams → BizGro | Chatbot: nhân viên hỏi trong Teams channel |

**Callback URL cho Outgoing Webhook:**

```
https://endpoint-487619c8-18ad-448f-8267-268ddce4aae7.agentbase-runtime.aiplatform.vngcloud.vn/teams/webhook
```

- HMAC-SHA256 signature verification (header `Authorization`)
- Trả lời trong 5 giây (FastAPI BackgroundTasks)
- Cùng `ChatAgent` với Community chat — context-aware

---

## Environment Variables

| Variable | Mô tả |
|----------|-------|
| `OPENAI_API_KEY` | API key cho LLM (GreenNode MAAS hoặc OpenAI) |
| `OPENAI_BASE_URL` | LLM endpoint |
| `OPENAI_MODEL` | Model ID, VD: `google/gemma-4-31b-it` |
| `DATABASE_URL` | SQLite URL, VD: `sqlite+aiosqlite:///./bizgro.db` |
| `SECRET_KEY` | JWT signing key |
| `TEAMS_INCOMING_WEBHOOK_URL` | URL Incoming Webhook của Teams channel |
| `TEAMS_WEBHOOK_SECRET` | HMAC secret cho Outgoing Webhook verification |

---

## Seed Data

Khi backend khởi động lần đầu, `main.py::seed_data()` tự động tạo:

- 1 admin + 1 demo user + 19 nhân viên mẫu (đủ leaderboard)
- 3 chiến dịch active (Số Dư Sinh Lời · Zalopay Business · QR Payment)
- 5 badges (Chiến thần Lan tỏa · Đại sứ Kết nối · Nhà phát minh · Top Earner · Zalopay Star)
- 6 store items (Ngày phép · Grab voucher · Udemy · AirPods Pro · Spa · AWS cert)
- 4 system broadcast messages
