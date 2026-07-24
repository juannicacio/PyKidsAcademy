from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class Language(str, Enum):
    en = "en"
    es = "es"


class RegisterRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password",
    )

    country: str = Field(
        min_length=2,
        max_length=2,
        description="ISO country code",
    )

    language: Language = Language.en


class LoginRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class Token(BaseModel):
    access_token: str
    token_type: str
