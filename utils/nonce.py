import hmac
import hashlib
import base64
import time
from config import SECRET_KEY, HMAC_ALGO, NONCE_LIFE_SECONDS

def get_tick(life_time_seconds: int = NONCE_LIFE_SECONDS) -> int:
    tick_length = life_time_seconds // 2
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

def verify_nonce(nonce: str, life_time_seconds: int = NONCE_LIFE_SECONDS) -> bool:
    current_tick = get_tick(life_time_seconds)
    if hmac.compare_digest(nonce, generate_nonce(current_tick)):
        return True
    # previous tick (grace window)
    if hmac.compare_digest(nonce, generate_nonce(current_tick - 1)):
        return True
    return False