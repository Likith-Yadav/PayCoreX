import hmac
import hashlib
import json


def generate_webhook_signature(payload, secret):
    payload_str = json.dumps(payload, sort_keys=True) if isinstance(payload, dict) else payload
    return hmac.new(
        secret.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()


def verify_webhook_signature(signature, payload, secret):
    expected = generate_webhook_signature(payload, secret)
    return hmac.compare_digest(signature, expected)

