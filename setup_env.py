#!/usr/bin/env python
"""Setup script to generate .env file for PayCoreX"""
import secrets
from cryptography.fernet import Fernet
import os

def generate_env_file():
    """Generate .env file with secure random values"""
    
    # Generate secret key
    secret_key = secrets.token_urlsafe(50)
    
    # Generate token encryption key
    token_key = Fernet.generate_key().decode()
    
    env_content = f"""# Django Settings
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (PostgreSQL)
DB_NAME=paycorex
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://127.0.0.1:6379/1

# Celery Configuration
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Token Encryption Key (for token vault)
TOKEN_ENCRYPTION_KEY={token_key}

# Crypto RPC URLs (optional - for crypto payments)
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
POLYGON_RPC_URL=https://polygon-rpc.com
BSC_RPC_URL=https://bsc-dataseed.binance.org
"""
    
    env_file = '.env'
    
    if os.path.exists(env_file):
        response = input(f"{env_file} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✓ Created {env_file} with secure random values")
    print("\n⚠️  IMPORTANT: Update the following values in .env:")
    print("   - DB_PASSWORD: Set your PostgreSQL password")
    print("   - DB_USER: Set your PostgreSQL username if different")
    print("   - ETHEREUM_RPC_URL: Add your Infura API key for Ethereum")
    print("   - Set DEBUG=False in production")

if __name__ == '__main__':
    generate_env_file()

