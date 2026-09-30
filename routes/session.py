import json

# pyright: reportMissingImports=false
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import (
    get_current_active_user,
    get_token_from_request,
)
from app.models.db_models import (
    RecommendationHistory,
    User,
)


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard(
    request: Request,
    current_user: User = Depends(
        get_current_active_user
    ),
    db: Session = Depends(get_db),
):
    recent = (
        db.query(RecommendationHistory)
        .filter(
            RecommendationHistory.user_id
            == current_user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "recent": recent,
        },
    )


@router.get("/session-info")
def session_info(
    current_user: User = Depends(
        get_current_active_user
    ),
):
    return {
        "logged_in": True,
        "user_id": current_user.id,
        "email": current_user.email,
    }


@router.get("/session-data")
def session_data(
    current_user: User = Depends(
        get_current_active_user
    ),
    db: Session = Depends(get_db),
):
    count = (
        db.query(RecommendationHistory)
        .filter(
            RecommendationHistory.user_id
            == current_user.id
        )
        .count()
    )

    return {
        "logged_in": True,
        "user_id": current_user.id,
        "email": current_user.email,
        "recommendation_count": count,
    }


@router.get(
    "/history",
    response_class=HTMLResponse,
)
def history_page(
    request: Request,
    current_user: User = Depends(
        get_current_active_user
    ),
    db: Session = Depends(get_db),
):
    history = (
        db.query(RecommendationHistory)
        .filter(
            RecommendationHistory.user_id
            == current_user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .all()
    )

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "user": current_user,
            "history": history,
        },
    )


@router.get("/recommendations-details/{recommendation_id}")
def recommendation_details(
    recommendation_id: int,
    current_user: User = Depends(
        get_current_active_user
    ),
    db: Session = Depends(get_db),
):
    item = (
        db.query(RecommendationHistory)
        .filter(
            RecommendationHistory.id
            == recommendation_id,
            RecommendationHistory.user_id
            == current_user.id,
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found.",
        )

    return {
        "id": item.id,
        "planner_type": item.planner_type,
        "created_at": item.created_at,
        "request": json.loads(
            item.request_data
        ),
        "response": json.loads(
            item.response_data
        ),
    }


@router.get("/api/history")
def history_api(
    current_user: User = Depends(
        get_current_active_user
    ),
    db: Session = Depends(get_db),
):
    history = (
        db.query(RecommendationHistory)
        .filter(
            RecommendationHistory.user_id
            == current_user.id
        )
        .order_by(
            RecommendationHistory.created_at.desc()
        )
        .all()
    )

    return [
        {
            "id": item.id,
            "planner_type": item.planner_type,
            "created_at": item.created_at,
            "request": json.loads(
                item.request_data
            ),
            "response": json.loads(
                item.response_data
            ),
        }
        for item in history
    ]


@router.get("/startup")
def startup_status():
    return {
        "status": "ok",
        "message": "PocketSmart AI is running.",
    }