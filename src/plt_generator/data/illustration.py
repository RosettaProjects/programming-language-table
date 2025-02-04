from typing import Literal, Self, TypeAlias
import re

from .constants import LANGUAGE_ABBREVS
from .utils import Language, Row, RowID

ROW_INFO_REGEX: re.Pattern = re.compile(r"^(?P<main>\d+)\.?(?P<sub>\d*)\.?(?P<subsub>\d*) +(?P<text>.+)$")
section_regex_raw: str = (
    r"(> (?P<note>.+?)\n\n)?"
    r"(##### Snippet:\n\n```(?P<lang>[a-z]+)\n(?P<snippet>.+?)\n```\n\n)"
    r"(##### Output:\n\n```txt\n(?P<snippet_output>.+?)\n```\n\n)?"
    r"(##### Full:\n\n```(?P<lang2>[a-z]+)\n(?P<full>.+?)\n```\n\n)?"
    r"(##### Output:\n\n```txt\n(?P<full_output>.+?)\n```)?"
)
SECTION_BODY_REGEX: re.Pattern = re.compile(r"^\n*" + section_regex_raw, re.DOTALL)
SECTION_FULL_REGEX: re.Pattern = re.compile(
    r"^(?P<level>#+) +"
    r"(?P<number>[\d\.]+) +"
    r"(?P<title>[^\n]+)\n+"
    f"{section_regex_raw}",
    re.DOTALL
)
'''
Cases:
0) snippet and full are the same (only snippet is given)
1) snippet output and full output exist and differ
1) no snippet output, but full output
2) no full output -> same as snippet output
3) neither has output (should full always have output?)

'''

class Illustration:
    """
    Atomic element, containing a single code illustration with optional annotation. Also requires
      the language code, group id number, and feature id number.
    """
    def __init__(
        self,
        *,
        row: RowID,
        name: str,
        note: str,
        snippet: str,
        full: str | None,
        snippet_output: str | None,
        full_output: str | None,
        language: str,
    ):
        self.row = row
        self.name = name
        self.note = note
        self.snippet = snippet
        self.snippet_output = snippet_output
        self.full = full
        self.full_output = full_output
        self.language = language

    @classmethod
    def from_langview(cls, raw_md: str) -> Self:
        d = cls._parse_raw(raw_md, SECTION_FULL_REGEX)
        info = RowID()

        return cls(
            info=info,
            name=d["title"],
            note=d["note"],
            snippet=d["snippet"],
            snippet_output=d["snippet_output"],
            full=d["full"],
            full_output=d["full_output"],
            language=d["lang"],
        )

    @classmethod
    def from_featview(cls, raw_md: str, row_info: RowID) -> Self:
        d = cls._parse_raw(raw_md, SECTION_FULL_REGEX)

    @classmethod
    def from_section_body(cls, raw_md: str, *, row: Row, name: str, language: Language) -> Self:
        d = cls._parse_raw(raw_md, SECTION_BODY_REGEX)
        # assert language == LANGUAGE_ABBREVS[d["lang"]]
        return cls(
            row=row,
            name=name,
            language=language,
            note=d["note"],
            snippet=d["snippet"],
            snippet_output=d["snippet_output"],
            full=d["full"],
            full_output=d["full_output"],
            
        )


    def for_lang(self) -> str:
        return "\n\n".join(filter(bool,
            self.info.markdown,
            self.note,
            f"```{self.lang}\n{self.snippet}\n```",
            f"```{self.lang}\n{self.full}\n```",
            f"```txt\n{self.output}\n```",
            "",
        ))

    def for_feat(self) -> str:
        return "\n\n".join(filter(bool,
            f"{'#' * self.level} {LANGUAGE_ABBREVS[self.lang]}",
            self.note,
            f"```{self.lang}\n{self.snippet}\n```",
            f"```{self.lang}\n{self.full}\n```",
            f"```txt\n{self.output}\n```",
            "",
        ))
    
    @staticmethod
    def _parse_raw(raw_md: str, reg: re.Pattern) -> dict[str, str]:
        parsed = re.search(reg, raw_md)
        if not parsed:
            raise ValueError(f"Invalid format: {raw_md}")
        return parsed.groupdict()