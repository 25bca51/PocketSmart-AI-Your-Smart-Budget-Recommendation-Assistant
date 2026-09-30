from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field, field_validator  # type: ignore[import-not-found]
except ImportError:
    from pydantic import BaseModel, Field, validator  # type: ignore[import-not-found]

    def field_validator(*fields, **kwargs):
        return validator(*fields, **kwargs)


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        value = value.strip().lower()

        if "@" not in value or "." not in value:
            raise ValueError("Please provide a valid email address.")

        return value


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HomePlannerRequest(BaseModel):
    budget: float = Field(gt=0)
    rooms: List[str] = Field(min_length=1)
    style: str = "Modern"
    items: Dict[str, int] = Field(default_factory=dict)

    @field_validator("rooms")
    @classmethod
    def validate_rooms(cls, value):
        cleaned = [room.strip() for room in value if room.strip()]

        if not cleaned:
            raise ValueError("At least one room is required.")

        return cleaned


class PartyPlannerRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0, le=10000)
    event_type: str = "Birthday"
    venue: str = "Home"
    preferences: Optional[str] = ""


class RecommendationItem(BaseModel):
    name: str
    category: str
    platform: str
    estimated_price: float
    reason: str
    url: Optional[str] = None


class RecommendationResponse(BaseModel):
    planner_type: str
    budget: float
    summary: str
    allocations: Dict[str, float] = Field(default_factory=dict)
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    ai_generated: bool = False
    notes: List[str] = Field(default_factory=list)


class SessionInfo(BaseModel):
    logged_in: bool
    user_id: Optional[int] = None
    email: Optional[str] = None


class SessionData(BaseModel):
    logged_in: bool
    user_id: Optional[int] = None
    email: Optional[str] = None
    recommendation_count: int = 0