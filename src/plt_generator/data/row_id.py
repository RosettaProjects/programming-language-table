from typing import Literal, cast


class RowID:
    def __init__(
        self,
        *,
        main: int,
        sub: int | None,
        subsub: int | None,
        text: str,
        octothorpes: str,
    ) -> None:
        self.main = main
        self.sub = sub
        self.subsub = subsub
        self.text = text
        self.octothorpes = octothorpes

    @property
    def numbers(self) -> tuple[int] | tuple[int, int] | tuple[int, int, int]:
        if self.subsub is not None:
            return (self.main, self.sub, self.subsub)
        elif self.sub is not None:
            return (self.main, self.sub)
        else:
            return self.main

    # @classmethod
    # def from_md(cls, s: str) -> Self:
    #     parsed = re.search(cls.parser, s)
    #     assert parsed
    #     gd = parsed.groupdict()
    #     main = gd["main"]
    #     sub = gd["sub"] or None
    #     subsub = gd["subsub"] or None
    #     text = gd["text"]
    #     return cls(
    #         original=s,
    #         main=main,
    #         sub=sub,
    #         subsub=subsub,
    #         text=text,
    #     )

    def __str__(self) -> str:
        if self.subsub is not None:
            numbers = f"{self.main}.{self.sub}.{self.subsub}."
        elif self.sub is not None:
            numbers = f"{self.main}.{self.sub}."
        else:
            numbers = f"{self.main}."
        return f"{numbers:<8} {self.text}"

    def __repr__(self) -> str:
        return f"RowInfo('{str(self) + "',":<25} level={self.level})"

    def __hash__(self) -> int:
        return hash((self.main, self.sub, self.subsub))

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
        _sum = sum(map(lambda val: int(bool(val)), (self.main, self.sub, self.subsub)))
        return cast(Literal[1, 2, 3], _sum)
