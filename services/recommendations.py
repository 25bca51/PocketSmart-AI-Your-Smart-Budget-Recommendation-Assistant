from typing import Optional

from .gemini_utils import (
    _build_home_prompt,
    _build_party_prompt,
    _build_jewelry_prompt,
    generate_gemini_response,
)

from .platforms import (
    filter_by_budget,
    get_platform_catalog,
)


def _normalize_ai_result(
    result: dict,
    planner_type: str,
    budget: float,
) -> dict:

    recommendations = result.get(
        "recommendations",
        [],
    )

    normalized = []

    for item in recommendations:
        normalized.append(
            {
                "name": item.get(
                    "name",
                    "Recommended option",
                ),
                "category": item.get(
                    "category",
                    "General",
                ),
                "platform": item.get(
                    "platform",
                    "AI suggestion",
                ),
                "estimated_price": float(
                    item.get(
                        "estimated_price",
                        0,
                    )
                    or 0
                ),
                "reason": item.get(
                    "reason",
                    "Matches the requested criteria.",
                ),
                "url": item.get("url"),
            }
        )

    return {
        "planner_type": planner_type,
        "budget": budget,
        "summary": result.get(
            "summary",
            "AI-generated recommendations.",
        ),
        "allocations": result.get(
            "allocations",
            {},
        ),
        "recommendations": normalized,
        "ai_generated": True,
        "notes": result.get(
            "notes",
            [],
        ),
    }


def _fallback_home(data: dict) -> dict:
    budget = data["budget"]

    allocations = {
        "Furniture": round(budget * 0.40, 2),
        "Lighting": round(budget * 0.20, 2),
        "Decor": round(budget * 0.20, 2),
        "Storage": round(budget * 0.20, 2),
    }

    products = filter_by_budget(
        get_platform_catalog("home"),
        budget,
    )

    recommendations = []

    for product in products[:6]:
        recommendations.append(
            {
                "name": product["name"],
                "category": product["category"],
                "platform": product["platform"],
                "estimated_price": product["price"],
                "reason": (
                    f"Fits a {data['style']} style and "
                    "the requested budget."
                ),
                "url": product["url"],
            }
        )

    return {
        "planner_type": "home",
        "budget": budget,
        "summary": (
            "A budget-conscious home interior plan "
            "was generated using the selected rooms, "
            "style, and requested items."
        ),
        "allocations": allocations,
        "recommendations": recommendations,
        "ai_generated": False,
        "notes": [
            "These are simulated catalog recommendations.",
            "Prices are estimates and should be verified "
            "before purchasing.",
        ],
    }


def _fallback_party(data: dict) -> dict:
    budget = data["budget"]

    allocations = {
        "Catering": round(budget * 0.45, 2),
        "Venue": round(budget * 0.20, 2),
        "Decoration": round(budget * 0.20, 2),
        "Entertainment": round(budget * 0.15, 2),
    }

    products = filter_by_budget(
        get_platform_catalog("party"),
        budget,
    )

    recommendations = []

    for product in products:
        recommendations.append(
            {
                "name": product["name"],
                "category": product["category"],
                "platform": product["platform"],
                "estimated_price": product["price"],
                "reason": (
                    f"Suitable for a {data['event_type']} "
                    f"event with approximately "
                    f"{data['guests']} guests."
                ),
                "url": product["url"],
            }
        )

    return {
        "planner_type": "party",
        "budget": budget,
        "summary": (
            f"A {data['event_type']} budget plan was "
            f"created for {data['guests']} guests."
        ),
        "allocations": allocations,
        "recommendations": recommendations,
        "ai_generated": False,
        "notes": [
            "Vendor information is simulated.",
            "Confirm current pricing and availability "
            "with the vendor."
        ],
    }


def _fallback_jewelry(data: dict) -> dict:
    budget = data["budget"]

    allocations = {
        "Necklace": round(budget * 0.45, 2),
        "Earrings": round(budget * 0.30, 2),
        "Bracelet": round(budget * 0.25, 2),
    }

    products = filter_by_budget(
        get_platform_catalog("jewelry"),
        budget,
    )

    recommendations = []

    for product in products:
        recommendations.append(
            {
                "name": product["name"],
                "category": product["category"],
                "platform": product["platform"],
                "estimated_price": product["price"],
                "reason": (
                    f"Selected as a {data['style']} option "
                    f"for a {data['occasion']} occasion."
                ),
                "url": product["url"],
            }
        )

    return {
        "planner_type": "jewelry",
        "budget": budget,
        "summary": (
            "A jewelry shortlist was created according "
            "to the occasion, style, and budget."
        ),
        "allocations": allocations,
        "recommendations": recommendations,
        "ai_generated": False,
        "notes": [
            "If an outfit image was supplied, Gemini can "
            "provide additional visual matching when configured.",
            "Marketplace prices are simulated estimates.",
        ],
    }


def generate_home(data: dict) -> dict:
    result = generate_gemini_response(
        _build_home_prompt(data)
    )

    if result:
        return _normalize_ai_result(
            result,
            "home",
            data["budget"],
        )

    return _fallback_home(data)


def generate_party(data: dict) -> dict:
    result = generate_gemini_response(
        _build_party_prompt(data)
    )

    if result:
        return _normalize_ai_result(
            result,
            "party",
            data["budget"],
        )

    return _fallback_party(data)


def generate_jewelry(
    data: dict,
    image_bytes: Optional[bytes] = None,
    image_mime_type: Optional[str] = None,
) -> dict:

    result = generate_gemini_response(
        _build_jewelry_prompt(
            data,
            image_bytes is not None,
        ),
        image_bytes=image_bytes,
        image_mime_type=image_mime_type,
    )

    if result:
        return _normalize_ai_result(
            result,
            "jewelry",
            data["budget"],
        )

    return _fallback_jewelry(data)