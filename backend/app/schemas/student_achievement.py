from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudentAchievementBase(BaseModel):
    student_id: int
    achievement_id: int


class StudentAchievementCreate(StudentAchievementBase):
    pass


class StudentAchievementResponse(StudentAchievementBase):
    id: int
    unlocked_at: datetime
    notified: bool

    model_config = ConfigDict(from_attributes=True)
