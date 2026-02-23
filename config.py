# config.py

import os
import hashlib

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-shared-key")
HMAC_ALGO = hashlib.sha256
