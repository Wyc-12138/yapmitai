from pydantic import BaseModel, Field, HttpUrl, model_validator


class ModelConfigCreate(BaseModel):
    provider_code: str = Field(min_length=2, max_length=50)
    provider_name: str = Field(min_length=2, max_length=100)
    model_code: str = Field(min_length=2, max_length=100)
    display_name: str = Field(min_length=2, max_length=100)
    model_type: str = Field(pattern="^(chat|embedding)$")
    api_base_url: HttpUrl
    api_key: str = Field(default="", max_length=3000)
    dimension: int | None = Field(default=None, ge=1)
    max_input_tokens: int | None = Field(default=None, ge=1)
    context_window_tokens: int | None = Field(default=None, ge=1)
    max_output_tokens: int | None = Field(default=None, ge=1)
    default_temperature: float | None = Field(default=None, ge=0, le=2)
    enabled: bool = True
    is_default: bool = False
    remark: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_type_fields(self):
        if self.model_type == "embedding" and (
            self.dimension is None or self.max_input_tokens is None
        ):
            raise ValueError("Embedding 模型必须填写 dimension 和 max_input_tokens")
        if self.model_type == "chat" and (
            self.context_window_tokens is None or self.max_output_tokens is None
        ):
            raise ValueError(
                "Chat 模型必须填写 context_window_tokens 和 max_output_tokens"
            )
        return self


class ModelConfigUpdate(BaseModel):
    provider_code: str | None = Field(default=None, min_length=2, max_length=50)
    provider_name: str | None = Field(default=None, min_length=2, max_length=100)
    model_code: str | None = Field(default=None, min_length=2, max_length=100)
    display_name: str | None = Field(default=None, min_length=2, max_length=100)
    model_type: str | None = Field(default=None, pattern="^(chat|embedding)$")
    api_base_url: HttpUrl | None = None
    api_key: str | None = Field(default=None, max_length=3000)
    dimension: int | None = Field(default=None, ge=1)
    max_input_tokens: int | None = Field(default=None, ge=1)
    context_window_tokens: int | None = Field(default=None, ge=1)
    max_output_tokens: int | None = Field(default=None, ge=1)
    default_temperature: float | None = Field(default=None, ge=0, le=2)
    enabled: bool | None = None
    is_default: bool | None = None
    remark: str | None = Field(default=None, max_length=1000)
