from typing import Any
from uuid import uuid4


def success(data: Any = None, msg: str = "success") -> dict[str, Any]:
    return {
        "code": 200,
        "data": {} if data is None else data,
        "msg": msg,
        "traceId": str(uuid4()),
    }


def failure(code: int, msg: str, data: Any = None) -> dict[str, Any]:
    return {
        "code": code,
        "data": {} if data is None else data,
        "msg": msg,
        "traceId": str(uuid4()),
    }
