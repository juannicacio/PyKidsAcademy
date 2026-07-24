from fastapi import HTTPException


class StudentNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Student not found.",
        )


class StudentLimitReached(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Student limit reached.",
        )
