# BizGro — Business Growth from Within

> Every Employee a Growth Engine — Khi mỗi nhân viên là một động cơ tăng trưởng

---

## Mô tả ngắn (dùng cho form nộp bài)

Một công ty 5.000 nhân viên đang ngồi trên một mỏ vàng tăng trưởng — và không biết.

95% nhân viên không thuộc Sales nhưng có thứ mà Sales phải mất hàng tháng mới xây dựng được: mạng lưới quan hệ thực, sự tin tưởng từ bạn bè và đối tác, cùng sự hiểu biết sâu về sản phẩm. Vấn đề không phải họ không muốn đóng góp — mà là **không biết bắt đầu từ đâu, không có công cụ, và không có lý do đủ mạnh để hành động**.

**BizGro** giải quyết cả ba rào cản đó bằng kiến trúc **4 AI agent chuyên biệt**, chạy trên nền tảng GreenNode AgentBase:

**BIZ-SHARE** — Nhân viên chọn chiến dịch, nhấn một nút. Trong vòng 30 giây, **ContentAgent** tạo ra 3 bài viết được cá nhân hóa theo phong cách riêng của họ (hài hước / chuyên nghiệp / chân thật), kèm mã affiliate để track từng chuyển đổi. Từ "tôi không biết viết gì" đến bài đăng sẵn sàng — 30 giây.

**BIZ-CONNECT** — Nhân viên paste danh sách liên hệ. **NetworkAgent** phân tích từng người, match với ICP của Zalopay, rồi tự động viết Ice-breaker và Pitching Script cá nhân hóa cho từng contact. Mạng lưới quan hệ cá nhân trở thành pipeline sales có thể đo được.

**BIZ-COCREATE** — Nhân viên viết ý tưởng thô bằng ngôn ngữ tự nhiên. **IdeaAgent** chạy 3 LLM call tuần tự: tăng cường thành Business Proposal hoàn chỉnh → phân tích TAM/SAM/SOM và dự phóng doanh thu → chấm điểm khả thi/chi phí/tiềm năng. Ý tưởng "nháp trên giấy" thành hồ sơ trình Ban Giám Đốc — tự động.

**Community & Teams Bot** — **ChatAgent** tích hợp ngay trong Microsoft Teams và ứng dụng, trả lời mọi câu hỏi về điểm thưởng, xu hướng, chiến dịch với context real-time từ leaderboard và hệ thống.

Toàn bộ được gamify: BizCoins, bảng xếp hạng, huy hiệu, và BizStore đổi quà thực tế. Nhưng quan trọng hơn — **BizGro thay đổi hành vi**. Khi mỗi nhân viên đều có thể tạo content, kết nối khách hàng, và đề xuất ý tưởng chỉ trong vài phút, tăng trưởng không còn là bài toán của riêng Sales nữa. Đó là bài toán của cả công ty — và AI đang giải nó từng ngày.

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
