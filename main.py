# main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body, Query
from fastapi.responses import StreamingResponse
import io

from utils.qr_generator import generate_qr
from utils.jwt import decode_jwt
from utils.gzip import decompress_gzip
from utils.base64_url import decode_base64_url

app = FastAPI(title="Custom QR Code API")


@app.post("/generate_qr_v1")
async def generate_qr_endpoint(
        data: str = Form(...),  # QR content
        foreground: str = Form("black"),
        background: str = Form("white"),
        scale: int = Form(5),
        shape: str = Form("default"),  # default, heart, circle, etc.
        shape_scale: float = Form(1.3),
        error_level: str = Form("h"),  # l, m, q, h
        logo_image: UploadFile = File(None),
        logo_scale: float = Form(0.2),       # Fraction of QR width for logo
):

    # Generate QR
    qr_bytes = generate_qr(
        data=data,
        foreground=foreground,
        background=background,
        scale=scale,
        shape=shape,
        shape_scale=shape_scale,
        error_level=error_level,
        logo_image=logo_image,
        logo_scale=logo_scale
    )

    return StreamingResponse(io.BytesIO(qr_bytes), media_type="image/png")


@app.get("/generate_qr_v3")
async def decode_payload_endpoint(payload: str = Query(...)):

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

