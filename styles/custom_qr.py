import segno
from PIL import Image
import io

from utils.shape import create_shape

def generate_custom_qr(
        data,
        foreground = "black",
        background = "white",
        scale = 5,
        shape=None,
        shape_scale=1.3,
        error_level = "h"
):

    # Step 1: Generate QR code matrix using segno
    qr = segno.make(data, error=error_level)
    matrix = qr.matrix

    # Step 2: Define image dimensions
    border = 4
    qr_width = len(matrix[0])
    qr_height = len(matrix)
    img_width = (qr_width + 2 * border) * scale
    img_height = (qr_height + 2 * border) * scale

    # Step 3: Create colored background
    qr_img = Image.new("RGBA", (img_width, img_height), background)

    # Step 4: Create heart image with user-specified color
    module_shape = create_shape(foreground, shape, scale * shape_scale)

    # Step 5: Place hearts where QR modules are dark
    for row_idx, row in enumerate(matrix):
        for col_idx, module in enumerate(row):
            if module:  # Dark module (1 or True)
                x = (col_idx + border) * scale
                y = (row_idx + border) * scale
                qr_img.paste(module_shape, (x, y), mask=module_shape)

    # Step 6: Return as PNG
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()
