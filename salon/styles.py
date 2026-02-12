STYLES = {
    # Haircuts
    "haircut": 20,
    "buzz cut": 15,
    "crew cut": 18,
    "fade": 25,
    "undercut": 22,
    "bob": 28,
    "pixie": 30,
    "layered haircut": 35,
    "quiff": 30,

    # Other services
    "hair coloring": 50,
    "manicure": 15,
    "pedicure": 18,
    "facial": 30
}

def list_styles():
    return "\n".join([f"{style.title()}: ${cost}" for style, cost in STYLES.items()])

# Map common user inputs and synonyms to canonical style keys
ALIASES = {
    "cut": "haircut",
    "hair cut": "haircut",
    "buzzcut": "buzz cut",
    "crewcut": "crew cut",
    "fade haircut": "fade",
    "under cut": "undercut",
    "bob cut": "bob",
    "pixie cut": "pixie",
    "layers": "layered haircut",
    "layered": "layered haircut",
    "color": "hair coloring",
    "colour": "hair coloring",
    "hair color": "hair coloring",
    "hair colouring": "hair coloring",
}

def _normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())

def match_style(user_input: str) -> str | None:
    """Return the canonical style key for a user input.
    - Case-insensitive exact match
    - Alias mapping for common synonyms
    - Simple close match fallback
    """
    import difflib

    s = _normalize(user_input)
    if s in STYLES:
        return s
    if s in ALIASES:
        return ALIASES[s]
    # Fallback to close match among known styles
    candidates = list(STYLES.keys())
    close = difflib.get_close_matches(s, candidates, n=1, cutoff=0.7)
    if close:
        return close[0]
    return None
