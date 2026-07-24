from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        String(30),
        nullable=False,
        default="parent",
    )

    country = Column(
        String(2),
        nullable=True,
    )

    language = Column(
        String(10),
        nullable=False,
        default="en",
    )

    max_students = Column(
        Integer,
        nullable=False,
        default=2,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    last_login = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    students = relationship(
        "Student",
        back_populates="user",
        cascade="all, delete-orphan",
    )
