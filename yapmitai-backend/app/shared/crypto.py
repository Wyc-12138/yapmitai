import base64


def encrypt_api_key(value: str | None) -> str:
    if not value:
        return ""
    return base64.urlsafe_b64encode(value.encode("utf-8")).decode("ascii")


def decrypt_api_key(value: str | None) -> str:
    if not value:
        return ""
    return base64.urlsafe_b64decode(value.encode("ascii")).decode("utf-8")


def api_key_last4(value: str | None) -> str:
    return value[-4:] if value else ""
