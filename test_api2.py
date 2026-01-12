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
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    print(f"DEBUG: payload={payload[:50]}...")
    print(f"DEBUG: signature={sig[:30]}...")
    return sig

# Test payment creation
timestamp = str(int(time.time()))
body = json.dumps({"amount": "100.00", "method": "wallet", "user_id": str(uuid.uuid4()), "reference_id": f"TEST-{int(time.time())}"}, separators=(',', ':'))
signature = generate_signature(SECRET_KEY, timestamp, body)

headers = {
    "X-API-Key": API_KEY,
    "X-Signature": signature,
    "X-Timestamp": timestamp,
    "Content-Type": "application/json"
}

print(f"\nHeaders: {headers}")
print(f"Body: {body}")

r = requests.post(f"{BASE_URL}/v1/payments/create", headers=headers, data=body)
print(f"\nStatus: {r.status_code}")
print(f"Response: {r.text}")
