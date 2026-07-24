from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class QuestionBase(BaseModel):
    challenge_id: int
    question_text: str = Field(..., min_length=1, max_length=5000)
    question_type: str = Field(..., max_length=50)
    question_order: int = Field(..., ge=1)
    explanation: str | None = Field(default=None, max_length=5000)
    xp_reward: int = Field(default=5, ge=0)
    is_active: bool = True


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question_text: str | None = Field(default=None, min_length=1, max_length=5000)
    question_type: str | None = Field(default=None, max_length=50)
    question_order: int | None = Field(default=None, ge=1)
    explanation: str | None = Field(default=None, max_length=5000)
    xp_reward: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
