import io
import re
import cairosvg
from PIL import Image

def create_shape(color: str, size: float) -> Image.Image:
    """Create a heart image with the specified color and size."""
    svg_path = "assets/heart.svg"

    """Read SVG file and replace fill color with user-specified color."""
    with open(svg_path, "r") as f:
        svg_content = f.read()

    # Replace fill color attribute
    recolored_svg = re.sub(r'fill="[^"]*"', f'fill="{color}"', svg_content)

    # Convert SVG to PNG bytes
    png_bytes = cairosvg.svg2png(bytestring=recolored_svg.encode())

    shape = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    shape = shape.resize((int(size), int(size)), Image.LANCZOS)
    return shape