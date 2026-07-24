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


class Game(Base):
    __tablename__ = "games"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(150),
        nullable=False,
    )

    slug = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    category = Column(
        String(50),
        nullable=False,
    )

    difficulty = Column(
        Integer,
        nullable=False,
        default=1,
    )

    min_age = Column(
        Integer,
        nullable=False,
    )

    max_age = Column(
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

    levels = relationship(
        "Level",
        back_populates="game",
        cascade="all, delete-orphan",
    )
