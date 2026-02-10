from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

def make_reset_token(user_id: int) -> str:
    s = _serializer()
    return s.dumps({"uid": user_id, "purpose": "password_reset"})

def verify_reset_token(token: str, max_age_seconds: int = 3600):
    s = _serializer()
    try:
        data = s.loads(token, max_age=max_age_seconds)
        if data.get("purpose") != "password_reset":
            return None
        return int(data.get("uid"))
    except Exception:
        return None
