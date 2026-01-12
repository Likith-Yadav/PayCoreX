# PayCoreX API Integration Guide for Donation Sites

## Overview

This guide shows how to integrate PayCoreX API into your donation website, including:
1. Getting merchant's available payment methods
2. Creating payments
3. Redirecting to payment page with QR code
4. Handling payment status

## API Endpoints

### 1. Get Available Payment Methods

**Endpoint:** `GET /v1/payments/methods`

**Headers:**
```
X-API-Key: your-api-key
X-Signature: hmac-signature
X-Timestamp: unix-timestamp
```

**Response:**
```json
{
  "merchant_id": "uuid",
  "available_methods": [
    {
      "method": "upi_intent",
      "display_name": "UPI",
      "config_type": "upi",
      "upi_id": "merchant@upi"
    }
  ]
}
```

### 2. Create Payment

**Endpoint:** `POST /v1/payments/create`

**Request Body:**
```json
{
  "amount": 100,
  "method": "upi_intent",
  "user_id": "user-identifier",
  "reference_id": "donation-123",
  "metadata": {}
}
```

**Response:**
```json
{
  "id": "payment-uuid",
  "amount": "100.00",
  "status": "success",
  "payment_page_url": "/v1/payments/{payment_id}/page",
  ...
}
```

### 3. Payment Page (Public)

**URL:** `https://api.buildforu.pw/v1/payments/{payment_id}/page`

This page shows:
- QR code for UPI payment
- "Open in UPI App" button
- Auto-status checking

## Integration Flow

### Step 1: Get Payment Methods on Page Load

```javascript
async function getPaymentMethods() {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const body = "";
  const signature = await generateHMACSignature(SECRET_KEY, timestamp, body);
  
  const response = await fetch('https://api.buildforu.pw/v1/payments/methods', {
    method: 'GET',
    headers: {
      'X-API-Key': API_KEY,
      'X-Signature': signature,
      'X-Timestamp': timestamp
    }
  });
  
  const data = await response.json();
  
  // Show only available payment methods
  const methods = data.available_methods;
  // Display methods in your UI (e.g., only show UPI if available)
  return methods;
}
```

### Step 2: Create Payment When User Clicks "Donate"

```javascript
async function createPayment(amount, method, userId, referenceId) {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const body = JSON.stringify({
    amount: amount,
    method: method,
    user_id: userId,
    reference_id: referenceId
  });
  
  const signature = await generateHMACSignature(SECRET_KEY, timestamp, body);
  
  const response = await fetch('https://api.buildforu.pw/v1/payments/create', {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY,
      'X-Signature': signature,
      'X-Timestamp': timestamp,
      'Content-Type': 'application/json'
    },
    body: body
  });
  
  const payment = await response.json();
  
  if (response.ok) {
    // Redirect to payment page
    window.location.href = `https://api.buildforu.pw${payment.payment_page_url}`;
  } else {
    alert('Payment creation failed: ' + payment.error);
  }
}
```

### Step 3: HMAC Signature Generation

```javascript
async function generateHMACSignature(secret, timestamp, body) {
  const payload = timestamp + body;
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secret);
  const messageData = encoder.encode(payload);
  
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  
  const signature = await crypto.subtle.sign('HMAC', cryptoKey, messageData);
  const hashArray = Array.from(new Uint8Array(signature));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
```

## Complete Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>Donation Site</title>
</head>
<body>
    <h1>Make a Donation</h1>
    
    <form id="donationForm">
        <label>Amount: ₹</label>
        <input type="number" id="amount" value="100" min="1" required>
        
        <label>Payment Method:</label>
        <select id="paymentMethod">
            <!-- Options populated from API -->
        </select>
        
        <button type="submit">Donate Now</button>
    </form>
    
    <script>
        const API_KEY = 'your-api-key';
        const SECRET_KEY = 'your-secret-key';
        const BASE_URL = 'https://api.buildforu.pw';
        
        // Load payment methods on page load
        window.addEventListener('DOMContentLoaded', async () => {
            const methods = await getPaymentMethods();
            const select = document.getElementById('paymentMethod');
            methods.forEach(method => {
                const option = document.createElement('option');
                option.value = method.method;
                option.textContent = method.display_name;
                select.appendChild(option);
            });
        });
        
        // Handle form submission
        document.getElementById('donationForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const amount = document.getElementById('amount').value;
            const method = document.getElementById('paymentMethod').value;
            const userId = 'user-' + Date.now();
            const referenceId = 'donation-' + Date.now();
            
            await createPayment(amount, method, userId, referenceId);
        });
        
        // Include getPaymentMethods, createPayment, and generateHMACSignature functions from above
    </script>
</body>
</html>
```

## Payment Page Features

The payment page (`/v1/payments/{payment_id}/page`) automatically:
- Shows QR code for UPI payments
- Provides "Open in UPI App" button
- Auto-checks payment status every 5 seconds
- Redirects on successful payment

## Notes

1. **Payment Methods**: Only show methods returned by `/v1/payments/methods`
2. **UPI Configuration**: Merchant must have verified UPI ID in Payment Settings
3. **Payment Status**: Payment page auto-updates status
4. **Security**: Never expose SECRET_KEY in frontend code - use backend proxy

## Backend Proxy (Recommended)

For security, create a backend endpoint that proxies API calls:

```python
# Backend endpoint: /api/create-payment
@app.route('/api/create-payment', methods=['POST'])
def proxy_create_payment():
    # Generate HMAC signature on backend
    # Call PayCoreX API
    # Return response to frontend
    pass
```

This keeps your SECRET_KEY secure on the server.

