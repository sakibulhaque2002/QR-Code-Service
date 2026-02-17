# customJwt.py

import base64
import json
import hmac
from fastapi import HTTPException

from config import SECRET_KEY, HMAC_ALGO

def sign_data(payload: str) -> str:
    mac = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        HMAC_ALGO
    )

    sig_bytes = mac.digest()

    # Base64 URL encode without padding
    signature = base64.urlsafe_b64encode(sig_bytes).decode().rstrip("=")

    # Truncate to 16 chars (must match Spring Boot)
    return signature[:16]


def verify_and_extract(token: str) -> dict:
    parts = token.split(".")

    if len(parts) != 2:
        raise HTTPException(status_code=400, detail="Invalid token format")

    payload_b64 = parts[0]
    received_signature = parts[1]

    # 🔐 Recompute signature
    expected_signature = sign_data(payload_b64)

    if not hmac.compare_digest(received_signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 📦 Decode payload
    try:
        padded = payload_b64 + "=" * (-len(payload_b64) % 4)
        decoded_bytes = base64.urlsafe_b64decode(padded)
        claims = json.loads(decoded_bytes)
        return claims
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")
