from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    __table_args__ = (
        UniqueConstraint(
            "challenge_id",
            "question_order",
            name="uq_question_challenge_order",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    challenge_id = Column(
        Integer,
        ForeignKey("challenges.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_text = Column(Text, nullable=False)

    question_type = Column(
        String(50),
        nullable=False,
        default="multiple_choice",
    )

    question_order = Column(
        Integer,
        nullable=False,
    )

    explanation = Column(Text)

    xp_reward = Column(
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

    challenge = relationship(
        "Challenge",
        back_populates="questions",
    )
