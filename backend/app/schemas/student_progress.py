from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StudentProgressBase(BaseModel):
    student_id: int = Field(..., gt=0)
    game_id: int = Field(..., gt=0)
    level_id: int = Field(..., gt=0)
    challenge_id: int | None = Field(default=None, gt=0)

    completed: bool = False
    unlocked: bool = False

    stars: int = Field(default=0, ge=0, le=3)
    score: int = Field(default=0, ge=0)
    attempts: int = Field(default=0, ge=0)

    best_time: int | None = Field(default=None, ge=0)


class StudentProgressCreate(StudentProgressBase):
    pass


class StudentProgressUpdate(BaseModel):
    completed: bool | None = None
    unlocked: bool | None = None

    stars: int | None = Field(default=None, ge=0, le=3)
    score: int | None = Field(default=None, ge=0)
    attempts: int | None = Field(default=None, ge=0)

    best_time: int | None = Field(default=None, ge=0)


class StudentProgressResponse(StudentProgressBase):
    id: int

    last_played_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
