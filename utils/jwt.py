#jwt.py

import jwt

def decode_jwt(jwt_string: str):
    # Decode JWT without verification
    decoded = jwt.decode(
        jwt_string,
        options={"verify_signature": False}
    )

    # Extract QR parameters without defaults
    qr_params = {
        "data": decoded.get("data"),
        "foreground": decoded.get("foreground"),
        "background": decoded.get("background"),
        "scale": decoded.get("scale"),
        "shape": decoded.get("shape"),
        "shape_scale": decoded.get("shape_scale"),
        "error_level": decoded.get("error_level"),
        "iat": decoded.get("iat"),
        "exp": decoded.get("exp")
    }

    return qr_params