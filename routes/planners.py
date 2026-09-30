import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from fastapi import (  # type: ignore[import-not-found]
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    )
except ImportError as exc:
    raise ImportError(
        "FastAPI is required to load planner routes. Install it with 'pip install fastapi'."
    ) from exc
from typing import Any


# Keep route type annotations usable when SQLAlchemy's optional type stubs are
# unavailable to the editor; the database dependency still supplies sessions
# at runtime.
Session = Any

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_active_user
try:
    from app.models.db_models import RecommendationHistory, User  # type: ignore[import-not-found]
except ImportError as exc:
    raise ImportError(
        "Database models are required to load planner routes."
    ) from exc
try:
    from app.models.schemas import (  # type: ignore[import-not-found]
        HomePlannerRequest,
        PartyPlannerRequest,
    )
except ImportError as exc:
    raise ImportError(
        "Planner schemas are required to load planner routes."
    ) from exc
try:
    from app.services.recommendations import (  # type: ignore[import-not-found]
        generate_home,
        generate_jewelry,
        generate_party,
    )
except ImportError:
    from services.recommendations import (  # type: ignore[import-not-found]
        generate_home,
        generate_jewelry,
        generate_party,
    )


router = APIRouter()


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def save_history(
    db: Session,
    user: User,
    planner_type: str,
    request_data: dict,
    response_data: dict,
):
    history = RecommendationHistory(
        user_id=user.id,
        planner_type=planner_type,
        request_data=json.dumps(
            request_data,
            ensure_ascii=False,
        ),
        response_data=json.dumps(
            response_data,
            ensure_ascii=False,
        ),
    )

    db.add(history)
    db.commit()


@router.post("/generate-home")
def generate_home_endpoint(
    payload: HomePlannerRequest,
    current_user: User = Depends(
        get_current_active_user
    ),
    db: Session = Depends(get_db),
):
    data = payload.model_dump()

    result = generate_home(data)

    save_history(
        db,
        current_user,
        "home",
        data,
        result,
    )

    return result


@router.post("/generate-party")
def generate_party_endpoint(
    payload: PartyPlannerRequest,
    current_user: User = Depends(
        get_current_active_user
    ),
    db: Session = Depends(get_db),
):
    data = payload.model_dump()

    result = generate_party(data)

    save_history(
        db,
        current_user,
        "party",
        data,
        result,
    )

    return result


@router.post("/generate-jewelry")
async def generate_jewelry_endpoint(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_description: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    current_user: User = Depends(
        get_current_active_user
    ),
    db: Session = Depends(get_db),
):
    if budget <= 0:
        raise HTTPException(
            status_code=400,
            detail="Budget must be greater than zero.",
        )

    image_bytes = None
    image_mime_type = None

    if outfit_image:
        if outfit_image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG and WebP images are supported."
                ),
            )

        image_bytes = await outfit_image.read()

        max_bytes = (
            settings.MAX_IMAGE_SIZE_MB
            * 1024
            * 1024
        )

        if len(image_bytes) > max_bytes:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Image must be smaller than "
                    f"{settings.MAX_IMAGE_SIZE_MB} MB."
                ),
            )

        image_mime_type = outfit_image.content_type

    data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "outfit_description": outfit_description,
    }

    result = generate_jewelry(
        data,
        image_bytes=image_bytes,
        image_mime_type=image_mime_type,
    )

    history_data = {
        **data,
        "image_uploaded": image_bytes is not None,
    }

    save_history(
        db,
        current_user,
        "jewelry",
        history_data,
        result,
    )

    return result