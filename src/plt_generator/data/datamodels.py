from typing import Literal, Self
import re

from .constants import LANGUAGE_ABBREVS

ROW_INFO_REGEX: re.Pattern = re.compile(r"^(?P<main>\d+)\.?(?P<sub>\d*)\.?(?P<subsub>\d*) +(?P<text>.+)$")
SECTION_TEXT_REGEX: re.Pattern = re.compile(
    r"^(?P<level>#+) +"
    r"(?P<number>[\d\.]+) +"
    r"(?P<title>[^\n]+)\n\n"
    r"(> (?P<note>.+?)\n\n)?"
    r"(##### Snippet:\n\n```(?P<lang>[a-z]+)\n(?P<snippet>.+?)\n```\n\n)"
    r"(##### Full:\n\n```(?P<lang2>[a-z]+)\n(?P<full>.+?)\n```\n\n)?"
    r"(##### Output:\n\n```txt\n(?P<output>.+?)\n```)?\n*$",
    re.DOTALL
)


class RowInfo:
    def __init__(
        self,
        *,
        main: int,
        sub: int | None,
        subsub: int | None,
        text: str,
        original: str,
    ) -> None:
        self.main = main
        self.sub = sub
        self.subsub = subsub
        self.text = text
        self.original = original

    @classmethod
    def from_md(cls, s: str) -> Self:
        parsed = re.search(cls.parser, s)
        assert parsed
        gd = parsed.groupdict()
        main = gd["main"]
        sub = gd["sub"] or None
        subsub = gd["subsub"] or None
        text = gd["text"]
        return cls(
            original=s,
            main=main,
            sub=sub,
            subsub=subsub,
            text=text,
        )

    def __str__(self) -> str:
        return f"{self.main}.{self.sub}.{self.subsub} {self.text}"
    
    def __repr__(self) -> str:
        return f"RowInfo('{self.main}.{self.sub}.{self.subsub} {self.text}', level={self.level})"

    @property
    def markdown(self) -> str:
        if self.subsub is not None:
            number = f"{self.main}.{self.sub}.{self.subsub}"
        elif self.sub is not None:
            number = f"{self.main}.{self.sub}"
        else:
            number = str(self.main)
        return f"{'#' * self.level} {number} {self.text}"

    @property
    def formatted(self) -> str:
        return f"{self.main}_{self.sub}_{self.subsub}__{self.text}"

    @property
    def level(self) -> Literal[1, 2, 3]:
        return sum(map(lambda val: int(bool(val)), (self.main, self.sub, self.subsub)))
    


class CellContents:
    """
    Atomic element, containing a single code illustration with optional annotation. Also requires
      the language code, group id number, and feature id number.
    """
    def __init__(
        self,
        *,
        info: RowInfo,
        title: str,
        note: str,
        snippet: str,
        full: str | None,
        output: str | None,
        lang: str,
    ):
        self.info = info
        self.title = title
        self.note = note
        self.snippet = snippet
        self.full = full
        self.output = output
        self.lang = lang

    @classmethod
    def from_lang(cls, raw_md: str) -> Self:
        d = cls._parse_raw(raw_md)
        info = RowInfo()

        return cls(
            info=info,
            title=d["title"],
            note=d["note"],
            snippet=d["snippet"],
            output=d["output"],
            lang=d["lang"],
        )

    @classmethod
    def from_feat(cls, raw_md: str, row_info: RowInfo) -> Self:
        d = cls._parse_raw(raw_md)

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
    def _parse_raw(raw_md) -> dict[str, str]:
        parsed = re.search(SECTION_TEXT_REGEX, raw_md)
        if not parsed:
            raise ValueError(f"Invalid format: {raw_md}")
        return parsed.groupdict()