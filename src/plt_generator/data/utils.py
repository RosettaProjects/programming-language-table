import re

type Language = str
type Row = str


def len_non_none(t: tuple) -> int:
    """Count the number of non-None elements in a tuple."""
    return sum(1 for x in t if x is not None)


def standardize(s: str) -> str:
    return re.sub("[^a-z_]", "", s.replace(" ", "_").lower().replace(".md", ""))
