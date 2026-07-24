from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class GameBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    slug: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    category: str = Field(..., max_length=50)
    difficulty: int = Field(default=1, ge=1)
    min_age: int = Field(..., ge=1)
    max_age: int = Field(..., ge=1)
    xp_reward: int = Field(default=10, ge=0)
    coin_reward: int = Field(default=5, ge=0)
    is_active: bool = True


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    slug: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    category: str | None = Field(default=None, max_length=50)
    difficulty: int | None = Field(default=None, ge=1)
    min_age: int | None = Field(default=None, ge=1)
    max_age: int | None = Field(default=None, ge=1)
    xp_reward: int | None = Field(default=None, ge=0)
    coin_reward: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class GameResponse(GameBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
