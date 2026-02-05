#gzip.py

import gzip
import io

def decompress_gzip(compressed_bytes: bytes) -> str:
    """
    Decompress GZIP-compressed bytes and return decoded string.
    """
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(compressed_bytes)) as f:
            return f.read().decode("utf-8")
    except (OSError, gzip.BadGzipFile) as e:
        raise ValueError(f"Invalid GZIP payload: {e}")