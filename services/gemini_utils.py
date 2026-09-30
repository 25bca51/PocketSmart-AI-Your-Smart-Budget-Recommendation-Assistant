import importlib
import json
import logging
from typing import Optional

from app.config import settings


logger = logging.getLogger(__name__)


def _build_home_prompt(data: dict) -> str:
    return f"""
You are PocketSmart AI, a budget planning assistant.

Create practical home interior recommendations.

User budget:
₹{data["budget"]}

Rooms:
{", ".join(data["rooms"])}

Preferred style:
{data["style"]}

Requested quantities:
{json.dumps(data["items"], indent=2)}

Return ONLY valid JSON in this format:

{{
  "summary": "short summary",
  "allocations": {{
    "Furniture": 0,
    "Lighting": 0,
    "Decor": 0,
    "Storage": 0
  }},
  "recommendations": [
    {{
      "name": "product name",
      "category": "category",
      "estimated_price": 0,
      "reason": "why this fits"
    }}
  ],
  "notes": ["note 1"]
}}

Important:
- Stay within the user's budget.
- Do not invent real-time availability.
- Estimated prices must be reasonable estimates.
- Return valid JSON only.
"""


def _build_party_prompt(data: dict) -> str:
    return f"""
You are PocketSmart AI, an event budget planning assistant.

Create a party/event budget plan.

Budget:
₹{data["budget"]}

Guests:
{data["guests"]}

Event type:
{data["event_type"]}

Venue:
{data["venue"]}

Preferences:
{data.get("preferences", "")}

Return ONLY valid JSON:

{{
  "summary": "short summary",
  "allocations": {{
    "Catering": 0,
    "Venue": 0,
    "Decoration": 0,
    "Entertainment": 0
  }},
  "recommendations": [
    {{
      "name": "option name",
      "category": "category",
      "estimated_price": 0,
      "reason": "why this fits"
    }}
  ],
  "notes": ["note 1"]
}}

Stay within the budget and clearly distinguish estimates from verified prices.
"""


def _build_jewelry_prompt(
    data: dict,
    has_image: bool,
) -> str:
    image_note = (
        "An outfit image has been provided. Consider its visible colors "
        "and overall aesthetic."
        if has_image
        else
        "No outfit image was provided."
    )

    return f"""
You are PocketSmart AI, a jewelry recommendation assistant.

Budget:
₹{data["budget"]}

Occasion:
{data["occasion"]}

Preferred style:
{data["style"]}

Outfit description:
{data.get("outfit_description", "")}

{image_note}

Return ONLY valid JSON:

{{
  "summary": "short summary",
  "allocations": {{
    "Necklace": 0,
    "Earrings": 0,
    "Bracelet": 0
  }},
  "recommendations": [
    {{
      "name": "jewelry option",
      "category": "category",
      "estimated_price": 0,
      "reason": "why it matches"
    }}
  ],
  "notes": ["note 1"]
}}

Stay within the budget.
Do not claim live marketplace availability.
"""


def _parse_json_response(text: str) -> Optional[dict]:
    if not text:
        return None

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def generate_gemini_response(
    prompt: str,
    image_bytes: Optional[bytes] = None,
    image_mime_type: Optional[str] = None,
) -> Optional[dict]:

    if not settings.GEMINI_API_KEY:
        logger.info("Gemini API key not configured.")
        return None

    try:
        genai = importlib.import_module("google.genai")
        types = importlib.import_module("google.genai.types")

        client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        contents = []

        if image_bytes:
            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=image_mime_type or "image/jpeg",
                )
            )

        contents.append(prompt)

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
            ),
        )

        return _parse_json_response(
            response.text
        )

    except Exception as exc:
        logger.exception(
            "Gemini request failed: %s",
            exc,
        )
        return None