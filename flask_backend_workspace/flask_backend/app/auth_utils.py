import hashlib
import hmac
import os
import base64
from datetime import datetime, timedelta

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")  # Should be set in .env for production

# PUBLIC_INTERFACE
def hash_password(password):
    """Hash a password using SHA-256 (for demo; use bcrypt/argon2 in production)"""
    salt = os.environ.get("PASSWORD_SALT", "static-salt")
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

# PUBLIC_INTERFACE
def verify_password(password, hash_val):
    """Verify input password against stored hash"""
    return hmac.compare_digest(hash_password(password), hash_val)

# PUBLIC_INTERFACE
def generate_token(user_id, expiry_hours=24):
    """Generate a primitive JWT-like token (NOT FOR production use)"""
    expiry = int((datetime.utcnow() + timedelta(hours=expiry_hours)).timestamp())
    token_str = f"{user_id}:{expiry}"
    signature = hmac.new(SECRET_KEY.encode(), token_str.encode(), hashlib.sha256).digest()
    token = f"{token_str}:{base64.urlsafe_b64encode(signature).decode()}"
    return base64.urlsafe_b64encode(token.encode()).decode()

# PUBLIC_INTERFACE
def decode_token(token):
    """Decode and validate the token, return user_id if valid, else None"""
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        parts = decoded.split(":")
        if len(parts) != 3:
            return None
        user_id, expiry, sig = parts
        expected_sig = hmac.new(SECRET_KEY.encode(), f"{user_id}:{expiry}".encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(base64.urlsafe_b64encode(expected_sig).decode(), sig):
            return None
        if int(expiry) < int(datetime.utcnow().timestamp()):
            return None
        return int(user_id)
    except Exception:
        return None
