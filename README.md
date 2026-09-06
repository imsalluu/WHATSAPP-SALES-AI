# 🛍️ WHATSAPP SALES AI

> **Production-grade B2B Multi-Tenant SaaS Platform for Autonomous AI-Powered WhatsApp Sales Agents.**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.111-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2016%20App%20Router-black.svg?logo=next.js&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2016%20%2B%20pgvector-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![WhatsApp Cloud API](https://img.shields.io/badge/Meta-WhatsApp%20Cloud%20API%20v20.0-25D366.svg?logo=whatsapp&logoColor=white)](https://developers.facebook.com)
[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Deployment-Docker%20Compose-2496ED.svg?logo=docker&logoColor=white)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-Pytest%20100%25%20Passed-brightgreen.svg?logo=pytest&logoColor=white)](backend/tests/)

---

## 🌟 Executive Overview

**WhatsApp Sales AI** is not a simple question-and-answer chatbot. It is a full-fledged **digital salesperson** engineered for e-commerce and retail brands to autonomously conduct conversational sales, check live inventory, provide budget-tailored recommendations, overcome objections, calculate delivery fees, capture qualified CRM leads, fulfill verified orders, and escalate smoothly to human agents.

```
WhatsApp Customer Message
        │
        ▼
Meta WhatsApp Cloud API (Webhook)
        │  (HMAC SHA-256 Verified)
        ▼
FastAPI Gateway & Memory Compactor
        │
        ▼
LangGraph AI Sales Agent Engine
   ├── RAG Knowledge Base (pgvector)
   └── 12 Business Database Tools
        │
        ▼
Anti-Hallucination Guardrail & Validator
        │
        ▼
WhatsApp Markdown Formatted Response + Order Creation
```

---

## ✨ Key Capabilities

- **🛡️ Zero Hallucinations**: Strictly grounded facts. The AI never invents pricing, inventory stock, delivery times, or store policies. If information is needed, it calls database tools.
- **⚡ 12 Autonomous Sales Tools**: Direct atomic database operations for product discovery, live stock verification, shipping calculation, order creation, lead capture, and human escalation.
- **📚 RAG Knowledge Base (`pgvector`)**: Upload store policies, return terms, and FAQs. Hybrid search combines dense vector embeddings with full-text keyword matching.
- **📱 Dual-Pane WhatsApp Inbox with Takeover**: Real-time customer chat stream, human takeover toggle (`AI_ACTIVE` ↔ `HUMAN_ACTIVE`), customer CRM panel, and order drawer.
- **🧪 In-Browser WhatsApp Phone Simulator**: Zero-cost interactive mobile sandbox directly inside the dashboard to test customer journeys and tool executions in real time.
- **🏢 Multi-Tenant SaaS Isolation**: Every transaction, product, customer, and conversation is strictly isolated by `organization_id`.
- **📊 Sales Intelligence & Funnel Analytics**: Tracks buying stages (`AWARENESS` → `CONSIDERATION` → `DECISION` → `RETENTION`), customer objections, and lead scores (0–100).
- **🌐 Bilingual Support**: Natural, culturally aligned conversations in both English and Bengali / Banglish.

---

## 🛠️ 12 Core Business Sales Tools

| Tool Name | Parameters | Description |
|---|---|---|
| `search_products` | `query, category, min_price, max_price, limit` | Catalog keyword, category, and budget matching. |
| `get_product` | `product_id_or_sku` | Fetches specs, attributes, and image gallery. |
| `check_inventory` | `product_id_or_sku, size, color` | Live stock check for exact product variants. |
| `get_product_variants` | `product_id` | Lists all available sizes, colors, and pricing differentials. |
| `get_order` | `order_number_or_id, customer_phone` | Fetches live fulfillment and delivery tracking status. |
| `create_order` | `customer_name, customer_phone, delivery_address, items, payment_method` | Places confirmed order into DB & updates inventory. |
| `update_order` | `order_id, status, notes` | Modifies order state or notes. |
| `calculate_shipping` | `city, delivery_address, item_count` | Computes delivery fee (Dhaka: ৳60 / Outside: ৳120). |
| `get_shipping_status` | `order_id_or_tracking` | Live courier tracking details. |
| `capture_lead` | `name, phone, intent, interested_products, budget, location, lead_score` | Enrolls CRM lead with buying intent score (0-100). |
| `create_support_ticket` | `customer_phone, subject, issue_description, priority` | Logs escalated customer service tickets. |
| `transfer_to_human` | `reason, conversation_id, department` | Transitions conversation status to `HUMAN_REQUIRED`. |

---

## 📂 Repository Structure

