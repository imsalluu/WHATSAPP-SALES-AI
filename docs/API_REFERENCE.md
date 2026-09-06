# REST API Reference

All endpoints are versioned under `/api/v1/` and require standard JWT Bearer Authorization header (`Authorization: Bearer <token>`), except public authentication and WhatsApp webhook verification endpoints.

---

## 1. Authentication (`/api/v1/auth`)

- `POST /register`: Register a new organization owner and organization workspace.
- `POST /login`: OAuth2 password form / JSON login returning `access_token` and `refresh_token`.
- `POST /refresh`: Refresh expired access token.
- `GET /me`: Get authenticated user profile and active organization memberships.

---

## 2. Organization & Team (`/api/v1/organizations`)

- `GET /current`: Active organization profile and limits.
- `PATCH /current`: Update company name, currency, timezone, settings.
- `GET /members`: List organization team members and assigned roles.
- `POST /invite`: Invite a teammate (`ADMIN`, `AGENT`, `VIEWER`).

---

## 3. Products & Catalog (`/api/v1/products`)

- `GET /`: List and filter products (supports keyword search, category, stock filters).
- `POST /`: Create a new product with variants and initial stock.
- `GET /{product_id}`: Retrieve detailed product info with variants.
- `PUT /{product_id}`: Update product information.
- `DELETE /{product_id}`: Soft delete product.
- `POST /{product_id}/variants`: Add a new variant (color, size, price differential, stock).

---

## 4. Orders & Fulfillment (`/api/v1/orders`)

- `GET /`: List orders with filtering by status, customer, date range.
- `POST /`: Create manual or AI-assisted order.
- `GET /{order_id}`: Order details with itemized list and customer info.
- `PATCH /{order_id}/status`: Transition status (`PENDING` -> `CONFIRMED` -> `PROCESSING` -> `SHIPPED` -> `DELIVERED`).
- `POST /{order_id}/notify`: Send WhatsApp shipping notification / invoice.

---

## 5. Conversations & Inbox (`/api/v1/conversations`)

- `GET /`: List conversations with real-time status (`AI_ACTIVE`, `HUMAN_REQUIRED`, `HUMAN_ACTIVE`, `RESOLVED`).
- `GET /{conversation_id}`: Full message history, intent, cart state, and customer profile.
- `POST /{conversation_id}/takeover`: Human agent takes over; AI paused.
- `POST /{conversation_id}/release`: Release conversation back to AI.
- `POST /{conversation_id}/messages`: Human agent sends a live reply to customer.
- `POST /{conversation_id}/simulator`: Send simulated incoming customer message.

---

## 6. Leads & CRM (`/api/v1/leads`)

- `GET /`: List leads with score, intent, budget, and stage filters.
- `PATCH /{lead_id}`: Update lead status or assign sales rep.
- `GET /metrics`: Aggregate lead capture rates and pipeline values.

---

## 7. RAG Knowledge Base (`/api/v1/knowledge`)

- `GET /documents`: List uploaded knowledge documents.
- `POST /documents`: Upload policy, manual, or FAQ document (auto-chunked and embedded).
- `DELETE /documents/{doc_id}`: Remove document and vectorized chunks.
- `POST /search`: Test semantic retrieval with custom query.

---

## 8. AI Salesperson Configuration (`/api/v1/agent-config`)

- `GET /`: Fetch active agent persona, sales instructions, enabled tools.
- `PUT /`: Update agent rules, tone, business hours, and escalation criteria.
- `POST /test`: Sandbox playground to test prompt and tool execution.

---

## 9. WhatsApp Integration (`/api/v1/whatsapp`)

- `GET /webhook`: Meta Cloud API webhook verification challenge.
- `POST /webhook`: Inbound message and status update webhook (HMAC SHA-256 verified).
- `GET /account`: Account connection status and phone number details.
- `POST /connect`: Connect Meta WABA credentials and token.
- `POST /test-message`: Send outbound test message to any WhatsApp number.

---

## 10. Analytics (`/api/v1/analytics`)

- `GET /overview`: Executive KPIs (Conversations, Leads, Orders, Revenue, Conversion rate, AI actions).
- `GET /sales-funnel`: Buying stage conversion distribution.
- `GET /top-products`: Most frequently requested and purchased products.
- `GET /objections`: Top customer objections and AI resolution rates.
