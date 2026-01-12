#!/usr/bin/env python3
import hmac
import hashlib
import time
import json
import requests
import uuid

BASE_URL = "https://api.buildforu.pw"
API_KEY = "y5XQpcXhxzzGfk5ND3b3iU0Np7HaZWYw_Z4w2b42h64"
SECRET_KEY = "-9iJc1OZXohB4gf3lanGob4M9ypMLFH4FeiyYCEPfKwNIa-dBjrs7Z_XiRqMD3paMgqCVYxH5k3oDDH1saikFQ"

def generate_signature(secret, timestamp, body):
    payload = f"{timestamp}{body}"
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

# Test 1: Health check
print("1. Health Check:")
r = requests.get(f"{BASE_URL}/")
print(f"   Status: {r.status_code}")

# Test 2: Create payment with proper headers
print("\n2. Create Payment:")
timestamp = str(int(time.time()))
body = json.dumps({
    "amount": "100.00",
    "method": "wallet",
    "user_id": str(uuid.uuid4()),
    "reference_id": f"TEST-{timestamp}"
}, separators=(',', ':'))
signature = generate_signature(SECRET_KEY, timestamp, body)

headers = {
    "X-API-Key": API_KEY,
    "X-Signature": signature,
    "X-Timestamp": timestamp,
    "Content-Type": "application/json"
}

print(f"   Timestamp: {timestamp}")
print(f"   Body: {body}")
print(f"   Signature: {signature[:30]}...")

r = requests.post(f"{BASE_URL}/v1/payments/create", headers=headers, data=body)
print(f"   Status: {r.status_code}")
print(f"   Response: {r.text[:200]}")

if r.status_code == 201:
    payment = r.json()
    payment_id = payment.get('id')
    print(f"\n3. Get Payment {payment_id}:")
    timestamp2 = str(int(time.time()))
    body2 = ""
    signature2 = generate_signature(SECRET_KEY, timestamp2, body2)
    headers2 = {
        "X-API-Key": API_KEY,
        "X-Signature": signature2,
        "X-Timestamp": timestamp2,
    }
    r2 = requests.get(f"{BASE_URL}/v1/payments/{payment_id}", headers=headers2)
    print(f"   Status: {r2.status_code}")
    print(f"   Response: {r2.text[:200]}")
