from math import ceil
from typing import Any
from uuid import uuid4


HTTP_STATUS_CODES = {
    400: 10400,
    401: 10401,
    403: 10402,
    404: 10404,
    405: 10405,
    409: 10409,
    422: 10422,
    429: 10429,
    500: 10500,
    501: 10501,
    502: 10502,
    503: 10503,
    504: 10504,
}


def _normalize_data(data: Any) -> Any:
    if data is None:
        return None
    if isinstance(data, list):
        total = len(data)
        page_size = total or 20
        return {
            "list": data,
            "total": total,
            "page": 1,
            "page_size": page_size,
            "total_pages": ceil(total / page_size) if total else 0,
        }
    return data


def code_for_status(status_code: int) -> int:
    return HTTP_STATUS_CODES.get(status_code, 10500 if status_code >= 500 else 10400)


def success(
    data: Any = None,
    msg: str = "操作成功",
    *,
    code: int = 0,
    status_code: int = 200,
) -> dict[str, Any]:
    return {
        "code": code,
        "msg": msg,
        "data": _normalize_data(data),
        "status_code": status_code,
        "success": True,
        "traceId": str(uuid4()),
    }


def failure(
    code: int,
    msg: str,
    data: Any = None,
    *,
    status_code: int | None = None,
) -> dict[str, Any]:
    response_status_code = status_code
    if code in HTTP_STATUS_CODES and (response_status_code is None or code == response_status_code):
        response_status_code = code
        code = code_for_status(code)
    elif response_status_code is None:
        response_status_code = 200 if code < 50000 else 500
    return {
        "code": code,
        "msg": msg,
        "data": _normalize_data(data),
        "status_code": response_status_code,
        "success": False,
        "traceId": str(uuid4()),
    }
