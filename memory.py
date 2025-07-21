"""Relationship memory management for the interactive story simulator."""
import json
from pathlib import Path
from typing import Dict


MEMORY_DIR = Path("logs")


def load_memory(character_name: str) -> Dict[str, int]:
    """Load existing memory for a character or create default stats."""
    MEMORY_DIR.mkdir(exist_ok=True)
    mem_file = MEMORY_DIR / f"{character_name}_memory.json"
    if mem_file.exists():
        with mem_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    # Default stats
    return {"trust": 5, "attraction": 5}


def save_memory(character_name: str, memory: Dict[str, int]) -> None:
    """Persist memory to disk."""
    mem_file = MEMORY_DIR / f"{character_name}_memory.json"
    with mem_file.open("w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


def update_memory(memory: Dict[str, int], parsed: 'ParsedInput') -> None:
    """Adjust relationship stats based on parsed input."""
    # Simple heuristic updates
    if parsed.intent == "affection":
        memory["attraction"] = min(10, memory.get("attraction", 5) + 1)
    if parsed.intent == "hostile":
        memory["trust"] = max(0, memory.get("trust", 5) - 1)
    if parsed.intent == "question" and parsed.emotion == "happy":
        memory["trust"] = min(10, memory.get("trust", 5) + 1)
