"""Input parser for the interactive story simulator."""
from dataclasses import dataclass
from typing import Optional

try:
    import spacy
except ImportError as e:  # pragma: no cover - guidance for missing dependency
    raise ImportError(
        "spaCy is required for parsing. Install it with 'pip install spacy' and "
        "download the English model via 'python -m spacy download en_core_web_sm'."
    ) from e

try:
    nlp = spacy.load("en_core_web_sm")
except OSError as e:  # pragma: no cover
    raise OSError(
        "spaCy model 'en_core_web_sm' not found. Run 'python -m spacy download en_core_web_sm'"
    ) from e


@dataclass
class ParsedInput:
    """Structured representation of user input."""
    text: str
    intent: str
    emotion: Optional[str] = None
    tone: Optional[str] = None
    target: Optional[str] = None


def parse_input(text: str) -> ParsedInput:
    """Parse user language with spaCy to extract conversation features."""

    doc = nlp(text)
    lemmas = {token.lemma_.lower() for token in doc}

    # Determine intent using simple keyword matching on lemmas
    if "?" in text:
        intent = "question"
    elif lemmas & {"love", "adore", "kiss", "flirt", "date"}:
        intent = "flirt"
    elif lemmas & {"fight", "challenge", "battle", "confront"}:
        intent = "challenge"
    elif lemmas & {"comfort", "hug", "console"}:
        intent = "comfort"
    else:
        intent = "statement"

    # Determine emotion
    if lemmas & {"angry", "mad", "furious"}:
        emotion = "anger"
    elif lemmas & {"happy", "glad", "joy", "excited"}:
        emotion = "joy"
    elif lemmas & {"sad", "upset", "unhappy"}:
        emotion = "sadness"
    else:
        emotion = None

    # Determine tone
    if lemmas & {"sarcastic", "sarcasm"}:
        tone = "sarcastic"
    elif lemmas & {"serious", "solemn"}:
        tone = "serious"
    elif lemmas & {"playful", "tease", "joke"}:
        tone = "playful"
    else:
        tone = None

    # Determine target using named entities
    target = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            target = ent.text
            break

    return ParsedInput(text=text, intent=intent, emotion=emotion, tone=tone, target=target)
