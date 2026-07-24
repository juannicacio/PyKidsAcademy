from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    first_name = Column(
        String(100),
        nullable=False,
    )

    birth_month = Column(
        Integer,
        nullable=False,
    )

    birth_year = Column(
        Integer,
        nullable=False,
    )

    avatar = Column(
        String(255),
        nullable=True,
    )

    learning_level = Column(
        Integer,
        nullable=False,
        default=1,
    )

    xp = Column(
        Integer,
        nullable=False,
        default=0,
    )

    coins = Column(
        Integer,
        nullable=False,
        default=0,
    )

    current_game_id = Column(
        Integer,
        ForeignKey("games.id"),
        nullable=True,
    )

    current_level_id = Column(
        Integer,
        ForeignKey("levels.id"),
        nullable=True,
    )

    stars = Column(
        Integer,
        nullable=False,
        default=0,
    )

    completed_levels = Column(
        Integer,
        nullable=False,
        default=0,
    )

    completed_challenges = Column(
        Integer,
        nullable=False,
        default=0,
    )

    longest_streak = Column(
        Integer,
        nullable=False,
        default=0,
    )

    current_streak = Column(
        Integer,
        nullable=False,
        default=0,
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

    user = relationship(
        "User",
        back_populates="students",
    )

    current_game = relationship(
        "Game",
        foreign_keys=[current_game_id],
    )

    current_level = relationship(
        "Level",
        foreign_keys=[current_level_id],
    )

    student_achievements = relationship(
        "StudentAchievement",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    game_sessions = relationship(
        "GameSession",
        back_populates="student",
        cascade="all, delete-orphan",
    )
