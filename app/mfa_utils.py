import base64
from io import BytesIO
import pyotp
import qrcode

def generate_secret() -> str:
    return pyotp.random_base32()

def provisioning_uri(secret: str, username: str, issuer_name: str = "PindolaVermellaDemo") -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer_name)

def verify_token(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)

def qr_code_data_uri(uri: str) -> str:
    img = qrcode.make(uri)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
