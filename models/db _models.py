from datetime import datetime, timezone

try:
    from sqlalchemy import (  # type: ignore[reportMissingImports]
        Boolean,
        Column,
        DateTime,
        ForeignKey,
        Integer,
        String,
        Text,
    )
    from sqlalchemy.orm import relationship  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover - dependency must be installed in the runtime environment
    from typing import Any

    Boolean = Integer = String = Text = DateTime = ForeignKey = Any
    Column = Any

    def relationship(*args, **kwargs):
        return None

from app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    recommendations = relationship(
        "RecommendationHistory",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    planner_type = Column(
        String(50),
        nullable=False,
    )

    request_data = Column(
        Text,
        nullable=False,
    )

    response_data = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="recommendations",
    )