```
├── backend/
│   ├── app/
│   │   ├── agents/          # LangGraph Sales Agent & Intent Analyzer
│   │   ├── api/v1/          # REST endpoints (auth, products, orders, conversations, leads, etc.)
│   │   ├── core/            # Config, async DB engine, security, JWT, RBAC
│   │   ├── integrations/    # WhatsApp Meta Cloud API provider & live simulator
│   │   ├── models/          # SQLAlchemy 2.0 multi-tenant declarative models
│   │   ├── rag/             # Chunking, embeddings & pgvector hybrid retrieval
│   │   ├── schemas/         # Pydantic v2 schemas & ConfigDict validation
│   │   ├── tools/           # 12 Autonomous Sales Tools & JSON definitions
│   │   └── main.py          # FastAPI application entrypoint & lifespan
│   ├── tests/               # Pytest suite (Auth, Tools, Simulator, RAG)
│   ├── Dockerfile           # Backend container
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app/                 # Next.js 16 App Router pages
│   │   ├── agent/           # AI Salesperson personality & tool configurator
│   │   ├── analytics/       # Sales funnels & objection breakdown
│   │   ├── conversations/   # WhatsApp dual-pane inbox & live chat
│   │   ├── dashboard/       # Executive SaaS metrics & KPI overview
│   │   ├── knowledge/       # RAG document uploader & vector tester
│   │   ├── leads/           # CRM lead pipeline & scoring table
│   │   ├── login/ & register/ # SaaS authentication & org onboarding
│   │   ├── orders/          # Fulfillment pipeline & tracking manager
│   │   ├── products/        # Product catalog & stock variant manager
│   │   ├── settings/        # Organization profile, team RBAC, plans
│   │   └── whatsapp/        # Meta Cloud API credentials & webhook status
│   ├── components/          # Sidebar, Header, WhatsApp Simulator Modal
│   ├── lib/                 # Typed API client & Auth context
│   └── Dockerfile           # Next.js standalone container
├── docs/                    # Complete architectural and setup documentation
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── DATABASE_SCHEMA.md
│   ├── AI_AGENT_AND_TOOLS.md
│   ├── RAG_AND_KNOWLEDGE_BASE.md
│   ├── WHATSAPP_INTEGRATION_GUIDE.md
│   └── DEPLOYMENT_AND_DOCKER.md
├── docker-compose.yml       # PostgreSQL + pgvector, Redis, Backend, Frontend
└── pytest.ini               # Pytest configuration
```

---

## 🚀 Quickstart Guide

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/imsalluu/WHATSAPP-SALES-AI.git
cd WHATSAPP-SALES-AI

# 2. Copy environment template
cp .env.example .env

# 3. Spin up all multi-tenant services
docker compose up --build -d
```

- **Frontend Dashboard**: `http://localhost:3000`
- **FastAPI API & Swagger Docs**: `http://localhost:8000/api/v1/docs`

---

### Option 2: Local Development Setup

#### Backend:
```bash
# 1. Navigate and install dependencies
python -m pip install -r backend/requirements.txt

# 2. Run backend server
uvicorn app.main:app --app-dir backend --reload --port 8000
```

#### Frontend:
```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies & run dev server
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🧪 Automated Testing Suite

WhatsApp Sales AI includes a comprehensive test suite covering multi-tenancy, authentication, all 12 tools, RAG vector ingestion, and end-to-end conversation simulation:

```bash
python -m pytest backend/tests/ -v
```

```text
============================= test session starts =============================
backend/tests/test_agent.py::test_sales_simulator_flow PASSED            [ 25%]
backend/tests/test_auth.py::test_register_and_login PASSED               [ 50%]
backend/tests/test_rag.py::test_rag_knowledge_pipeline PASSED            [ 75%]
backend/tests/test_tools.py::test_all_sales_tools PASSED                 [100%]
======================= 4 passed in 1.45s ========================
```

---

## 📖 Detailed Documentation

| Document | Purpose |
|---|---|
| [**Architecture Overview**](docs/ARCHITECTURE.md) | High-level system design, data flows, and state machines. |
| [**WhatsApp Integration Guide**](docs/WHATSAPP_INTEGRATION_GUIDE.md) | Meta Cloud API setup, permanent system token, and webhooks. |
| [**REST API Reference**](docs/API_REFERENCE.md) | OpenAPI specification and endpoint documentation. |
| [**Database Schema & ERD**](docs/DATABASE_SCHEMA.md) | Multi-tenant schema, relationships, and pgvector. |
| [**AI Agent & 12 Tools**](docs/AI_AGENT_AND_TOOLS.md) | LangGraph agent loop, system prompts, and tool parameters. |
| [**RAG & Knowledge Base**](docs/RAG_AND_KNOWLEDGE_BASE.md) | Chunking algorithms, embeddings, and hybrid search. |
| [**Deployment & Docker**](docs/DEPLOYMENT_AND_DOCKER.md) | Production Docker Compose and container orchestration. |

---

## 📜 License & Support

Distributed under the **MIT License**. Built for high-growth e-commerce brands and commercial SaaS deployments.
