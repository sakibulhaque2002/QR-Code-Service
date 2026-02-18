#endpoints.py

from fastapi import APIRouter, Form, File, UploadFile, Query
from fastapi.responses import StreamingResponse
import io
import base64
import json
import hmac
import os
from fastapi import HTTPException
from fastapi import Request


from utils.qr_generator import generate_qr
from utils.customJwt import verify_and_extract
from utils.helpers import get_final
from utils.resolve_logo import resolve_logo, resolve_logo_file
from utils.template import get_template

router = APIRouter()  # single router for all endpoints


@router.post("/post_qr_code")
async def post_qr_code(
        request: Request,
        template: str = Form("default"),
        data: str = Form(...),  # QR content

        foreground: str = Form(None),
        background: str = Form(None),
        scale: int = Form(None),
        shape: str = Form(None),
        shape_scale: float = Form(None),
        error_level: str = Form(None),
        logo_image: UploadFile = File(None),
        logo_scale: float = Form(None),
):

    template_config = get_template(request, template)

    logo_bytes = await resolve_logo_file(logo_image, template_config)

    # Generate QR using template config
    qr_bytes = generate_qr(
        data=data,
        foreground=get_final(foreground, template_config.get("foreground")),
        background=get_final(background, template_config.get("background")),
        scale=get_final(scale, template_config.get("scale")),
        shape=get_final(shape, template_config.get("shape")),
        shape_scale=get_final(shape_scale, template_config.get("shape_scale")),
        error_level=get_final(error_level, template_config.get("error_level")),
        logo_image=logo_bytes,
        logo_scale=get_final(logo_scale, template_config.get("logo_scale"))
    )

    return StreamingResponse(io.BytesIO(qr_bytes), media_type="image/png")


@router.get("/get_qr_code")
async def get_qr_code(token: str = Query(...), request: Request = None):

    qr_params=verify_and_extract(token)

    # 4️⃣ Extract template_name from payload (default to "DEFAULT")
    template_name = qr_params.get("template", "default")
    template_config = get_template(request, template_name)

    # 5️⃣ Handle logo (no file upload in GET, fallback to template)
    logo_bytes = resolve_logo(qr_params.get("logo_image"), template_config)

    # 6️⃣ Generate QR using payload values or template defaults
    qr_bytes = generate_qr(
        data=qr_params.get("data"),
        foreground=get_final(qr_params.get("foreground"), template_config.get("foreground")),
        background=get_final(qr_params.get("background"), template_config.get("background")),
        scale=get_final(qr_params.get("scale"), template_config.get("scale")),
        shape=get_final(qr_params.get("shape"), template_config.get("shape")),
        shape_scale=get_final(qr_params.get("shape_scale"), template_config.get("shape_scale")),
        error_level=get_final(qr_params.get("error_level"), template_config.get("error_level")),
        logo_image=logo_bytes,
        logo_scale=get_final(qr_params.get("logo_scale"), template_config.get("logo_scale"))
    )

    return StreamingResponse(io.BytesIO(qr_bytes), media_type="image/png")
