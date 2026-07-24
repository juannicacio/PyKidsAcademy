from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AchievementBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=255)
    icon: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    xp_reward: int = Field(default=0, ge=0)
    coin_reward: int = Field(default=0, ge=0)
    active: bool = True


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    slug: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=255)
    icon: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    xp_reward: int | None = Field(default=None, ge=0)
    coin_reward: int | None = Field(default=None, ge=0)
    active: bool | None = None


class AchievementResponse(AchievementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
