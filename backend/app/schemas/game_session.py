from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GameSessionBase(BaseModel):
    student_id: int
    game_id: int
    level_id: int


class GameSessionCreate(GameSessionBase):
    pass


class GameSessionUpdate(BaseModel):
    score: int
    correct_answers: int
    wrong_answers: int
    xp_earned: int
    coins_earned: int
    completed: bool = True


class GameSessionResponse(GameSessionBase):
    id: int
    started_at: datetime
    finished_at: datetime | None
    score: int
    correct_answers: int
    wrong_answers: int
    xp_earned: int
    coins_earned: int
    completed: bool

    model_config = ConfigDict(from_attributes=True)
