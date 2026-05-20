"""
gemini.py  –  LLM Outfit Description helper
Calls Gemini 1.5 Flash (free tier) to generate a short, stylish
natural-language description of the scanned clothing item.

Set GEMINI_API_KEY in a .env file next to this project or as an env var.
If the key is missing or the call fails the function returns None and the
app continues normally without a description.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional; key can still be set as plain env var

_client_initialized = False
_model = None


def _init_client():
    global _client_initialized, _model
    if _client_initialized:
        return
    _client_initialized = True
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return  # leave _model as None – caller will skip gracefully
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature": 0.85,
                "max_output_tokens": 120,
            },
        )
    except Exception:
        _model = None


def generate_outfit_description(
    label: str,
    category: str,
    color: str,
    style: str,
    season: str,
    material: str,
) -> str | None:
    """
    Returns a 2-3 sentence stylish outfit description, or None on failure.
    Example output:
      "A crisp navy blue shirt in breathable cotton — a timeless wardrobe
       staple that transitions effortlessly from the office to a dinner out.
       Pair it with chinos and loafers for a polished smart-casual look."
    """
    _init_client()
    if _model is None:
        return None

    prompt = (
        f"You are a professional fashion stylist. "
        f"Write a 2-3 sentence stylish and inspiring description of this clothing item. "
        f"Be specific about the item and suggest a real outfit pairing. "
        f"Do NOT use bullet points or headers — just flowing, natural prose.\n\n"
        f"Item details:\n"
        f"- Type: {label} ({category})\n"
        f"- Color: {color}\n"
        f"- Style: {style}\n"
        f"- Season: {season}\n"
        f"- Material: {material}\n"
    )

    try:
        response = _model.generate_content(prompt)
        text = response.text.strip() if response.text else None
        return text if text else None
    except Exception:
        return None
