from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    country: str | None = None
    language: str

    max_students: int

    is_active: bool

    model_config = ConfigDict(from_attributes=True)
