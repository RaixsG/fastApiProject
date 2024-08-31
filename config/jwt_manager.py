from jwt import encode, decode

def create_token(data: dict):
    return encode(payload=data, key="secret", algorithm="HS256")

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="secret", algorithms=["HS256"])
    return data