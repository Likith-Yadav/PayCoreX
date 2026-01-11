#!/usr/bin/env python
"""Check PayCoreX setup and configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

print("PayCoreX Configuration Check")
print("=" * 50)

# Check required settings
required_vars = [
    'SECRET_KEY',
    'DB_NAME',
    'DB_USER',
    'DB_PASSWORD',
    'DB_HOST',
    'REDIS_URL',
    'TOKEN_ENCRYPTION_KEY'
]

missing = []
for var in required_vars:
    value = os.getenv(var)
    if not value:
        missing.append(var)
        print(f"✗ {var}: NOT SET")
    else:
        # Mask sensitive values
        if 'PASSWORD' in var or 'SECRET' in var or 'KEY' in var:
            display_value = value[:10] + "..." if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"✓ {var}: {display_value}")

if missing:
    print(f"\n⚠️  Missing required variables: {', '.join(missing)}")
else:
    print("\n✓ All required environment variables are set!")

# Check optional settings
print("\nOptional Settings:")
optional_vars = {
    'ETHEREUM_RPC_URL': 'Crypto payments (Ethereum)',
    'POLYGON_RPC_URL': 'Crypto payments (Polygon)',
    'BSC_RPC_URL': 'Crypto payments (BSC)'
}

for var, description in optional_vars.items():
    value = os.getenv(var)
    if value and 'YOUR' not in value.upper():
        print(f"✓ {var}: Configured ({description})")
    else:
        print(f"○ {var}: Not configured ({description})")

print("\n" + "=" * 50)
print("Next steps:")
print("1. Update DB_PASSWORD if your PostgreSQL password is different")
print("2. Ensure PostgreSQL is running on DB_HOST:DB_PORT")
print("3. Ensure Redis is running")
print("4. Run: python manage.py migrate")
print("5. Run: python manage.py runserver")

