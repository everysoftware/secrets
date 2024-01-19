import base64
from io import BytesIO

import qrcode


def generate_qr_code(uri: str) -> str:
    img = qrcode.make(uri)
    buffered = BytesIO()
    img.save(buffered)

    return base64.b64encode(buffered.getvalue()).decode()
