from jwt import encode, decode
from config.config import settings

def create_token(data: dict):
    return encode(payload=data, key=settings.secret_key, algorithm=settings.algorithm)

def validate_token(token: str) -> dict:
    try:
        data: dict = decode(token, key=settings.secret_key, algorithms=[settings.algorithm])
        return data
    except:
        return {}