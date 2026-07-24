from pydantic import BaseModel, ConfigDict


class LeaderboardEntry(BaseModel):
    student_id: int
    first_name: str
    avatar: str | None

    learning_level: int
    xp: int
    coins: int

    model_config = ConfigDict(
        from_attributes=True,
    )
