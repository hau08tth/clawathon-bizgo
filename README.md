# 🚀 BizGro — Biến Mọi Nhân Viên Thành Động Cơ Tăng Trưởng

> Every Employee a Growth Engine — Khi mỗi nhân viên là một động cơ tăng trưởng

---

## 📌 Vấn đề cốt lõi
Mọi doanh nghiệp đều đang lãng phí một "mỏ vàng" vô giá: **95% nhân sự không thuộc bộ phận Sales**. Họ sở hữu mạng lưới quan hệ thực, sự tin tưởng cao và hiểu sâu sản phẩm, nhưng tiềm năng này bị "đóng băng" hoàn toàn vì nhân viên thiếu công cụ, không biết bắt đầu từ đâu và thiếu động lực hành động. 

---

## 💡 Giải pháp đột phá
**BizGro** là nền tảng AI Agent tiên phong phá vỡ rào cản phòng ban để biến 100% nhân sự thành lực lượng tăng trưởng tổng lực nhờ 4 trụ cột:

* **🚀 BIZ-SHARE:** AI tự động hóa việc sáng tạo và cá nhân hóa nội dung chia sẻ sản phẩm trong vài giây.
* **🤝 BIZ-CONNECT:** Số hóa và đo lường mạng lưới quan hệ cá nhân thành nguồn khách hàng tiềm năng chất lượng.
* **💡 BIZ-COCREATE:** Biến ý tưởng thô của nhân viên thành đề xuất kinh doanh hoàn chỉnh nhờ AI thẩm định tự động.
* **🎯 Community & Teams Bot:** "AI Coach" thời gian thực, thúc đẩy hành động có tác động lớn nhất.

---

## 💎 Giá trị độc bản
Bằng cách kết hợp **AI Agent, Gamification và cơ chế BizCoins minh bạch**, BizGro thay đổi hoàn toàn cuộc chơi: chuyển dịch doanh nghiệp từ áp lực doanh thu đè nặng lên 5% phòng Sales sang **Mô hình Tăng trưởng Toàn diện**. 

Sản phẩm được lan tỏa tự nhiên, khách hàng đến từ nguồn lực uy tín nhất, và đổi mới sáng tạo diễn ra liên tục từ dòng máu nội bộ.

> 🔥 **Cốt lõi:** Với BizGro, tăng trưởng không còn là nhiệm vụ của một phòng ban — **Cả công ty là một động cơ tăng trưởng được vận hành bởi AI.**

---

## Kiến trúc hệ thống

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

- Chọn chiến dịch → chọn nền tảng (Facebook / LinkedIn / TikTok)
- AI sinh 3 biến thể bài viết: hài hước · chuyên nghiệp · tâm sự
- Mã affiliate cá nhân, track clicks & conversions
- **+10 BizCoins** khi chia sẻ

**Agent**: `ContentAgent` — LangGraph: `generate_posts → optimize_post`

### 2. BIZ-CONNECT — AI Referral Matchmaker

- Nhập danh sách contact → AI match với ICP (SME / Startup / Retail)
- Tạo Ice-breaker ngắn & Pitching Script đầy đủ
- Track trạng thái: Matched → Introduced → Closed
- **+200 BizCoins** khi giới thiệu thành công

**Agent**: `NetworkAgent` — LangGraph: `analyze_contacts → generate_scripts`

### 3. BIZ-COCREATE — AI Idea Incubator

- Gửi ý tưởng thô → AI **tăng cường** thành Business Proposal (400–500 từ)
- AI **phân tích thị trường**: TAM/SAM/SOM, dự phóng doanh thu 12 tháng
- AI **chấm điểm**: Khả thi · Chi phí · Tiềm năng (1–10), verdict APPROVED/REVIEWING/REJECTED
- **+500 BizCoins** khi ý tưởng được duyệt

**Agent**: `IdeaAgent` — LangGraph: `enhance_idea → analyze_market → evaluate_idea`

