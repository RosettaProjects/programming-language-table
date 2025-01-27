from typing import Literal, Self
import re


ROW_INFO_REGEX: re.Pattern = re.compile(r"^(?P<main>\d+)\.?(?P<sub>\d*)\.?(?P<subsub>\d*) +(?P<text>.+)$")
SECTION_TEXT_REGEX: re.Pattern = re.compile(
    r"^(?P<level>#+) +"
    r"(?P<number>[\d\.]+) +"
    r"(?P<title>[^\n]+)\n\n"
    r"(> (?P<notes>.+?)\n\n)?"
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
    def formatted(self) -> str:
        return f"{self.main}_{self.sub}_{self.subsub}__{self.text}"

    @property
    def level(self) -> Literal[1, 2, 3]:
        return sum(map(lambda val: int(bool(val)), (self.main, self.sub, self.subsub)))
    


class Illustration:
    """
    Atomic element, containing a single code illustration with optional annotation. Also requires
      the language code, group id number, and feature id number.
    """
    info: RowInfo
    text: str
    code: str
    lang: str
    group_id: int
    feature_id: int
    ...

    @classmethod
    def from_lang(raw_md: str) -> Self:
        ...

    @classmethod
    def from_feat(raw_md: str, row_info: RowInfo) -> Self:
        ...
