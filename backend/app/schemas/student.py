from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class StudentCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    first_name: str = Field(
        min_length=2,
        max_length=40,
    )

    birth_month: int = Field(
        ge=1,
        le=12,
    )

    birth_year: int = Field(
        ge=2015,
        le=2035,
    )

    avatar: str | None = Field(
        default=None,
        max_length=50,
    )


class StudentUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=40,
    )

    birth_month: int | None = Field(
        default=None,
        ge=1,
        le=12,
    )

    birth_year: int | None = Field(
        default=None,
        ge=2015,
        le=2035,
    )

    avatar: str | None = Field(
        default=None,
        max_length=50,
    )


class StudentResponse(BaseModel):
    id: int
    user_id: int

    first_name: str

    birth_month: int
    birth_year: int

    avatar: str | None

    learning_level: int
    xp: int
    coins: int

    model_config = ConfigDict(
        from_attributes=True,
    )

class StudentStatsUpdate(BaseModel):
    xp: int
    coins: int
    learning_level: int
