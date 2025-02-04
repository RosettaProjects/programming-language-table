from typing import Literal, Self, TypeAlias
import re

from .constants import LANGUAGE_ABBREVS

Language: TypeAlias = str
Row: TypeAlias = str


class RowID:
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
