import re
from typing import Self

from .constants import ABBREV2LANG, LANGUAGE_ABBREVS
from .row_id import RowID

"""
Cases:
0) snippet and full are the same (only snippet is given)
1) snippet output and full output exist and differ
1) no snippet output, but full output
2) no full output -> same as snippet output
3) neither has output (should full always have output?)



for result in re.finditer(SECTION_REGEX, "\n" + raw_md):
    for key, value in result.groupdict().items():
        if value is not None:
            print(f"{key}: {value!r}")
    print()
"""


class Illustration:
    """
    Atomic element, containing a single code illustration with optional annotation. Also requires
      the language code, group id number, and feature id number.
    """

    def __init__(
        self,
        *,
        row: RowID | None,
        note: str,
        snippet: str,
        full: str | None,
        snippet_output: str | None,
        full_output: str | None,
        language: str,
    ):
        self.row = row
        self.note = note
        self.snippet = snippet
        self.snippet_output = snippet_output
        self.full = full
        self.full_output = full_output
        self.language = language

    @property
    def name(self) -> str:
        if not self.row:
            return "<NO_NAME>"
        return self.row.text

    def __str__(self):
        return (
            f"Illustration: {self.language} <> {self.name} ({self.row})\n"
            f"\n\n> {self.note}"
            f"\n\nSnippet:"
            f"\n\n```\n{LANGUAGE_ABBREVS[self.language]}\n```{self.snippet}\n```"
            f"\n\nOutput:"
            f"\n\n```\ntxt\n```{self.snippet_output}\n```"
            f"\n\nFull"
            f"\n\n```\n{LANGUAGE_ABBREVS[self.language]}\n```{self.snippet}\n```"
            f"\n\nOutput:"
            f"\n\n```\ntxt\n```{self.full_output}\n```"
        )

    def __repr__(self):
        return str(self).replace("\n", "\n    ")
    
    @classmethod
    def from_dict_rowless(
        cls,
        note: str | None,
        lang: str | None,
        snippet: str | None,
        snippet_output: str | None,
        lang_full: str | None,
        full_code: str | None,
        full_output: str | None,
        **kwargs,
    ) -> Self:

        snippet = snippet or full_code
        full_code = full_code or snippet
        snippet_output = snippet_output or full_output
        full_output = full_output or snippet_output

        cls._check_validity(
            note,
            snippet,
            snippet_output,
            full_code,
            full_output,
            lang,
            lang_full,
        )

        return cls(
            row=None,
            note=(note or ""),
            snippet=(snippet or ""),
            snippet_output=(snippet_output or ""),
            full=(full_code or ""),
            full_output=(full_output or ""),
            language=ABBREV2LANG[lang] if lang else "unknown",
        )

    @classmethod
    def from_dict(
        cls,
        octothorpes: str,
        id0: str | int,
        id1: str | None,
        id2: str | None,
        title: str,
        note: str | None,
        lang: str | None,
        snippet: str | None,
        snippet_output: str | None,
        lang_full: str | None,
        full_code: str | None,
        full_output: str | None,
    ) -> Self:
        row_id = RowID(
            main=int(id0),
            sub=int(id1) if id1 is not None else None,
            subsub=int(id2) if id2 is not None else None,
            text=title,
            octothorpes=octothorpes,
        )
        snippet = snippet or full_code
        full_code = full_code or snippet
        snippet_output = snippet_output or full_output
        full_output = full_output or snippet_output

        cls._check_validity(
            note,
            snippet,
            snippet_output,
            full_code,
            full_output,
            lang,
            lang_full,
        )

        return cls(
            row=row_id,
            note=(note or ""),
            snippet=(snippet or ""),
            snippet_output=(snippet_output or ""),
            full=(full_code or ""),
            full_output=(full_output or ""),
            language=ABBREV2LANG[lang] if lang else "unknown",
        )
    
    @classmethod
    def _check_validity(
        cls,
        note: str | None,
        snippet: str | None,
        snippet_output: str | None,
        full_code: str | None,
        full_output: str | None,
        lang: str | None,
        lang_full: str | None,
    ) -> None:
        combination = (
            note is not None,
            snippet is not None,
            snippet_output is not None,
            full_code is not None,
            bool(full_output),
        )
        valid_combinations = {
            (True, True, True, True, True),
            (True, True, True, True, False),
            (True, True, False, True, True),
            (False, False, False, False, False),  # no content
            (False, True, False, False, False),  # only snippet
            (False, True, True, False, False),  # snippet with output
            (False, True, False, True, False),  # snippet and full code
            (False, True, True, True, True),  # snippet and full code with output
            (False, True, False, True, False),  # snippet and full code with output
            (True, False, False, False, False),  # note, no content
            (True, True, False, False, False),  # note, only snippet
            (True, True, True, False, False),  # note, snippet with output
            (True, True, False, True, False),  # note, snippet and full code
            (True, True, True, True, True),  # note, snippet and full code with output
            (True, True, False, True, False),  # note, snippet and full code with output
        }
        if combination not in valid_combinations:
            raise ValueError(
                f"Invalid combination: {combination}\n  {note=}\n  {snippet=}\n  {snippet_output=}\n  {full_code=}\n  {full_output=}"
            )
        
        if lang != (lang_full or lang):
            raise ValueError(f"Language mismatch: {lang=}, {lang_full=}")
