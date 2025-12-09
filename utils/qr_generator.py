# qr_converter.py

import segno
from PIL import Image
import io
import cairosvg
from styles.default_qr import generate_default_qr
from styles.heart_qr import generate_heart_qr


def generate_qr(
        type: str,
        data: str,
        foreground: str = "#000000",
        background: str = "#FFFFFF",
        scale: int = 5,
        style: str="default",
        error_level: str = "h",
        output_format: str = "png"

):
    """
    Main QR generator function. Dispatches to specific style modules.
    """

    # Dispatch to correct style
    if style == "heart":
        return generate_heart_qr(
            type=type,
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            error_level=error_level,
            output_format=output_format
        )
    else:  # default or unknown style
        return generate_default_qr(
            type=type,
            data=data,
            foreground=foreground,
            background=background,
            scale=scale,
            error_level=error_level,
            output_format=output_format
        )