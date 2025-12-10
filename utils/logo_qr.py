# utils/qr_logo.py

import io
from PIL import Image

def embed_logo_in_qr(qr_bytes: bytes, logo_bytes: bytes, logo_scale: float = 0.3) -> bytes:
    """
    Embeds a logo at the center of the QR code.

    :param qr_bytes: Generated QR code in bytes.
    :param logo_bytes: Uploaded logo image in bytes.
    :param logo_scale: Size of the logo as a fraction of the QR width.
    :return: Modified QR code with embedded logo as bytes.
    """

    # Open QR image
    qr_img = Image.open(io.BytesIO(qr_bytes)).convert("RGBA")
    logo = Image.open(io.BytesIO(logo_bytes)).convert("RGBA")

    # Resize logo
    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width * logo_scale)
    logo.thumbnail((logo_size, logo_size))

    # Center position
    pos = ((qr_width - logo.width) // 2, (qr_height - logo.height) // 2)

    # Paste logo onto QR
    qr_img.paste(logo, pos, mask=logo)

    # Convert back to bytes
    out_buf = io.BytesIO()
    qr_img.save(out_buf, format="PNG")
    return out_buf.getvalue()
