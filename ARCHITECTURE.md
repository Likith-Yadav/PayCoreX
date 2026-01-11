# PayCoreX Architecture & How It Works

## 🏗️ System Overview

PayCoreX is an enterprise-grade Payment Orchestration Platform that routes payments through multiple methods (UPI, Wallet, Tokenized Cards, Crypto) while maintaining a unified ledger and providing webhook notifications.

---

## 📦 Core Components

### 1. **Merchant System** (`merchants/`)
**Purpose**: Manages merchant accounts and API authentication

**How it works**:
- Merchants register via `/v1/merchants/register`
- System generates unique `api_key` and `secret` for each merchant
- These credentials are used for HMAC signature authentication on all API requests
- Merchants can regenerate keys via `/v1/merchants/apikey`

**Database**: `merchants` table stores merchant info and credentials

---

### 2. **Security Layer** (`security/middleware.py`)
**Purpose**: HMAC signature verification for every API request

**How it works**:
1. Client sends request with headers:
   - `X-API-Key`: Merchant's API key
   - `X-Signature`: HMAC-SHA256 signature
   - `X-Timestamp`: Current timestamp
2. Middleware intercepts request (except exempt paths)
3. Retrieves merchant's secret using API key
4. Reconstructs signature: `HMAC-SHA256(secret, timestamp + request_body)`
5. Compares signatures using `hmac.compare_digest()` (timing-safe)
6. If valid, attaches `merchant` object to request
7. If invalid, returns 401 Unauthorized

**Exempt paths**: `/v1/merchants/register`, `/admin/`, `/`, `/favicon.ico`

---

### 3. **Payment Orchestration** (`payments/`)
**Purpose**: Routes payments to appropriate payment method handlers

**How it works**:

```
POST /v1/payments/create
  ↓
PaymentOrchestrator.create_payment()
  ↓
Creates Payment record (status: 'pending')
  ↓
PaymentOrchestrator.process_payment()
  ↓
Routes based on method:
  ├─ 'wallet' → WalletService.pay_from_wallet()
  ├─ 'tokenized' → TokenService.process_payment()
  ├─ 'upi_intent' → UPI handler (returns payment link)
  └─ 'crypto' → CryptoService.create_payment_address()
  ↓
If successful:
  ├─ Update Payment status to 'success'
  ├─ Update Ledger (credit merchant account)
  └─ Send webhook to merchant
```

**Payment States**: `pending` → `processing` → `success`/`failed`

**Database**: `payments` table tracks all transactions

---

### 4. **Ledger System** (`ledger/`)
**Purpose**: Immutable double-entry accounting system

**How it works**:
- Every financial transaction creates a ledger entry
- Each entry has: `credit`, `debit`, `balance`
- Balance is calculated: `previous_balance + credit - debit`
- Ledger entries are **immutable** (never updated, only appended)
- Supports multiple entities: `merchant`, `wallet`, `user`

**Example Flow**:
```
Payment of ₹1000 received:
  Ledger Entry:
    entity: 'merchant'
    entity_id: <merchant_uuid>
    credit: 1000
    debit: 0
    balance: 1000 (previous: 0)
    reference_type: 'payment'
    reference_id: <payment_uuid>
```

**Use Cases**:
- Track merchant balance
- Track wallet balance
- Audit trail for all transactions
- Reconciliation

**Database**: `ledgers` table with indexes on `(entity, entity_id)`

---

### 5. **Wallet System** (`wallet/`)
**Purpose**: Internal wallet for users to store and spend funds

**How it works**:

**Create Wallet**:
```
POST /v1/wallet/create
  → Creates Wallet record (balance: 0)
```

**Top Up**:
```
POST /v1/wallet/topup
  → Increases wallet.balance
  → Creates ledger entry (credit)
```

**Pay from Wallet**:
```
POST /v1/wallet/pay
  → Checks: wallet.balance >= amount
  → Decreases wallet.balance
  → Creates ledger entry (debit)
  → Returns updated balance
```

