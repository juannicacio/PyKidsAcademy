from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Level(Base):
    __tablename__ = "levels"

    __table_args__ = (
        UniqueConstraint(
            "game_id",
            "level_number",
            name="uq_level_game_number",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    game_id = Column(
        Integer,
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(
        String(150),
        nullable=False,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    level_number = Column(
        Integer,
        nullable=False,
    )

    xp_reward = Column(
        Integer,
        nullable=False,
        default=10,
    )

    coin_reward = Column(
        Integer,
        nullable=False,
        default=5,
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

    game = relationship(
        "Game",
        back_populates="levels",
    )

    challenges = relationship(
        "Challenge",
        back_populates="level",
        cascade="all, delete-orphan",
    )
