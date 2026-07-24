from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChallengeBase(BaseModel):
    title: str
    description: str | None = None
    challenge_type: str
    challenge_order: int
    xp_reward: int = 10
    coin_reward: int = 5
    is_active: bool = True


class ChallengeCreate(ChallengeBase):
    level_id: int


class ChallengeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    challenge_type: str | None = None
    challenge_order: int | None = None
    xp_reward: int | None = None
    coin_reward: int | None = None
    is_active: bool | None = None


class ChallengeResponse(ChallengeBase):
    id: int
    level_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
