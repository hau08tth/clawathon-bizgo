# BizGro — Business Growth from Within

> Every Employee a Growth Engine — Khi mỗi nhân viên là một động cơ tăng trưởng

---

## Mô tả ngắn (300 từ — dùng cho form nộp bài)

**Vấn đề:** Đội ngũ Sales tại các công ty fintech như Zalopay chỉ chiếm ~5% nhân sự, nhưng phải gánh toàn bộ mục tiêu tăng trưởng. 95% nhân viên còn lại — kỹ sư, designer, vận hành — có mạng lưới quan hệ rộng và hiểu sản phẩm sâu, nhưng không có công cụ hay động lực để biến điều đó thành doanh thu thực sự. Kết quả: nguồn lực tăng trưởng khổng lồ bị lãng phí mỗi ngày.

**Người dùng:** Toàn bộ nhân viên Zalopay — không chỉ Sales — đặc biệt là những người có mạng lưới quan hệ B2B hoặc ý tưởng cải tiến sản phẩm nhưng chưa có kênh để hành động.

**Giải pháp AI:** BizGro là nền tảng multi-agent biến mỗi nhân viên thành một "growth engine" thông qua 4 agent AI chuyên biệt:

- **ContentAgent (BIZ-SHARE):** Nhân viên chọn chiến dịch, AI tự động tạo 3 phiên bản bài viết được cá nhân hóa theo phong cách của từng người (hài hước / chuyên nghiệp / tâm sự) kèm mã affiliate để track chuyển đổi — từ 0 đến bài viết sẵn sàng đăng chỉ trong 30 giây.

- **NetworkAgent (BIZ-CONNECT):** Nhân viên nhập danh sách liên hệ, AI phân tích và match với ICP của Zalopay, tự động viết Ice-breaker và Pitching Script cá nhân hóa — biến mạng lưới quan hệ thành pipeline sales thực sự.

- **IdeaAgent (BIZ-COCREATE):** Nhân viên gửi ý tưởng thô bằng ngôn ngữ tự nhiên, AI qua 3 bước (tăng cường → phân tích thị trường → chấm điểm) tự động nâng thành Business Proposal hoàn chỉnh gửi lên Ban Giám Đốc.

- **ChatAgent (Community + Teams Bot):** Chatbot context-aware tích hợp ngay trong ứng dụng và Microsoft Teams — trả lời câu hỏi về điểm, trends, chiến dịch, phần thưởng theo thời gian thực.

**Giá trị mang lại:** Toàn bộ hành động được gamify với BizCoins — nhân viên kiếm điểm, leo bảng xếp hạng, đổi quà thực tế. BizGro không chỉ là công cụ AI — đây là hệ sinh thái tăng trưởng từ bên trong, nơi mỗi nhân viên đều có thể đóng góp vào doanh thu của công ty.

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
