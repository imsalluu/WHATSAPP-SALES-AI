# WhatsApp Cloud API Integration & Webhook Guide

## 1. Meta WhatsApp Cloud API Setup

### Step 1: Create Meta Developer App
1. Go to [developers.facebook.com](https://developers.facebook.com).
2. Create an App -> Type: **Business**.
3. Add the **WhatsApp** product to your app.

### Step 2: Configure Webhook
- **Webhook URL**: `https://your-domain.com/api/v1/whatsapp/webhook`
- **Verify Token**: Configured in your Organization WhatsApp Settings.
- **Webhook Fields Subscribed**: `messages`, `message_deliveries`, `message_reads`.

---

## 2. In-Dashboard Live Simulator

For rapid onboarding and developer testing, WhatsApp Sales AI includes an in-browser WhatsApp phone simulator. You can:
1. Simulate incoming customer inquiries in real time.
2. Watch tool calling executions as they happen.
3. Test order placement and human handoff toggling without incurring Meta messaging fees.
