# qr_converter.py

import segno
from PIL import Image
import io
import cairosvg
from styles.default_qr import generate_default_qr
from styles.heart_qr import generate_heart_qr
from utils.logo import embed_logo_in_qr


def generate_qr(
        data: str,
        foreground: str = "#000000",
        background: str = "#FFFFFF",
        scale: int = 5,
        shape: str="default",
        error_level: str = "h",
        logo_image=None,       # <-- now accepts UploadFile
        logo_scale: float = 0.3
):
    """
    Main QR generator function. Dispatches to specific shape modules.
    """

    # Dispatch to correct shape
    if shape == "heart":
        qr_bytes=generate_heart_qr(
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            error_level=error_level
        )
    else:  # default or unknown shape
        qr_bytes=generate_default_qr(
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            error_level=error_level
        )

    if logo_image:
        # Read bytes from UploadFile
        logo_bytes = logo_image.file.read()
        qr_bytes = embed_logo_in_qr(qr_bytes, logo_bytes, logo_scale)

    return qr_bytes