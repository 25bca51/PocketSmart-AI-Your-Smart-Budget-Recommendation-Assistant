from __future__ import annotations

import importlib
from typing import Any


def _load_user_model() -> Any:
    for module_name in ("app_models.db_models", "app.app_models.db_models"):
        try:
            return importlib.import_module(module_name).User
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError(
        "Could not import User from app_models.db_models or app.app_models.db_models"
    )


User = _load_user_model()


async def get_current_active_user() -> Any:
    """
    Placeholder dependency for a real authentication system.

    Replace this with JWT/session-based auth once your auth layer is added.
    """
    return User(
        id=1,
        username="demo_user",
        email="demo@example.com",
        is_active=True,
    )
