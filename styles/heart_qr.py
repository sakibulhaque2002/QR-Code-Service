import segno
from PIL import Image
import io
import os
import cairosvg

def generate_heart_qr(
        type,
        data,
        foreground = "#000000",
        background = "#FFFFFF",
        scale = 5,
        error_level = "h",
        output_format = "png"
):
    """
    Generate QR code with heart-shaped modules.
    """

    qr = segno.make(data, error=error_level)
    matrix = qr.matrix

    # Heart image path
    heart_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "heart.png")

    heart = Image.open(heart_path).convert("RGBA")
    heart = heart.resize((scale, scale))

    rows = len(matrix)
    cols = len(matrix[0])

    out = Image.new("RGB", (cols * scale, rows * scale), background)

    for y, row in enumerate(matrix):
        for x, val in enumerate(row):
            if val:  # draw heart only for black modules
                out.paste(heart, (x * scale, y * scale), heart)


    # PNG output
    buffer = io.BytesIO()
    out.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()
