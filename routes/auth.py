from datetime import timedelta
from typing import Any

from fastapi import (  # type: ignore[import-not-found]
    APIRouter,
    Depends,
    Form,
    HTMLResponse,
    HTTPException,
    RedirectResponse,
    Request,
    status,
)
from fastapi.templating import Jinja2Templates  # type: ignore[import-not-found]
from app.config import settings
from app.database import get_db
from app.dependencies import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.db_models import User  # type: ignore[import-not-found]
from app.models.schemas import UserCreate  # type: ignore[import-not-found]


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
        },
    )


@router.post("/register")
def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Any = Depends(get_db),
):
    try:
        user_data = UserCreate(
            email=email,
            password=password,
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": str(exc),
            },
            status_code=400,
        )

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "An account with this email already exists.",
            },
            status_code=400,
        )

    user = User(
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        },
        timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    response = RedirectResponse(
        "/dashboard",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
    )

    return response


@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        },
    )


@router.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Any = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(
            User.email == email.strip().lower()
        )
        .first()
    )

    if not user or not verify_password(
        password,
        user.password_hash,
    ):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid email or password.",
            },
            status_code=401,
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    response = RedirectResponse(
        "/dashboard",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
    )

    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(
        "/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    response.delete_cookie("access_token")

    return response


@router.post("/token")
def token(
    email: str = Form(...),
    password: str = Form(...),
    db: Any = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(
            User.email == email.strip().lower()
        )
        .first()
    )

    if not user or not verify_password(
        password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }