"""Character response generator for the interactive story simulator."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from parser import ParsedInput


def load_character(path: Path) -> Dict:
    """Load a character profile from a JSON file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_response(character: Dict, parsed: ParsedInput, memory: Dict[str, int]) -> str:
    """Generate a simple in-character response.

    This is a placeholder implementation. A real system might call into an
    LLM or rule-based AI module using the character's persona and the parsed
    input to craft dialogue. Here we simply return canned phrases based on
    intent and relationship stats.
    """
    name = character.get("name", "Unknown")
    persona = "clark" if memory.get("trust", 0) < 7 else "superman"

    base_response = {
        "question": f"{name} ponders your question thoughtfully.",
        "affection": f"{name} smiles warmly at you.",
        "hostile": f"{name} looks taken aback by your hostility.",
        "statement": f"{name} nods in acknowledgement."
    }.get(parsed.intent, f"{name} has no response.")

    # Modify response based on emotion
    if parsed.emotion == "angry":
        base_response += " He seems unsettled by your anger."
    elif parsed.emotion == "happy":
        base_response += " Your good mood is contagious."

    # Personal touch from persona
    persona_desc = character.get("personas", {}).get(persona, {}).get("description", "")
    if persona_desc:
        base_response = f"[{persona.title()}] {base_response}"

    return base_response
