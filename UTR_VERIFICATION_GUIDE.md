# UTR Verification System Guide

## Overview
The UTR (Unique Transaction Reference) verification system allows users to submit their UTR number after completing a UPI payment, which is then verified against the actual payment transaction.

## How It Works

### User Flow
1. User creates payment → Status: "pending"
2. User scans QR code or clicks "Open in UPI App"
3. User completes payment in UPI app
4. User gets UTR number from UPI app
5. User returns to payment page
6. User clicks "I've Already Paid - Enter UTR"
7. User enters UTR number
8. System verifies UTR and updates payment status

### Verification Methods

#### 1. Automatic Verification (If Payment Gateway Configured)
- **Razorpay**: Verifies UTR via Razorpay API
- **PhonePe**: Verifies UTR via PhonePe API (when implemented)
- **Paytm**: Verifies UTR via Paytm API (when implemented)

#### 2. Manual Merchant Verification (Default)
- UTR is stored in payment metadata
- Merchant checks their bank account
- Merchant verifies UTR matches payment
- Merchant uses verify API to mark as success

## API Endpoints

### Submit UTR for Verification
**Endpoint:** `POST /v1/payments/{payment_id}/verify-utr`

**Request:**
```json
{
  "utr_number": "123456789012"
}
```

**Response (Auto-verified):**
```json
{
  "verified": true,
  "status": "success",
  "message": "Payment verified via Razorpay"
}
```

**Response (Pending Merchant Verification):**
```json
{
  "verified": false,
  "status": "pending_merchant_verification",
  "message": "UTR recorded. Merchant will verify it against their bank account."
}
```

### Merchant Verify Payment (with UTR)
**Endpoint:** `POST /v1/payments/{payment_id}/verify`

**Request:**
```json
{
  "transaction_id": "123456789012",
  "verify": true
}
```

## UTR Verification Process

### Step 1: User Submits UTR
- User enters UTR from their UPI app
- System stores UTR in payment metadata
- System attempts automatic verification

### Step 2: Automatic Verification (If Available)
- Checks payment gateway APIs (Razorpay, PhonePe, Paytm)
- Matches UTR with payment transaction
- If match found → Payment marked as success
- If no match → Goes to manual verification

### Step 3: Manual Verification (If Needed)
- Merchant receives notification (via webhook or dashboard)
- Merchant checks bank account for transaction
- Merchant verifies UTR matches payment amount
- Merchant uses verify API to confirm

## Where to Get UTR Number

### From UPI Apps
1. **PhonePe**: Transaction History → Select Payment → UTR shown in details
2. **Google Pay**: Transactions → Select Payment → UTR/Reference Number
3. **Paytm**: Passbook → Select Transaction → UTR shown
4. **BHIM UPI**: Transaction History → Select Payment → UTR shown

### UTR Format
- Typically 12 digits
- Can be alphanumeric
- Format: `123456789012` or `UPI123456789012`
- Length: 8-50 characters

## Implementation Details

### Payment Model Updates
- `metadata['utr_number']`: Stores user-submitted UTR
- `metadata['utr_submitted_at']`: Timestamp when UTR was submitted
- `provider_reference`: Updated with UTR number

### Verification Service
- `PaymentVerificationService.verify_utr()`: Main verification method
- `_verify_utr_razorpay()`: Razorpay API verification
- `_verify_utr_phonepe()`: PhonePe API verification (future)
- `_verify_utr_paytm()`: Paytm API verification (future)

## Limitations

### Current Limitations
1. **No Bank API Integration**: Cannot directly verify UTR with banks
2. **Manual Verification Required**: For UPI payments without payment gateway
3. **Payment Gateway Required**: For automatic verification

### Solutions

#### Option 1: Payment Gateway Integration (Recommended)
- Integrate Razorpay/PhonePe/Paytm SDKs
- Provides automatic UTR verification
- Most reliable method

#### Option 2: Bank API Integration (Future)
- Connect to merchant's bank account API
- Fetch transactions by UTR
- Auto-verify payments

#### Option 3: Manual Verification (Current)
- Merchant checks bank account
- Verifies UTR manually
- Uses verify API to confirm

## Testing

### Test UTR Submission
```bash
curl -X POST https://api.buildforu.pw/v1/payments/{payment_id}/verify-utr \
  -H "Content-Type: application/json" \
  -d '{"utr_number": "123456789012"}'
```

### Test Merchant Verification
```bash
curl -X POST https://api.buildforu.pw/v1/payments/{payment_id}/verify \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "X-Signature: YOUR_SIGNATURE" \
  -H "X-Timestamp: TIMESTAMP" \
  -H "Content-Type: application/json" \
  -d '{"transaction_id": "123456789012", "verify": true}'
```

## Best Practices

1. **Validate UTR Format**: Check length and format before submission
2. **Store UTR Securely**: UTR is stored in payment metadata
3. **Verify Promptly**: Merchant should verify UTR within 24 hours
4. **Handle Errors**: Provide clear error messages for invalid UTRs
5. **Auto-Refresh**: Payment page auto-refreshes after successful verification

## Future Enhancements

1. **Bank API Integration**: Direct bank account verification
2. **UPI Verification Service**: Third-party UTR verification APIs
3. **Automated Matching**: AI-based UTR matching with transaction history
4. **Real-time Notifications**: Push notifications when UTR is verified

