#endpoints.py

from fastapi import APIRouter, Form, File, UploadFile, Query
from fastapi.responses import StreamingResponse
import io
import base64
import json
import hmac
from fastapi import HTTPException
from fastapi import Request


from utils.qr_generator import generate_qr
from utils.jwt import decode_jwt
from utils.gzip import decompress_gzip
from utils.base64_url import decode_base64_url
from utils.customJwt import sign_data

router = APIRouter()  # single router for all endpoints


@router.post("/generate_qr_v1")
async def generate_qr_v1(
        request: Request,
        template_name: str = Form("DEFAULT"),
        data: str = Form(...),  # QR content
        foreground: str = Form("black"),
        background: str = Form("white"),
        scale: int = Form(5),
        shape: str = Form("default"),  # default, heart, circle, etc.
        shape_scale: float = Form(1.3),
        error_level: str = Form("h"),  # l, m, q, h
        # logo_image: UploadFile = File(None),
        logo_scale: float = Form(0.2),       # Fraction of QR width for logo
):
    # Get templates from app state
    templates = request.app.state.qr_templates

    # Validate template
    if template_name not in templates:
        raise HTTPException(status_code=400, detail="Invalid template name")

    template_config = templates[template_name]

    # Generate QR using template config
    qr_bytes = generate_qr(
        data=data,
        foreground=template_config.get("foreground"),
        background=template_config.get("background"),
        scale=template_config.get("scale"),
        shape=template_config.get("shape"),
        shape_scale=template_config.get("shape_scale"),
        error_level=template_config.get("error_level"),
        # logo_image=logo_image,
        # logo_scale=template_config["logo_scale"]
    )

    return StreamingResponse(io.BytesIO(qr_bytes), media_type="image/png")




@router.get("/generate_qr_v2")
async def generate_qr_v2(payload: str = Query(...)):

    b64_string = payload

    # 1️⃣ Base64URL decode (handle padding)
    compressed_bytes=decode_base64_url(b64_string)

    # 2️⃣ GZIP decompress
    jwt_string = decompress_gzip(compressed_bytes)

    # 3️⃣ Decode JWT without verifying signature (just extract claims)
    qr_params=decode_jwt(jwt_string)

    # Generate QR
    qr_bytes = generate_qr(
        data=qr_params["data"],
        foreground=qr_params["foreground"],
        background=qr_params["background"],
        scale=qr_params["scale"],
        shape=qr_params["shape"],
        shape_scale=qr_params["shape_scale"],
        error_level=qr_params["error_level"]
    )

    return StreamingResponse(io.BytesIO(qr_bytes), media_type="image/png")


@router.get("/generate_qr_v3")
def generate_qr_v3(customJwt: str = Query(...)):

    token = customJwt

    # 1️⃣ Split payload.signature
    parts = token.split(".")
    if len(parts) != 2:
        raise HTTPException(status_code=400, detail="Invalid token format")

    payload_b64 = parts[0]
    received_signature = parts[1]

    # 2️⃣ Verify signature
    expected_signature = sign_data(payload_b64)

    if not hmac.compare_digest(received_signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 3️⃣ Decode payload
    try:
        padded = payload_b64 + "=" * (-len(payload_b64) % 4)
        decoded_bytes = base64.urlsafe_b64decode(padded)
        qr_params = json.loads(decoded_bytes)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")

    # Generate QR
    qr_bytes = generate_qr(
        data=qr_params["data"],
        foreground=qr_params["foreground"],
        background=qr_params["background"],
        scale=qr_params["scale"],
        shape=qr_params["shape"],
        shape_scale=qr_params["shape_scale"],
        error_level=qr_params["error_level"]
    )

    return StreamingResponse(io.BytesIO(qr_bytes), media_type="image/png")
