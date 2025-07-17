import re
from typing import Self

from .constants import ABBREV2LANG, LANGUAGE_ABBREVS
from .utils import RowID

# ROW_INFO_REGEX: re.Pattern = re.compile(r"^(?P<main>\d+)\.?(?P<sub>\d*)
#         \.?(?P<subsub>\d*) +(?P<text>.+)$")
# section_regex_raw: str = (
#     r" *\n*((?P<note>.+?)\n\n)?"
#     r"(> Snippet:\n\n```(?P<lang>[a-z]+)\n(?P<snippet>.+?)\n```\n\n)?"
#     r"(> Output:\n\n```txt\n(?P<snippet_output>.+?)\n```\n\n)?"
#     r"(> Full:\n\n```(?P<lang2>[a-z]+)\n(?P<full>.+?)\n```\n\n)"
#     r"(> Output:\n\n```txt\n(?P<full_output>.+?)\n```)?"
# )
# SECTION_BODY_REGEX: re.Pattern = re.compile(r"^\n*" + section_regex_raw, re.DOTALL)
# SECTION_FULL_REGEX: re.Pattern = re.compile(
#     r"^(?P<octothorpes>#+) +"
#     r"(?P<number>[\d\.]+) +"
#     r"(?P<title>[^\n]+)\n+"
#     f"{section_regex_raw}",
#     re.DOTALL
# )
# SECTION_TITLE_REGEX = re.compile(
#     r"\n(?P<octothorpes>#+) +"
#     r"(?P<number>[\d\.]+) +"
#     r"(?P<title>[^\n]+)\n+"
# )
SECTION_REGEX: re.Pattern = re.compile(
    r"\n(?P<octothorpes>#+) +"
    r"((?P<id0>\d+)\.)((?P<id1>\d+)\.)?((?P<id2>\d+)\.)? +"
    r"(?P<title>[^\n]+)"
    r"\n(\n*(?P<note>[^\n#].+?)\n\n)?"
    r"(\n*> Snippet:\n\n```(?P<lang>[a-z]+)\n(?P<snippet>.*?)\n```\n\n)?"
    r"(\n*> Output:\n\n```txt\n(?P<snippet_output>.*?)\n```\n\n)?"
    r"(\n*> Full:\n\n```(?P<lang_full>[a-z]+)\n(?P<full_code>.*?)\n```\n\n)?"
    r"(\n*> Output:\n\n```txt\n(?P<full_output>.*?)\n```)?",
    re.DOTALL,
)


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
        row: RowID,
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
        return self.row.text

    def __str__(self):
        return (
            f"Illustration: {self.language} <> {self.name} ({self.row})\n"
            f"\n\n> {self.note}"
            f"\n\nSnippet:"
            f"\n\n```\n{LANGUAGE_ABBREVS[self.language]}\n```{self.snippet}\n```"
            f"\n\nOutput:"
            f"\n\n```\ntxt\n```{self.output}\n```"
            f"\n\nFull"
            f"\n\n```\n{LANGUAGE_ABBREVS[self.language]}\n```{self.snippet}\n```"
            f"\n\nOutput:"
            f"\n\n```\ntxt\n```{self.output}\n```"
        )

    def __repr__(self):
        return str(self).replace("\n", "\n    ")

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
        combination = (
            note is not None,
            snippet is not None,
            snippet_output is not None,
            full_code is not None,
            full_output is not None,
        )
        valid_combinations = {
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
                f"Invalid combination:{note=}{snippet=}{snippet_output=}{full_code=}{full_output=}"
            )
        if lang != lang_full:
            raise ValueError(f"Language mismatch: {lang=}, {lang_full=}")

        return cls(
            row=row_id,
            note=(note or ""),
            snippet=(snippet or ""),
            snippet_output=(snippet_output or ""),
            full=(full_code or ""),
            full_output=(full_output or ""),
            language=ABBREV2LANG[lang] if lang else "unknown",
        )


def split_file(raw_md: str) -> list[str]:
    """
    Splits the raw markdown file into sections based on the octothorpes.
    """
    return re.split(r"\n(?=#)", raw_md.strip())


def parse_file(raw_md_block: str) -> list[RowID | Illustration]:
    """
    Parses the raw markdown file and returns a list of Illustration objects.
    """
    sections: list[RowID | Illustration] = []
    result = re.search(SECTION_REGEX, "\n" + raw_md_block)
    if not result:
        raise ValueError(f"Invalid block:\n{raw_md_block}")
    groups = result.groupdict()
    if not groups["snippet"]:
        row = RowID(
            main=int(groups["id0"]),
            sub=int(groups["id1"]) if groups["id1"] else None,
            subsub=int(groups["id2"]) if groups["id2"] else None,
            text=groups["title"],
            octothorpes=groups["octothorpes"],
        )
        sections.append(row)
    else:
        illustration = Illustration.from_dict(**groups)
    sections.append(illustration)
    return sections
