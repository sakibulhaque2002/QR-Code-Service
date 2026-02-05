#base64_url

import base64

def decode_base64_url(b64_string: str) -> bytes:
    """
    Decode a Base64URL-encoded string into bytes, handling missing padding.
    """
    padding = 4 - (len(b64_string) % 4)
    if padding != 4:
        b64_string += "=" * padding

    try:
        return base64.urlsafe_b64decode(b64_string)

    except (base64.binascii.Error, ValueError) as e:
        raise ValueError(f"Invalid Base64 payload: {e}")