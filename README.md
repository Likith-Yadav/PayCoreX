# PayCoreX - Payment Orchestration Platform

Enterprise-grade payment orchestration platform built with Django REST Framework.

## Features

- Merchant onboarding with API keys and secrets
- HMAC signature verification
- Payment orchestration (UPI, Wallet, Tokenized, Crypto)
- Ledger-based accounting system
- Wallet system with balance management
- Token vault for secure storage
- Webhook engine with retry mechanism
- Refund system (partial and full)
- Crypto payment listener using Web3.py
- Dashboard APIs for analytics

## Setup

1. **Create and activate virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate  # Linux/Mac
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
# Generate .env file with secure random values
python setup_env.py
```

Or manually create `.env` file (see `env.example` for template):
- Update `DB_PASSWORD` with your PostgreSQL password
- Update `DB_USER` if different from `postgres`
- Add `ETHEREUM_RPC_URL` with your Infura API key (optional, for crypto payments)
- Set `DEBUG=False` in production

4. **Verify configuration:**
```bash
python check_setup.py
```

5. **Ensure services are running:**
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`

6. **Run migrations:**
```bash
python manage.py migrate
```

7. **Create superuser (optional):**
```bash
python manage.py createsuperuser
```

8. **Start server:**
```bash
python manage.py runserver
```

9. **Start Celery worker (for background tasks):**
```bash
celery -A core worker -l info
```

## API Endpoints

### Merchant
- `POST /v1/merchants/register` - Register merchant
- `POST /v1/merchants/apikey` - Regenerate API key
- `GET /v1/merchants/profile` - Get merchant profile

### Payments
- `POST /v1/payments/create` - Create payment
- `GET /v1/payments/{payment_id}` - Get payment details
- `POST /v1/payments/refund` - Create refund

### Wallet
- `POST /v1/wallet/create` - Create wallet
- `POST /v1/wallet/topup` - Top up wallet
- `POST /v1/wallet/pay` - Pay from wallet
- `GET /v1/wallet/balance` - Get wallet balance

### Tokens
- `POST /v1/tokens/store` - Store payment token
- `GET /v1/tokens/list` - List tokens
- `DELETE /v1/tokens/{id}` - Delete token

### Webhooks
- `POST /v1/webhooks/provider` - Create webhook endpoint
- `POST /v1/webhooks/retry` - Retry webhook delivery

### Crypto
- `POST /v1/crypto/address` - Register crypto address
- `GET /v1/crypto/status/{tx}` - Get transaction status

### Dashboard
- `GET /v1/dashboard/stats` - Get statistics
- `GET /v1/dashboard/payments` - Get payments list
- `GET /v1/dashboard/ledgers` - Get ledger entries

