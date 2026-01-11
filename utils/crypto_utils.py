import secrets
import hashlib


def generate_api_key():
    return secrets.token_urlsafe(32)


def generate_secret():
    return secrets.token_urlsafe(64)


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

