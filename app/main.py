from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import uvicorn  # pyright: ignore[reportMissingImports]
from fastapi import Depends, FastAPI, Request  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse, RedirectResponse  # pyright: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates  # pyright: ignore[reportMissingImports]

from app.config import settings
from app.dependencies import get_current_active_user


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"


# ============================================================
# JINJA2 TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ============================================================
# APPLICATION STARTUP / SHUTDOWN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown handler.

    This is where services such as the database or AI client
    can be initialized in the future.
    """

    print("Starting PocketSmart AI...")
    print("Application configuration loaded.")

    yield

    print("Shutting down PocketSmart AI...")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="PocketSmart AI",
    description=(
        "AI-powered budget and recommendation assistant "
        "for home interiors, party planning, and jewelry."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(
        settings,
        "allowed_origins_list",
        ["http://localhost:3000", "http://localhost:8000"],
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT / HEALTH ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Application home page.

    If index.html exists, it is rendered.
    Otherwise a simple API response is returned.
    """

    index_file = TEMPLATES_DIR / "index.html"

    if index_file.exists():
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
            },
        )

    return HTMLResponse(
        content="""
        <html>
            <head>
                <title>PocketSmart AI</title>
            </head>
            <body>
                <h1>Welcome to PocketSmart AI</h1>
                <p>The FastAPI backend is running successfully.</p>
            </body>
        </html>
        """
    )


@app.get("/health")
async def health_check():
    """
    Simple health-check endpoint.
    """
    return {
        "status": "healthy",
        "application": "PocketSmart AI",
        "version": "1.0.0",
    }


# ============================================================
# AUTHENTICATED DASHBOARD
# ============================================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: Any = Depends(get_current_active_user),
):
    """
    Display the authenticated user's dashboard.
    """

    dashboard_file = TEMPLATES_DIR / "dashboard.html"

    if dashboard_file.exists():
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "user": current_user,
            },
        )

    return HTMLResponse(
        content=f"""
        <html>
            <head>
                <title>PocketSmart AI Dashboard</title>
            </head>
            <body>
                <h1>Welcome to PocketSmart AI</h1>
                <p>User ID: {current_user.id}</p>
            </body>
        </html>
        """
    )


# ============================================================
# HOME PLANNER PAGE
# ============================================================

@app.get("/home-planner", response_class=HTMLResponse)
async def home_planner(
    request: Request,
    current_user: Any = Depends(get_current_active_user),
):
    """
    Home Interior Budget Planner page.
    """

    template_file = TEMPLATES_DIR / "home_planner.html"
    if template_file.exists():
        return templates.TemplateResponse(
            "home_planner.html",
            {
                "request": request,
                "user": current_user,
            },
        )

    return HTMLResponse(
        content=f"""
        <html>
            <head><title>Home Planner</title></head>
            <body>
                <h1>Home Planner</h1>
                <p>Welcome, {current_user.username}.</p>
            </body>
        </html>
        """
    )


# ============================================================
# PARTY PLANNER PAGE
# ============================================================

@app.get("/party-planner", response_class=HTMLResponse)
async def party_planner(
    request: Request,
    current_user: Any = Depends(get_current_active_user),
):
    """
    Party Budget Planner page.
    """

    template_file = TEMPLATES_DIR / "party_planner.html"
    if template_file.exists():
        return templates.TemplateResponse(
            "party_planner.html",
            {
                "request": request,
                "user": current_user,
            },
        )

    return HTMLResponse(
        content=f"""
        <html>
            <head><title>Party Planner</title></head>
            <body>
                <h1>Party Planner</h1>
                <p>Welcome, {current_user.username}.</p>
            </body>
        </html>
        """
    )


# ============================================================
# JEWELRY PLANNER PAGE
# ============================================================

@app.get("/jewelry-planner", response_class=HTMLResponse)
async def jewelry_planner(
    request: Request,
    current_user: Any = Depends(get_current_active_user),
):
    """
    Jewelry Budget Planner page.

    The documentation specifies optional outfit-image input
    for the jewelry recommendation workflow.
    """

    template_file = TEMPLATES_DIR / "jewelry_planner.html"
    if template_file.exists():
        return templates.TemplateResponse(
            "jewelry_planner.html",
            {
                "request": request,
                "user": current_user,
            },
        )

    return HTMLResponse(
        content=f"""
        <html>
            <head><title>Jewelry Planner</title></head>
            <body>
                <h1>Jewelry Planner</h1>
                <p>Welcome, {current_user.username}.</p>
            </body>
        </html>
        """
    )


# ============================================================
# REGISTER PAGE
# ============================================================

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Registration page.
    """

    template_file = TEMPLATES_DIR / "register.html"
    if template_file.exists():
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
            },
        )

    return HTMLResponse(
        content="""
        <html>
            <head><title>Register</title></head>
            <body>
                <h1>Create account</h1>
                <p>Registration page is ready.</p>
            </body>
        </html>
        """
    )


# ============================================================
# LOGIN PAGE
# ============================================================

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Login page.
    """

    template_file = TEMPLATES_DIR / "login.html"
    if template_file.exists():
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
            },
        )

    return HTMLResponse(
        content="""
        <html>
            <head><title>Login</title></head>
            <body>
                <h1>Login</h1>
                <p>Please sign in to continue.</p>
            </body>
        </html>
        """
    )


# ============================================================
# LOGOUT
# ============================================================

@app.get("/logout")
async def logout():
    """
    Logout the current browser session by removing
    the access token cookie.
    """

    response = RedirectResponse(
        url="/login",
        status_code=303,
    )

    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
    )

    return response


# ============================================================
# STARTUP INFORMATION
# ============================================================

@app.get("/startup")
async def startup_status():
    """
    Provides application startup/configuration status.
    """

    return {
        "application": "PocketSmart AI",
        "status": "running",
        "environment": getattr(
            settings,
            "ENVIRONMENT",
            "development",
        ),
    }


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=getattr(
            settings,
            "HOST",
            "127.0.0.1",
        ),
        port=int(
            getattr(
                settings,
                "PORT",
                8000,
            )
        ),
        reload=getattr(
            settings,
            "DEBUG",
            True,
        ),
    )