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


class Challenge(Base):
    __tablename__ = "challenges"

    __table_args__ = (
        UniqueConstraint(
            "level_id",
            "challenge_order",
            name="uq_challenge_level_order",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    level_id = Column(
        Integer,
        ForeignKey("levels.id", ondelete="CASCADE"),
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

    challenge_type = Column(
        String(50),
        nullable=False,
    )

    challenge_order = Column(
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

    level = relationship(
        "Level",
        back_populates="challenges",
    )

    questions = relationship(
        "Question",
        back_populates="challenge",
        cascade="all, delete-orphan",
    )
