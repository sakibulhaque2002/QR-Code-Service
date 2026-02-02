# main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import io

from utils.qr_generator import generate_qr

app = FastAPI(title="Custom QR Code API")

@app.post("/generate_qr")
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

    # Determine media_type
    media_type = "image/png"

    return StreamingResponse(io.BytesIO(qr_bytes), media_type=media_type)
