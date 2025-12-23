# qr_converter.py

from styles.default_qr import generate_default_qr
from styles.heart_qr import generate_custom_qr
from utils.logo import embed_logo_in_qr


def generate_qr(
        data: str,
        foreground: str = "black",
        background: str = "white",
        scale: int = 5,
        shape: str="default",
        shape_scale=1.3,
        error_level: str = "h",
        logo_image=None,
        logo_scale: float = 0.2
):

    if shape == "heart":
        qr_bytes=generate_custom_qr(
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            shape_scale=shape_scale,
            error_level=error_level
        )
    else:
        qr_bytes=generate_default_qr(
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            error_level=error_level
        )

    if logo_image:
        logo_bytes = logo_image.file.read()
        qr_bytes = embed_logo_in_qr(qr_bytes, logo_bytes, logo_scale)

    return qr_bytes