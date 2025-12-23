# default_qr.py

import segno
import io

def generate_default_qr(
        data,
        foreground = "black",
        background = "white",
        scale = 5,
        error_level = "h"
):

    qr = segno.make(data, error=error_level)

    # PNG output
    out = io.BytesIO()
    qr.save(out, kind='png', dark=foreground, light=background, scale=scale)
    out.seek(0)

    return out.getvalue()
