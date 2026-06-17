# 🚀 BizGro — Biến Mọi Nhân Viên Thành Động Cơ Tăng Trưởng

> Every Employee a Growth Engine — Khi mỗi nhân viên là một động cơ tăng trưởng

---

## 📌 Vấn đề
Mỗi doanh nghiệp đang ngồi trên một mỏ vàng tăng trưởng nhưng chưa được khai thác.

**95% nhân viên không thuộc bộ phận Sales**, nhưng họ lại sở hữu những tài sản quý giá nhất: 
* Mạng lưới quan hệ thực tế.
* Sự tin tưởng cá nhân từ bạn bè, đối tác.
* Hiểu biết sâu sắc về sản phẩm.
* Những ý tưởng sáng tạo có thể tạo ra giá trị mới.

Tuy nhiên, phần lớn tiềm năng này đang bị bỏ ngỏ vì nhân viên thường **không biết bắt đầu từ đâu, thiếu công cụ hỗ trợ và thiếu động lực** để tham gia vào quá trình tăng trưởng chung.

---

## 💡 Giải pháp
**BizGro** là nền tảng AI Agent được xây dựng trên **GreenNode AgentBase**, giúp mọi nhân viên trong doanh nghiệp đều có thể đóng góp trực tiếp và dễ dàng vào sự tăng trưởng của công ty thông qua 4 tính năng lõi:

### 🚀 BIZ-SHARE
> Tạo nội dung cá nhân hóa và chia sẻ sản phẩm chỉ trong vài giây bằng AI.

### 🤝 BIZ-CONNECT
> Biến mạng lưới quan hệ cá nhân thành nguồn khách hàng tiềm năng (Leads) có thể theo dõi và đo lường được.

### 💡 BIZ-COCREATE
> Chuyển các ý tưởng thô thành đề xuất kinh doanh hoàn chỉnh nhờ hệ thống phân tích và đánh giá tự động.

### 🎯 Community & Teams Bot
> AI Coach hoạt động theo thời gian thực (real-time), gợi ý chính xác cho nhân viên biết hành động nào sẽ tạo ra tác động lớn nhất.

---

## 💎 Giá trị mang lại

BizGro loại bỏ hoàn toàn rào cản giữa nhân viên và sự tăng trưởng của doanh nghiệp bằng cách kết hợp:
`AI` + `Gamification (Trò chơi hóa)` + `BizCoins` + `Hệ thống ghi nhận minh bạch`

| Mô hình truyền thống | Mô hình tăng trưởng cùng BizGro |
| :--- | :--- |
| Gánh nặng doanh thu đè nặng lên 5% nhân sự thuộc phòng Sales. | Kích hoạt sức mạnh tổng lực của **100% bộ phận** trong tổ chức. |
| Tiềm năng truyền thông và quan hệ của nhân viên bị lãng quên. | Lan tỏa sản phẩm, tìm kiếm khách hàng và đột phá ý tưởng tự động. |

> **Cốt lõi:** Tăng trưởng không còn là nhiệm vụ của riêng một phòng ban. Với BizGro, cả công ty trở thành một đội ngũ tăng trưởng đồng nhất được vận hành và tối ưu bởi AI.

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
