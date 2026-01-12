# PayCoreX API Usage Guide

## 🌐 Base URL

**Production API**: `https://api.buildforu.pw`

---

## 📋 Step 1: Register as a Merchant

First, you need to register your business/application to get API credentials.

### Endpoint
```
POST https://api.buildforu.pw/v1/merchants/register
```

### Request Body
```json
{
  "name": "Your Business Name",
  "email": "your-email@example.com"
}
```

### Example (cURL)
```bash
curl -X POST https://api.buildforu.pw/v1/merchants/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My E-commerce Store",
    "email": "merchant@example.com"
  }'
```

### Response
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My E-commerce Store",
  "email": "merchant@example.com",
  "api_key": "your-api-key-here",
  "secret": "your-secret-key-here",
  "is_active": true,
  "created_at": "2026-01-12T05:30:00Z"
}
```

**⚠️ IMPORTANT**: Save your `api_key` and `secret` securely! You'll need them for all API requests.

---

## 🔐 Step 2: Understanding Authentication (HMAC)

All API requests (except registration) require HMAC signature authentication.

### Required Headers
- `X-API-Key`: Your API key
- `X-Signature`: HMAC-SHA256 signature
- `X-Timestamp`: Current Unix timestamp (seconds)

### How to Generate Signature

**Formula**: `HMAC-SHA256(secret, timestamp + request_body)`

**Example (Python)**:
```python
import hmac
import hashlib
import time
import json

def generate_signature(secret, timestamp, body):
    payload = f"{timestamp}{body}"
    signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

# Example usage
api_key = "your-api-key"
secret = "your-secret"
timestamp = str(int(time.time()))
body = json.dumps({"amount": 1000, "method": "wallet"})

signature = generate_signature(secret, timestamp, body)

headers = {
    "X-API-Key": api_key,
    "X-Signature": signature,
    "X-Timestamp": timestamp,
    "Content-Type": "application/json"
}
```

**Example (JavaScript/Node.js)**:
```javascript
const crypto = require('crypto');

function generateSignature(secret, timestamp, body) {
    const payload = `${timestamp}${body}`;
    return crypto
        .createHmac('sha256', secret)
        .update(payload)
        .digest('hex');
}

// Example usage
const apiKey = 'your-api-key';
const secret = 'your-secret';
const timestamp = Math.floor(Date.now() / 1000).toString();
const body = JSON.stringify({ amount: 1000, method: 'wallet' });

const signature = generateSignature(secret, timestamp, body);

const headers = {
    'X-API-Key': apiKey,
    'X-Signature': signature,
    'X-Timestamp': timestamp,
    'Content-Type': 'application/json'
};
```

---

## 💳 Step 3: Create a Payment

Once you have your API credentials, you can start processing payments.

### Endpoint
```
POST https://api.buildforu.pw/v1/payments/create
```

### Request Body
```json
{
  "amount": 1000.00,
  "currency": "INR",
  "method": "wallet",
  "user_id": "user-123",
  "reference_id": "order-456",
  "metadata": {
    "order_id": "ORD-12345",
    "description": "Product purchase"
  }
}
```

### Payment Methods Available

- `wallet` - Wallet payment (requires user to have wallet balance)
- `tokenized` - Tokenized card payment (requires stored payment token)
- `upi_intent` - UPI payment intent
- `crypto` - Cryptocurrency payment (Ethereum, Polygon, BSC)

### Example (cURL with Authentication)
```bash
# Set your credentials
API_KEY="your-api-key"
SECRET="your-secret"
TIMESTAMP=$(date +%s)
BODY='{"amount":1000,"method":"wallet","user_id":"user-123"}'

# Generate signature
SIGNATURE=$(echo -n "${TIMESTAMP}${BODY}" | openssl dgst -sha256 -hmac "${SECRET}" | sed 's/^.* //')

# Make request
curl -X POST https://api.buildforu.pw/v1/payments/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${API_KEY}" \
  -H "X-Signature: ${SIGNATURE}" \
  -H "X-Timestamp: ${TIMESTAMP}" \
  -d "${BODY}"
```

### Response (Success)
```json
{
  "id": "payment-uuid-here",
  "merchant_id": "merchant-uuid",
  "amount": "1000.00",
  "currency": "INR",
  "status": "success",
  "method": "wallet",
  "user_id": "user-123",
  "reference_id": "order-456",
  "provider_reference": "provider-txn-id",
  "metadata": {
    "order_id": "ORD-12345",
    "description": "Product purchase"
  },
  "failure_reason": null,
  "created_at": "2026-01-12T05:30:00Z",
  "updated_at": "2026-01-12T05:30:01Z"
}
```

### Response (Failed)
```json
{
  "id": "payment-uuid-here",
  "status": "failed",
  "failure_reason": "Insufficient wallet balance",
  ...
}
```

---

## 📊 Step 4: Check Payment Status

### Endpoint
```
GET https://api.buildforu.pw/v1/payments/{payment_id}
```

### Example
```bash
curl -X GET https://api.buildforu.pw/v1/payments/payment-uuid-here \
  -H "X-API-Key: ${API_KEY}" \
  -H "X-Signature: ${SIGNATURE}" \
  -H "X-Timestamp: ${TIMESTAMP}"
