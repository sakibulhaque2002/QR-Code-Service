# main.py

from PIL.ImageOps import scale
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from utils.qr_generator import generate_qr
import io
import os

app = FastAPI(title="Custom QR Code API")

@app.post("/generate_qr")
async def generate_qr_endpoint(
        type: str = Form(...),  # QR type
        data: str = Form(...),  # QR content
        foreground: str = Form("#000000"),
        background: str = Form("#FFFFFF"),
        scale: int = Form(5),
        style: str = Form("default"),  # default, heart, circle, etc.
        error_level: str = Form("h"),  # l, m, q, h
        logo_image: UploadFile = File(None),  # Optional logo
        logo_scale: float = Form(0.3),       # Fraction of QR width for logo
        output_format: str = Form("png"),
):

    # Generate QR
    qr_bytes = generate_qr(
        type=type,
        data=data,
        foreground=foreground,
        background=background,
        scale=scale,
        style=style,
        error_level=error_level,
        logo_image=logo_image,
        logo_scale=logo_scale,
        output_format=output_format
    )

    # Determine media_type
    media_type = "image/png"

    return StreamingResponse(io.BytesIO(qr_bytes), media_type=media_type)
