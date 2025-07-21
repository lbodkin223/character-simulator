"""Input parser for the interactive story simulator."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedInput:
    """Structured representation of user input."""
    text: str
    intent: str
    emotion: Optional[str] = None
    tone: Optional[str] = None
    target: Optional[str] = None


def parse_input(text: str) -> ParsedInput:
    """Very naive natural language parser.

    This function uses simple keyword heuristics to determine the user's
    intent, emotion, tone, and target. In a full implementation this would
    be replaced with a call to a more sophisticated NLP model.
    """
    lowered = text.lower()

    # Determine intent
    if "?" in text:
        intent = "question"
    elif any(word in lowered for word in ["love", "like", "adore"]):
        intent = "affection"
    elif any(word in lowered for word in ["hate", "dislike"]):
        intent = "hostile"
    else:
        intent = "statement"

    # Determine emotion
    if any(word in lowered for word in ["angry", "mad", "furious"]):
        emotion = "angry"
    elif any(word in lowered for word in ["happy", "glad", "joy"]):
        emotion = "happy"
    else:
        emotion = None

    # Determine tone (very simplistic)
    if any(word in lowered for word in ["please", "kindly"]):
        tone = "polite"
    elif any(word in lowered for word in ["now", "immediately"]):
        tone = "demanding"
    else:
        tone = None

    # Determine target of interaction (not implemented)
    target = None

    return ParsedInput(text=text, intent=intent, emotion=emotion, tone=tone, target=target)
