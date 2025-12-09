from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse

import io
from PIL import Image
import qrcode

app = FastAPI(title="QR Code with Embedded Image")

@app.post("/generate_qr_with_logo")
async def generate_qr_with_logo(
    url: str = Form(...),
    image: UploadFile = File(...)
):
    """
    Generate a QR code pointing to `url` and embed the uploaded `image` at the center.
    """

    # Step 1: Read the uploaded image
    logo_bytes = await image.read()
    logo = Image.open(io.BytesIO(logo_bytes))
    logo = logo.convert("RGBA")

    # Step 2: Generate basic QR code
    qr = qrcode.QRCode(
        version=4,  # Controls size, 4 is moderate
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High, so logo doesn't break QR
        box_size=5,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Step 3: Resize logo to fit in the QR code
    qr_width, qr_height = qr_img.size
    logo_size = qr_width * 0.3 # logo takes up 1/4th of QR width
    logo.thumbnail((logo_size, logo_size))

    # Step 4: Calculate position to paste logo at center
    pos = ((qr_width - logo.width) // 2, (qr_height - logo.height) // 2)

    # Step 5: Paste logo on QR code
    qr_img.paste(logo, pos, mask=logo)

    # Step 6: Return QR as PNG response
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
