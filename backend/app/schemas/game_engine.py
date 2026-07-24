from pydantic import BaseModel, Field


class CompleteLevelRequest(BaseModel):
    student_id: int = Field(..., gt=0)
    game_id: int = Field(..., gt=0)
    level_id: int = Field(..., gt=0)

    score: int = Field(..., ge=0)
    stars: int = Field(..., ge=0, le=3)
    elapsed_time: int = Field(..., ge=0)


class CompleteLevelResponse(BaseModel):
    xp: int
    coins: int
    learning_level: int

    unlocked_next_level: bool

    completed: bool