```

---

## 🔄 Step 5: Process Refunds

### Endpoint
```
POST https://api.buildforu.pw/v1/payments/refund
```

### Request Body
```json
{
  "payment_id": "payment-uuid-here",
  "amount": 500.00,
  "reason": "Customer requested refund"
}
```

**Note**: Omit `amount` for full refund, include it for partial refund.

---

## 💰 Wallet System

### Create Wallet
```
POST https://api.buildforu.pw/v1/wallet/create
Body: {"user_id": "user-123"}
```

### Top Up Wallet
```
POST https://api.buildforu.pw/v1/wallet/topup
Body: {
  "user_id": "user-123",
  "amount": 5000.00,
  "currency": "INR"
}
```

### Get Balance
```
GET https://api.buildforu.pw/v1/wallet/balance?user_id=user-123
```

---

## 🔔 Webhooks

PayCoreX automatically sends webhooks for payment events.

### Setup Webhook Endpoint
```
POST https://api.buildforu.pw/v1/webhooks/provider
Body: {
  "url": "https://your-domain.com/webhook",
  "events": ["payment.success", "payment.failed", "refund.success"]
}
```

### Webhook Payload Example
```json
{
  "event": "payment.success",
  "timestamp": "2026-01-12T05:30:00Z",
  "data": {
    "payment_id": "payment-uuid",
    "amount": "1000.00",
    "status": "success",
    "method": "wallet"
  }
}
```

**Webhook Signature**: Verify using `X-Webhook-Signature` header.

---

## 📈 Dashboard & Analytics

### Get Statistics
```
GET https://api.buildforu.pw/v1/dashboard/stats
```

### Get Payments List
```
GET https://api.buildforu.pw/v1/dashboard/payments?status=success&limit=50
```

### Get Ledger Entries
```
GET https://api.buildforu.pw/v1/dashboard/ledgers
```

---

## 🚀 Complete Integration Example (Python)

```python
import requests
import hmac
import hashlib
import time
import json

class PayCoreXClient:
    def __init__(self, api_key, secret, base_url="https://api.buildforu.pw"):
        self.api_key = api_key
        self.secret = secret
        self.base_url = base_url
    
    def _generate_signature(self, timestamp, body):
        payload = f"{timestamp}{body}"
        return hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _get_headers(self, body):
        timestamp = str(int(time.time()))
        signature = self._generate_signature(timestamp, body)
        return {
            "X-API-Key": self.api_key,
            "X-Signature": signature,
            "X-Timestamp": timestamp,
            "Content-Type": "application/json"
        }
    
    def create_payment(self, amount, method, user_id=None, reference_id=None):
        url = f"{self.base_url}/v1/payments/create"
        body = json.dumps({
            "amount": amount,
            "method": method,
            "user_id": user_id,
            "reference_id": reference_id
        })
        
        response = requests.post(
            url,
            data=body,
            headers=self._get_headers(body)
        )
        return response.json()
    
    def get_payment(self, payment_id):
        url = f"{self.base_url}/v1/payments/{payment_id}"
        body = ""
        
        response = requests.get(
            url,
            headers=self._get_headers(body)
        )
        return response.json()

# Usage
client = PayCoreXClient(
    api_key="your-api-key",
    secret="your-secret"
)

# Create payment
payment = client.create_payment(
    amount=1000.00,
    method="wallet",
    user_id="user-123",
    reference_id="order-456"
)

print(f"Payment Status: {payment['status']}")
print(f"Payment ID: {payment['id']}")
```

---

## 🎯 Quick Start Checklist

1. ✅ Register merchant → Get `api_key` and `secret`
2. ✅ Save credentials securely
3. ✅ Implement HMAC signature generation
4. ✅ Create your first payment
5. ✅ Set up webhook endpoint to receive notifications
6. ✅ Test payment flow end-to-end
7. ✅ Integrate into your application

---

## 📞 Support

- **API Base URL**: `https://api.buildforu.pw`
- **Documentation**: See `ARCHITECTURE.md` for detailed system architecture
- **Health Check**: `GET https://api.buildforu.pw/` (no auth required)

---

## ⚠️ Important Notes

1. **Keep your secret secure** - Never expose it in client-side code
2. **Use HTTPS** - All API calls must use HTTPS
3. **Handle webhooks** - Implement webhook verification in your endpoint
4. **Test in staging** - Test thoroughly before going live
5. **Monitor payments** - Use dashboard APIs to monitor transaction status

---

**Happy integrating! 🚀**

