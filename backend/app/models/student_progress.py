from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class StudentProgress(Base):
    __tablename__ = "student_progress"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "level_id",
            name="uq_student_level_progress",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    game_id = Column(
        Integer,
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    level_id = Column(
        Integer,
        ForeignKey("levels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    challenge_id = Column(
        Integer,
        ForeignKey("challenges.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    completed = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    unlocked = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    stars = Column(
        Integer,
        nullable=False,
        default=0,
    )

    score = Column(
        Integer,
        nullable=False,
        default=0,
    )

    attempts = Column(
        Integer,
        nullable=False,
        default=0,
    )

    best_time = Column(
        Integer,
        nullable=True,
    )

    last_played_at = Column(
        DateTime(timezone=True),
        nullable=True,
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

    student = relationship(
        "Student",
    )

    game = relationship(
        "Game",
    )

    level = relationship(
        "Level",
    )

    challenge = relationship(
        "Challenge",
    )
