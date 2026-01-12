#!/usr/bin/env python3
import hmac
import hashlib
import time
import json
import requests
import uuid

BASE_URL = "https://api.paycorex.dev"
API_KEY = "y5XQpcXhxzzGfk5ND3b3iU0Np7HaZWYw_Z4w2b42h64"
SECRET_KEY = "-9iJc1OZXohB4gf3lanGob4M9ypMLFH4FeiyYCEPfKwNIa-dBjrs7Z_XiRqMD3paMgqCVYxH5k3oDDH1saikFQ"

def generate_signature(secret, timestamp, body):
    payload = f"{timestamp}{body}"
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

def make_request(method, endpoint, body=None):
    url = f"{BASE_URL}{endpoint}"
    timestamp = str(int(time.time()))
    body_str = json.dumps(body, separators=(',', ':')) if body else ""
    signature = generate_signature(SECRET_KEY, timestamp, body_str)
    headers = {
        "X-API-Key": API_KEY,
        "X-Signature": signature,
        "X-Timestamp": timestamp,
        "Content-Type": "application/json"
    }
    print(f"\n{'='*60}")
    print(f"{method} {endpoint}")
    print(f"Body: {body_str}")
    print(f"{'='*60}")
    if method == "GET":
        return requests.get(url, headers=headers)
    return requests.post(url, headers=headers, data=body_str)

print("Testing PayCoreX API...")
print("\n1. Health Check:")
r = requests.get(f"{BASE_URL}/")
print(f"Status: {r.status_code}, Response: {r.text[:100]}")

print("\n2. Create Payment:")
payment_data = {
    "amount": "100.00",
    "method": "wallet",
    "user_id": str(uuid.uuid4()),
    "reference_id": f"TEST-{int(time.time())}"
}
r = make_request("POST", "/v1/payments/create", payment_data)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")
if r.status_code == 201:
    payment = r.json()
    payment_id = payment.get('id')
    print(f"\n3. Get Payment {payment_id}:")
    r2 = make_request("GET", f"/v1/payments/{payment_id}")
    print(f"Status: {r2.status_code}")
    print(f"Response: {r2.text}")