**Refund to Wallet**:
```
→ Increases wallet.balance
→ Creates ledger entry (credit)
```

**Database**: `wallets` table with unique constraint on `(user_id, merchant_id)`

---

### 6. **Token Vault** (`tokens/`)
**Purpose**: Securely store payment tokens (cards, bank accounts, UPI)

**How it works**:
- Tokens are encrypted using Fernet (symmetric encryption)
- Encryption key stored in `TOKEN_ENCRYPTION_KEY` env variable
- Token hash stored for duplicate detection
- Only last 4 digits stored in plaintext (for display)
- Tokens can be deleted (soft delete: `is_active = False`)

**Security**:
- Encryption: AES-128 in CBC mode (via Fernet)
- Hashing: SHA-256 for duplicate detection
- Never returns full token value in API responses

**Database**: `tokens` table with encrypted storage

---

### 7. **Webhook Engine** (`webhooks/`)
**Purpose**: Deliver event notifications to merchant endpoints

**How it works**:

**Setup**:
```
POST /v1/webhooks/provider
  → Merchant registers webhook URL
  → System generates webhook secret
  → Stores endpoint configuration
```

**Delivery**:
```
Payment succeeds
  ↓
WebhookService.send_payment_webhook()
  ↓
For each active endpoint:
  ├─ Create payload: {event, data}
  ├─ Generate signature: HMAC-SHA256(secret, payload)
  ├─ POST to merchant URL with headers:
  │   ├─ X-Webhook-Signature
  │   └─ X-Webhook-Event
  ├─ Store delivery attempt in webhook_deliveries
  └─ If failed → Schedule retry (exponential backoff)
```

**Retry Logic**:
- Max 3 retries
- Exponential backoff: 2^retry_count minutes
- Status: `pending` → `retrying` → `sent`/`failed`

**Database**: 
- `webhook_endpoints`: Merchant webhook configurations
- `webhook_deliveries`: Delivery logs and retry tracking

---

### 8. **Crypto Integration** (`crypto/`)
**Purpose**: Monitor blockchain transactions for crypto payments

**How it works**:

**Register Address**:
```
POST /v1/crypto/address
  → Stores user's crypto wallet address
  → Network: ethereum, polygon, bsc
```

**Transaction Monitoring**:
```
Celery task: monitor_crypto_transactions()
  ↓
For each registered address:
  ├─ Query blockchain (via Web3.py)
  ├─ Check last 100 blocks
  ├─ Detect incoming transactions
  ├─ Verify transaction status
  └─ Update crypto_transactions table
```

**Status Check**:
```
GET /v1/crypto/status/{tx_hash}
  → Query blockchain for transaction
  → Return: status, confirmations, block_number
```

**Supported Networks**: Ethereum, Polygon, BSC

**Database**: 
- `crypto_addresses`: User wallet addresses
- `crypto_transactions`: Blockchain transaction records

---

### 9. **Refund System** (`payments/`)
**Purpose**: Process full and partial refunds

**How it works**:
```
POST /v1/payments/refund
  ↓
RefundService.create_refund()
  ↓
Validations:
  ├─ Payment exists and is successful
  ├─ Refund amount <= payment amount
  ├─ Total refunds <= payment amount
  ↓
Create Refund record
  ↓
Process refund:
  ├─ If wallet payment → Refund to wallet
  ├─ If tokenized → Process via payment gateway
  └─ Update ledger (debit merchant account)
  ↓
Send webhook notification
```

**Database**: `refunds` table linked to `payments`

---

### 10. **Dashboard APIs** (`dashboard/`)
**Purpose**: Analytics and reporting for merchants

**Endpoints**:
- `GET /v1/dashboard/stats`: Total volume, success rate, refunds
- `GET /v1/dashboard/payments`: Filtered payment list
- `GET /v1/dashboard/ledgers`: Ledger history

---

