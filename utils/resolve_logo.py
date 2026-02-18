# utils/resolve_logo.py

import os
from fastapi import HTTPException, UploadFile


async def resolve_logo_file(uploaded_logo: UploadFile, template_config: dict):
    """
    Priority:
    1. Uploaded logo
    2. Template logo
    3. None
    """

    # 1️⃣ If user uploaded logo
    if uploaded_logo is not None:
        return await uploaded_logo.read()

    # 2️⃣ If template has logo
    logo_filename = template_config.get("logo_image")
    if logo_filename:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "logos", logo_filename)

        if not os.path.exists(logo_path):
            raise HTTPException(
                status_code=500,
                detail=f"Logo file '{logo_filename}' not found"
            )

        with open(logo_path, "rb") as f:
            return f.read()

    # 3️⃣ No logo
    return None


import os
import base64
from fastapi import HTTPException


def resolve_logo(logo_base64: str, template_config: dict):
    """
    Priority:
    1. Logo from JWT (Base64 string)
    2. Template logo file
    3. None
    """

    # 1️⃣ If logo exists in JWT payload
    if logo_base64:
        try:
            return base64.b64decode(logo_base64)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid logo image encoding"
            )

    # 2️⃣ If template has logo
    logo_filename = template_config.get("logo_image")
    if logo_filename:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "logos", logo_filename)

        if not os.path.exists(logo_path):
            raise HTTPException(
                status_code=500,
                detail=f"Logo file '{logo_filename}' not found"
            )

        with open(logo_path, "rb") as f:
            return f.read()

    # 3️⃣ No logo
    return None
