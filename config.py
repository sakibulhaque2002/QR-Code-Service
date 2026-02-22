# config.py

import os
import hashlib

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-shared-key")
HMAC_ALGO = hashlib.sha256
NONCE_LIFE_SECONDS = 24 * 60 * 60  # 24 hours
