import segno
from PIL import Image
import io
import os
import cairosvg
from utils.shape import create_shape

def generate_heart_qr(
        data,
        foreground = "#000000",
        background = "#FFFFFF",
        scale = 5,
        error_level = "h"
):
    """
    Generate QR code with heart-shaped modules.
    """

    # Step 1: Generate QR code matrix using segno
    qr = segno.make(data, error=error_level)
    matrix = qr.matrix

    # Step 2: Define image dimensions
    qr_width = len(matrix[0])
    qr_height = len(matrix)
    img_width = (qr_width) * scale
    img_height = (qr_height) * scale

    # Step 3: Create colored background
    qr_img = Image.new("RGBA", (img_width, img_height), background)

    # Step 4: Create heart image with user-specified color
    heart = create_shape(foreground, scale * 1.5)

    # Step 5: Place hearts where QR modules are dark
    for row_idx, row in enumerate(matrix):
        for col_idx, module in enumerate(row):
            if module:  # Dark module (1 or True)
                x = (col_idx) * scale
                y = (row_idx) * scale
                qr_img.paste(heart, (x, y), mask=heart)

    # Step 6: Return as PNG
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()