### 4. Community Chatbot — BizGro AI Assistant

- Chat trong ứng dụng, polling 10 giây, markdown rendering
- **Teams Outgoing Webhook** HMAC-verified, phản hồi trong 5 giây
- Context-aware: leaderboard, hot trends, campaigns, hướng dẫn kiếm BizCoins

**Agent**: `ChatAgent` — Direct LLM call với system prompt context-aware

### 5. Gamification Engine

- **BizCoins** + **Leaderboard** top 20 real-time
- **Badges**: Chiến thần Lan tỏa · Đại sứ Kết nối · Nhà phát minh...
- **BizStore**: Đổi quà thực tế — ngày phép, voucher, AirPods Pro...

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
| Container | Single Docker image — supervisord + nginx + uvicorn + Next.js |
| Deploy | GreenNode AgentBase Runtime |

---

## Deployment Architecture

```
Docker Container (port 8080 exposed)
├── supervisord
│   ├── nginx        :8080  — public entry point, reverse proxy
│   ├── uvicorn      :8000  — FastAPI backend (2 workers)
│   └── node         :3000  — Next.js frontend (standalone)
└── bizgro.db               — SQLite database
```

### GreenNode AgentBase Runtimes

| Runtime | URL |
|---------|-----|
| `clawathon-bizgo` (backend + frontend) | `https://endpoint-487619c8-18ad-448f-8267-268ddce4aae7.agentbase-runtime.aiplatform.vngcloud.vn` |
| `clawathon-bizgo-ui` (frontend only) | `https://endpoint-c807eb5c-098b-4a49-852a-3bc459004060.agentbase-runtime.aiplatform.vngcloud.vn` |

Container Registry: `vcr.vngcloud.vn/111480-abp111947`

---

## API Endpoints

```
POST   /auth/register  |  POST /auth/token  |  GET /auth/me

GET    /bizshare/campaigns
POST   /bizshare/generate-content       → ContentAgent (300s timeout)
POST   /bizshare/share  |  GET /bizshare/my-posts

POST   /bizconnect/match                → NetworkAgent
GET    /bizconnect/opportunities
PATCH  /bizconnect/opportunities/{id}

POST   /bizcocreate/ideas               → IdeaAgent (300s timeout)
GET    /bizcocreate/ideas  |  GET /bizcocreate/ideas/all

GET    /gamification/leaderboard  |  /my-stats  |  /store  |  /badges
POST   /gamification/redeem

GET    /community/feed
POST   /community/chat                  → ChatAgent
POST   /community/broadcast             → admin only

POST   /teams/webhook                   → HMAC-verified, ChatAgent

GET    /health  |  GET /docs
```

---

## Cài đặt & Chạy local

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Điền OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
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

## Microsoft Teams Integration

| Loại | Hướng | Mục đích |
|------|-------|---------|
| Incoming Webhook | BizGro → Teams | Thông báo leaderboard, broadcast, coin award |
| Outgoing Webhook | Teams → BizGro | Chatbot trong Teams channel |

**Callback URL cho Outgoing Webhook:**
```
https://endpoint-487619c8-18ad-448f-8267-268ddce4aae7.agentbase-runtime.aiplatform.vngcloud.vn/teams/webhook
```

---

## Environment Variables

| Variable | Mô tả |
|----------|-------|
| `OPENAI_API_KEY` | API key cho LLM |
| `OPENAI_BASE_URL` | LLM endpoint (GreenNode MAAS hoặc OpenAI) |
| `OPENAI_MODEL` | Model ID, VD: `google/gemma-4-31b-it` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./bizgro.db` |
| `SECRET_KEY` | JWT signing key |
| `TEAMS_INCOMING_WEBHOOK_URL` | URL Incoming Webhook của Teams channel |
| `TEAMS_WEBHOOK_SECRET` | HMAC secret cho Outgoing Webhook |
