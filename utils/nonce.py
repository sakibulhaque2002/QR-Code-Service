import hmac
import base64
import time
from fastapi import HTTPException
from config import SECRET_KEY, HMAC_ALGO


def get_tick(lifetime_seconds: int) -> int:
    tick_length = lifetime_seconds // 2
    now = int(time.time())
    return now // tick_length

def generate_nonce(tick: int) -> str:
    mac = hmac.new(
        SECRET_KEY.encode(),
        str(tick).encode(),
        HMAC_ALGO
    )
    sig_bytes = mac.digest()
    signature = base64.urlsafe_b64encode(sig_bytes).decode().rstrip("=")
    return signature[:12]  # truncate same as Java

def validate_nonce(claims: dict) -> None:
    # ✅ Verify nonce
    nonce = claims.get("nonce")
    lifetime = claims.get("nonce_lifetime")
    if not nonce or not lifetime:
        raise HTTPException(status_code=401, detail="Missing nonce or lifetime")
    if not verify_nonce(nonce, int(lifetime)):
        raise HTTPException(status_code=401, detail="Invalid or expired nonce")

    return claims

def verify_nonce(nonce: str, lifetime_seconds: int) -> bool:
    current_tick = get_tick(lifetime_seconds)
    if hmac.compare_digest(nonce, generate_nonce(current_tick)):
        return True
    # previous tick (grace window)
    if hmac.compare_digest(nonce, generate_nonce(current_tick - 1)):
        return True
    return False

