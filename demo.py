from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
import io
import re
import cairosvg
from PIL import Image
import segno

app = FastAPI(title="QR Code with Colored Heart Shapes")


def recolor_svg(svg_path: str, new_color: str) -> bytes:
    """Read SVG file and replace fill color with user-specified color."""
    with open(svg_path, "r") as f:
        svg_content = f.read()

    # Replace fill color attribute
    recolored_svg = re.sub(r'fill="[^"]*"', f'fill="{new_color}"', svg_content)

    # Convert SVG to PNG bytes
    png_bytes = cairosvg.svg2png(bytestring=recolored_svg.encode())
    return png_bytes


def create_heart_image(color: str, size: int) -> Image.Image:
    """Create a heart image with the specified color and size."""
    svg_path = "assets/heart.svg"
    png_bytes = recolor_svg(svg_path, color)

    heart = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    heart = heart.resize((size, size), Image.LANCZOS)
    return heart


@app.post("/generate_heart_qr")
async def generate_heart_qr(
        url: str = Form(...),
        heart_color: str = Form(default="#FF0000")  # Default red
):
    """
    Generate a QR code with heart shapes as modules.

    Parameters:
    - url: The URL to encode in the QR code
    - heart_color: Hex color for hearts (e.g., #FF0000 for red, #00FF00 for green)
    """

    # Step 1: Generate QR code matrix using segno
    qr = segno.make(url, error="l")
    matrix = qr.matrix

    # Step 2: Define sizes
    box_size = 5  # Size of each module/heart

    # Calculate image dimensions
    qr_width = len(matrix[0])
    qr_height = len(matrix)
    img_width = (qr_width) * box_size
    img_height = (qr_height) * box_size

    # Step 3: Create white background
    qr_img = Image.new("RGBA", (img_width, img_height), "white")

    # Step 4: Create heart image with user-specified color
    heart = create_heart_image(heart_color, box_size)

    # Step 5: Place hearts where QR modules are dark
    for row_idx, row in enumerate(matrix):
        for col_idx, module in enumerate(row):
            if module:  # Dark module (1 or True)
                x = (col_idx) * box_size
                y = (row_idx) * box_size
                qr_img.paste(heart, (x, y), mask=heart)

    # Step 6: Return as PNG
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
