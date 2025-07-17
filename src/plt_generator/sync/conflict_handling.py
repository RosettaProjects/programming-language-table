from collections import Counter
from collections.abc import Iterable
from difflib import SequenceMatcher


def titles_match(titles1: Iterable[str], titles2: Iterable[str]) -> bool:
    """
    Given two sequences of (sub-)sections, check whether they match.
    """
    match: bool = False  # TODO

    return match


def ensemble_vote(titles: Iterable[str]) -> str:
    """
    Determine which version of titles is in the majority, if any.
      If no single list dominates, then each of the titles
      found in a (simple) majority of the sequences is returned.
      If no items are found in a majority of the sequences,
      an error is raised.
    """
    counts = Counter(titles)
    most_common = counts.most_common(1)[0][0]
    return most_common


def get_matching_titles(titles1: Iterable[str], titles2: Iterable[str]) -> tuple[str, ...]:
    """
    As a first step in the alignment process, find the titles that match perfectly.
    """
    titles1, titles2 = list(titles1), list(titles2)
    matches = SequenceMatcher(a=titles1, b=titles2).get_matching_blocks()
    return tuple(map(lambda m: titles1[m.a], filter(lambda x: x.size == 1, matches)))


def align_titles(titles1: Iterable[str], titles2: Iterable[str]) -> tuple[list[str], list[str]]:
    """
    Given two sequences of titles that do not match, align the titles to their closest matches,
      using fuzzy string matching. Log all operations that are not entirely obvious
      (e.g. where edit distance > 1), to
      allow for manual editing.
    """
    ...  # https://docs.python.org/3/library/difflib.html
    # https://github.com/gitpython-developers/GitPython/blob/main/git/diff.py
    # https://github.com/kloper/git-difftool -> old, but maybe re-implement
    # https://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970
    return [], []


def insert_new(
    alignment: list[tuple[int, int]], titles1: list[str], titles2: list[str]
) -> list[str]:
    """
    Given an alignment and two lists of titles, add the titles missing from each,
        such that the lists match.
    """
    _idx0, _idx1 = 0, 0
    titles: list[str] = []
    for i, j in alignment:
        ...

    return titles
