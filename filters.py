from config import SKILL_KEYWORDS, SPONSORSHIP_KEYWORDS


def matches_skill(text: str) -> bool:
    text = text.lower()
    return any(kw in text for kw in SKILL_KEYWORDS)


def matches_sponsorship(text: str) -> bool:
    text = text.lower()
    return any(kw in text for kw in SPONSORSHIP_KEYWORDS)


def is_relevant(title: str, description: str = "") -> bool:
    combined = f"{title} {description}"
    return matches_skill(combined) and matches_sponsorship(combined)
