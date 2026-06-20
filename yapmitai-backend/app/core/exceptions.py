class AppError(Exception):
    def __init__(self, code: int, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AgentUnavailableError(AppError):
    def __init__(self, message: str = "Agent unavailable") -> None:
        super().__init__(10503, message, 503)


class InsufficientBalanceError(AppError):
    def __init__(self, message: str = "Insufficient balance") -> None:
        super().__init__(30003, message, 200)


class InvalidParameterError(AppError):
    def __init__(self, message: str = "Invalid parameter") -> None:
        super().__init__(10422, message, 422)


class GatewayTimeoutError(AppError):
    def __init__(self, message: str = "Agent gateway timeout") -> None:
        super().__init__(10504, message, 504)
