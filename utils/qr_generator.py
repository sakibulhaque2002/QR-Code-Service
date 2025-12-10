# qr_converter.py

import segno
from PIL import Image
import io
import cairosvg
from styles.default_qr import generate_default_qr
from styles.heart_qr import generate_heart_qr
from utils.logo_qr import embed_logo_in_qr


def generate_qr(
        type: str,
        data: str,
        foreground: str = "#000000",
        background: str = "#FFFFFF",
        scale: int = 5,
        style: str="default",
        error_level: str = "h",
        logo_image=None,       # <-- now accepts UploadFile
        logo_scale: float = 0.3,
        output_format: str = "png"

):
    """
    Main QR generator function. Dispatches to specific style modules.
    """

    # Dispatch to correct style
    if style == "heart":
        qr_bytes=generate_heart_qr(
            type=type,
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            error_level=error_level,
            output_format=output_format
        )
    else:  # default or unknown style
        qr_bytes=generate_default_qr(
            type=type,
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            error_level=error_level,
            output_format=output_format
        )

    if logo_image:
        # Read bytes from UploadFile
        logo_bytes = logo_image.file.read()
        qr_bytes = embed_logo_in_qr(qr_bytes, logo_bytes, logo_scale)

    return qr_bytes