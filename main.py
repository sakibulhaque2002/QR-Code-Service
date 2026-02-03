# main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body, Query
from fastapi.responses import StreamingResponse
import io
import jwt
import base64
import gzip

from utils.qr_generator import generate_qr
from models.request_body import RequestBody

app = FastAPI(title="Custom QR Code API")


@app.get("/hello")
async def hello():
    return "Hello, World!"


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


@app.get("/receive_qr")
async def receive_qr_endpoint(
        data: str = Form(...),  # QR content
        foreground: str = Form("black"),
        background: str = Form("white"),
        scale: int = Form(5),
        shape: str = Form("default"),  # default, heart, circle, etc.
        shape_scale: float = Form(1.3),
        error_level: str = Form("h"),  # l, m, q, h
        logo_image: UploadFile = File(None),
        logo_scale: float = Form(0.2),  # Fraction of QR width for logo
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


@app.post("/decode_jwt")
async def decode_jwt_endpoint(request: RequestBody = Body(...)):
    try:
        # Decode JWT without verification
        decoded = jwt.decode(
            request.jwt,
            options={"verify_signature": False}
        )

        # Extract QR parameters without defaults
        qr_params = {
            "data": decoded.get("data"),
            "foreground": decoded.get("foreground"),
            "background": decoded.get("background"),
            "scale": decoded.get("scale"),
            "shape": decoded.get("shape"),
            "shape_scale": decoded.get("shape_scale"),
            "error_level": decoded.get("error_level"),
            "iat": decoded.get("iat"),
            "exp": decoded.get("exp")
        }

        return qr_params

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/decode_payload")
async def decode_payload_endpoint(payload: str = Query(...)):
    try:
        # 1️⃣ Base64URL decode (handle padding)
        b64_string = payload
        # Add padding if missing
        padding = 4 - (len(b64_string) % 4)
        if padding != 4:
            b64_string += "=" * padding
        compressed_bytes = base64.urlsafe_b64decode(b64_string)

        # 2️⃣ GZIP decompress
        with gzip.GzipFile(fileobj=io.BytesIO(compressed_bytes)) as f:
            jwt_string = f.read().decode("utf-8")

        # 3️⃣ Decode JWT without verifying signature (just extract claims)
        decoded = jwt.decode(jwt_string, options={"verify_signature": False})

        # 4️⃣ Extract QR parameters
        qr_params = {
            "data": decoded.get("data"),
            "foreground": decoded.get("foreground"),
            "background": decoded.get("background"),
            "scale": decoded.get("scale"),
            "shape": decoded.get("shape"),
            "shape_scale": decoded.get("shape_scale"),
            "error_level": decoded.get("error_level"),
            "iat": decoded.get("iat"),
            "exp": decoded.get("exp")
        }

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

    except (OSError, gzip.BadGzipFile):
        raise HTTPException(status_code=400, detail="Invalid GZIP payload")
    except (base64.binascii.Error, ValueError):
        raise HTTPException(status_code=400, detail="Invalid Base64 payload")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")

