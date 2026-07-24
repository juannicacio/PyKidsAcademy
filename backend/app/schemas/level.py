from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LevelBase(BaseModel):
    game_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    level_number: int = Field(..., ge=1)
    xp_reward: int = Field(default=10, ge=0)
    coin_reward: int = Field(default=5, ge=0)
    is_active: bool = True


class LevelCreate(LevelBase):
    pass


class LevelUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    level_number: int | None = Field(default=None, ge=1)
    xp_reward: int | None = Field(default=None, ge=0)
    coin_reward: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class LevelResponse(LevelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
