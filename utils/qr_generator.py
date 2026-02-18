# qr_converter.py

from styles.default_qr import generate_default_qr
from styles.custom_qr import generate_custom_qr
from utils.embed_logo import embed_logo_in_qr


def generate_qr(
        data: str,
        foreground: str,
        background: str,
        scale: int,
        shape: str,
        shape_scale,
        error_level: str,
        logo_image: bytes,
        logo_scale: float
):

    if shape == "default":
        qr_bytes = generate_default_qr(
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            error_level=error_level
        )
    else:
        qr_bytes = generate_custom_qr(
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            shape=shape,
            shape_scale=shape_scale,
            error_level=error_level
        )

    if logo_image:
        qr_bytes = embed_logo_in_qr(qr_bytes, logo_image, logo_scale)

    return qr_bytes