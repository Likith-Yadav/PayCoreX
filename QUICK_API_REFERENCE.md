# PayCoreX API - Quick Reference

## 🔗 Base URL
```
https://api.buildforu.pw
```

---

## 1️⃣ Register Merchant (No Auth Required)
```bash
POST /v1/merchants/register
Content-Type: application/json

{
  "name": "Your Business",
  "email": "merchant@example.com"
}
```

**Response**: Returns `api_key` and `secret` - **SAVE THESE!**

---

## 2️⃣ Create Payment (Requires Auth)

### Request
```bash
POST /v1/payments/create
X-API-Key: your-api-key
X-Signature: hmac-signature
X-Timestamp: unix-timestamp
Content-Type: application/json

{
  "amount": 1000.00,
  "method": "wallet",
  "user_id": "user-123",
  "reference_id": "order-456"
}
```

### Payment Methods
- `wallet` - Wallet payment
- `tokenized` - Tokenized card
- `upi_intent` - UPI payment
- `crypto` - Cryptocurrency

---

## 3️⃣ Generate HMAC Signature

**Formula**: `HMAC-SHA256(secret, timestamp + request_body)`

### Python
```python
import hmac, hashlib, time, json

timestamp = str(int(time.time()))
body = json.dumps({"amount": 1000, "method": "wallet"})
payload = f"{timestamp}{body}"

signature = hmac.new(
    secret.encode(),
    payload.encode(),
    hashlib.sha256
).hexdigest()
```

### JavaScript
```javascript
const crypto = require('crypto');

const timestamp = Math.floor(Date.now() / 1000).toString();
const body = JSON.stringify({amount: 1000, method: 'wallet'});
const payload = `${timestamp}${body}`;

const signature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
```

---

## 4️⃣ Check Payment Status
```bash
GET /v1/payments/{payment_id}
X-API-Key: your-api-key
X-Signature: signature
X-Timestamp: timestamp
```

---

## 5️⃣ Create Refund
```bash
POST /v1/payments/refund
X-API-Key: your-api-key
X-Signature: signature
X-Timestamp: timestamp

{
  "payment_id": "payment-uuid",
  "amount": 500.00,  # Optional (omit for full refund)
  "reason": "Customer request"
}
```

---

## 6️⃣ Wallet Operations

### Create Wallet
```bash
POST /v1/wallet/create
Body: {"user_id": "user-123"}
```

### Top Up
```bash
POST /v1/wallet/topup
Body: {
  "user_id": "user-123",
  "amount": 5000.00
}
```

### Get Balance
```bash
GET /v1/wallet/balance?user_id=user-123
```

---

## 7️⃣ Webhooks

### Setup Endpoint
```bash
POST /v1/webhooks/provider
Body: {
  "url": "https://your-domain.com/webhook",
  "events": ["payment.success", "payment.failed"]
}
```

### Verify Webhook
Check `X-Webhook-Signature` header matches your calculated signature.

---

## 📋 Complete cURL Example

```bash
# 1. Register
curl -X POST https://api.buildforu.pw/v1/merchants/register \
  -H "Content-Type: application/json" \
  -d '{"name":"My Store","email":"merchant@example.com"}'

# 2. Create Payment (with auth)
API_KEY="your-api-key"
SECRET="your-secret"
TIMESTAMP=$(date +%s)
BODY='{"amount":1000,"method":"wallet","user_id":"user-123"}'
SIGNATURE=$(echo -n "${TIMESTAMP}${BODY}" | openssl dgst -sha256 -hmac "${SECRET}" | sed 's/^.* //')

curl -X POST https://api.buildforu.pw/v1/payments/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${API_KEY}" \
  -H "X-Signature: ${SIGNATURE}" \
  -H "X-Timestamp: ${TIMESTAMP}" \
  -d "${BODY}"
```

---

## 🎯 Integration Flow

1. **Register** → Get `api_key` & `secret`
2. **Generate Signature** → For each API call
3. **Create Payment** → Process transaction
4. **Receive Webhook** → Get payment status update
5. **Check Status** → Verify payment if needed

---

## ⚠️ Important

- ✅ Always use HTTPS
- ✅ Keep `secret` secure (never expose in client code)
- ✅ Verify webhook signatures
- ✅ Handle payment statuses: `pending`, `processing`, `success`, `failed`

---

**Full Documentation**: See `API_USAGE_GUIDE.md`

