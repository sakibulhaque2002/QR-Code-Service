# default_qr.py

import segno
import io
import cairosvg

def generate_default_qr(
        type,
        data,
        foreground = "#000000",
        background = "#FFFFFF",
        scale = 5,
        error_level = "h",
        output_format = "png"
):
    """
    Generate standard square QR code.
    """

    qr = segno.make(data, error=error_level)

    # PNG output
    out = io.BytesIO()
    qr.save(out, kind='png', dark=foreground, light=background, scale=scale)
    out.seek(0)

    return out.getvalue()