## 🔄 Complete Payment Flow Example

### Scenario: User pays ₹1000 via Wallet

```
1. Client Request:
   POST /v1/payments/create
   Headers: X-API-Key, X-Signature, X-Timestamp
   Body: {
     "amount": 1000,
     "method": "wallet",
     "user_id": "user-123"
   }

2. Security Middleware:
   ✓ Validates HMAC signature
   ✓ Attaches merchant to request

3. Payment Orchestration:
   ✓ Creates Payment record (id: pay-456, status: 'pending')
   ✓ Routes to WalletService

4. Wallet Processing:
   ✓ Checks wallet balance >= 1000
   ✓ Deducts 1000 from wallet
   ✓ Updates wallet.balance: 5000 → 4000

5. Ledger Update:
   ✓ Creates ledger entry:
     - entity: 'wallet'
     - entity_id: wallet-789
     - debit: 1000
     - balance: 4000

6. Merchant Ledger:
   ✓ Creates ledger entry:
     - entity: 'merchant'
     - entity_id: merchant-123
     - credit: 1000
     - balance: 1000

7. Payment Update:
   ✓ Updates Payment status: 'success'
   ✓ Stores provider_reference

8. Webhook Delivery:
   ✓ Sends POST to merchant webhook URL
   ✓ Payload: {event: 'payment.success', data: {...}}
   ✓ Stores delivery log

9. Response:
   ✓ Returns Payment details to client
```

---

## 🗄️ Database Schema

### Key Tables:
- **merchants**: Merchant accounts and API keys
- **payments**: Payment transactions
- **refunds**: Refund records
- **wallets**: User wallet balances
- **ledgers**: Immutable accounting entries
- **tokens**: Encrypted payment tokens
- **crypto_addresses**: Crypto wallet addresses
- **crypto_transactions**: Blockchain transactions
- **webhook_endpoints**: Webhook configurations
- **webhook_deliveries**: Webhook delivery logs

---

## 🔐 Security Features

1. **HMAC Authentication**: Every request signed with merchant secret
2. **Token Encryption**: Payment tokens encrypted with Fernet
3. **Immutable Ledger**: Financial records cannot be modified
4. **Webhook Signatures**: Webhooks signed for verification
5. **Timing-Safe Comparison**: Prevents timing attacks

---

## 🚀 Scalability Features

1. **Domain Separation**: Each app is independent (microservice-ready)
2. **Redis Caching**: Fast lookups for merchant credentials
3. **Celery Tasks**: Background processing for webhooks and crypto
4. **Database Indexes**: Optimized queries on frequently accessed fields
5. **Connection Pooling**: Database connections reused

---

## 📊 Request/Response Flow

```
Client
  ↓
API Gateway (Django)
  ↓
HMAC Middleware (Authentication)
  ↓
URL Router
  ↓
View (Request Handler)
  ↓
Serializer (Validation)
  ↓
Service Layer (Business Logic)
  ↓
Model Layer (Database)
  ↓
Ledger Service (Accounting)
  ↓
Webhook Service (Notifications)
  ↓
Response to Client
```

---

## 🛠️ Technology Stack

- **Framework**: Django 4.2.7 + Django REST Framework
- **Database**: PostgreSQL (Render.com)
- **Cache/Queue**: Redis
- **Task Queue**: Celery
- **Crypto**: Web3.py (Ethereum, Polygon, BSC)
- **Encryption**: Cryptography (Fernet)

---

## 📝 Key Design Decisions

1. **Immutable Ledger**: Ensures audit trail and prevents fraud
2. **Service Layer**: Separates business logic from views
3. **HMAC Auth**: Industry-standard API authentication
4. **Webhook Retries**: Ensures reliable event delivery
5. **Multi-Method Support**: Unified interface for different payment types
6. **Token Vault**: PCI-compliant token storage

---

This architecture ensures **security**, **scalability**, and **reliability** for enterprise payment processing.

