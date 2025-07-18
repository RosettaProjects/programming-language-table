import re
from itertools import chain
from pathlib import Path
from typing import Self

from ..utils.recency import time_modified_readable
from ..utils.diff import NestedDict
from .row_id import RowID
from .illustration import Illustration
from .md_parsing import parse_lang_file
from .utils import Language, Row

# class FeatureSubsection:
#     """

#     """
#     def __getitem__(self, __item: int) -> "Illustration":
#         return Illustration()


# class ParsedGroupSection:
#     """
#     Correspond to a level-2 heading (##) in a programming language markdown
#       file under `markdown_lang_view`.
#     """

#     def __getitem__(self, __id: int) -> "Illustration":
#         return Illustration()


# class ParsedLanguageFile:
#     """
#     Corresponds to a single file under `markdown_lang_view`, containing sections
#       and subsectio which correspond, respectively, to feature groups and
#       illustrations of individual features.
#     """

#     def __getitem__(self, __id: int) -> "ParsedGroupSection":
#         return ParsedGroupSection()


class SingleLanguage:
    def __init__(
        self, language: str, raw_md: str, parsed: dict[tuple, RowID | Illustration], recency: str
    ):
        self.language: str = language
        self.raw = raw_md
        self.parsed = parsed
        self.recency = recency

    def __repr__(self):
        return f"rows: {', '.join(map(repr, self.rows))}; last modified {self.recency}"

    # def __getitem__(self, name: str) -> Illustration:
    #     return self.parsed.get(name, "NOT_FOUND")

    @property
    def dictionary(self) -> NestedDict:
        nd: NestedDict = {}
        return nd

    @property
    def rows(self) -> list[RowID]:
        # print(list(self.parsed.values()))[0]
        return [illu.row for illu in self.parsed.values() if isinstance(illu, Illustration)]

    @classmethod
    def from_markdown(cls, md: Path) -> Self:
        raw_md = md.read_text()
        s = re.search(r"(?<=# )[^\n]+", raw_md)
        if not s:
            raise ValueError("Invalid markdown format: missing language name")
        title = s.group(0)
        return cls(
            language=title,
            raw_md=raw_md,
            parsed=parse_lang_file(raw_md),
            recency=time_modified_readable(md),  # Placeholder
        )

    # @classmethod
    # def from_file(cls, p: Path) -> Self:
    #     recency = time_modified_readable(p)
    #     with open(p, encoding="utf-8") as f:
    #         raw_page = f.read()
    #         lang_name = p.name.replace(".md", "")

    #     sections = cls.parse_md(raw_page)

    #     return cls(lang_name, raw_page, sections, recency)

    # @staticmethod
    # def parse_md(raw_md: str) -> dict[str, Illustration]:
    #     # regex = re.compile(r"(?P<section_type>\n####) (?P<number>[\d\.]+)
    #     #     (?P<title>[^\n]+)\n+(?P<main>[^\n]+)", re.DOTALL)
    #     # sections = re.findall(regex, raw_md)
    #     # s = re.search(r"(?<=# )[^\n]+", raw_md)
    #     # if not s:
    #     #     raise ValueError("Invalid markdown format: missing language name")
    #     # language = s.group(0)
    #     # sections = list(
    #     #     map(
    #     #         lambda md: Illustration.from_langview(md, language=language),
    #     #         re.split(r"\n#(?=#{1,3} )", raw_md)[1:],
    #     #     )
    #     # )
    #     # print(sections)
    #     # return {illustr.row: illustr for illustr in sections}
    #     return {}


class LangView:
    """
    Parsed contents of `markdown_lang_view` folder.
    """

    def __init__(self, lang_dict: dict[Language, SingleLanguage]) -> None:
        self._lang_dict: dict[Language, SingleLanguage] = lang_dict
        self.languages: list[Language] = list(lang_dict.keys())

    def __repr__(self) -> str:
        return "LangView:\n    " + "\n    ".join(
            (f"{lang:<15} ::: {lang_item}" for lang, lang_item in self._lang_dict.items())
        )

    @property
    def rows(self) -> list[Language]:
        return self.get_rows(self._lang_dict)

    @property
    def recencies(self) -> dict:
        d = {}
        for lang, row, recency in self.cells:
            d.update({(lang, row): recency})
        return d

    @property
    def cells(self) -> list[tuple]:
        cells = []
        for lang, single_feature in self._lang_dict.items():
            for row in single_feature.rows:
                cells.append((lang, row, single_feature.recency))
        return cells

    @classmethod
    def from_directory(cls, langview_root: Path) -> "LangView":
        lang_dict = {}
        for md_path in langview_root.iterdir():
            single_feature = SingleLanguage.from_markdown(md_path)
            lang_dict.update({single_feature.language: single_feature})
        return cls(lang_dict)

    def __getitem__(self, row_id: Language) -> SingleLanguage:
        return self._lang_dict[row_id]

    def update_from_diff(self, fv, diff) -> Self:
        for (missing_lang, missing_row), recent in diff.items():
            print(missing_lang, missing_row, recent)
            # self.add_from_featview(fv, missing_lang, missing_row, recency) TODO
        return self

    def lookup(self, lang_id: Language, row_id: Row) -> Illustration:
        return self._lang_dict[lang_id][row_id]

    def write(self, langview_root: Path) -> None:
        for lang, single_lang in self._lang_dict.items():
            path = langview_root / f"{lang}.md"
            with path.open("w") as f:
                f.write(str(single_lang))
            print(f"Written {path} with recency {single_lang.recency}")

    @staticmethod
    def get_rows(row_dict: dict[Language, SingleLanguage]) -> list[Language]:
        _all_rows = list(set(chain.from_iterable(map(lambda sf: sf.rows, row_dict.values()))))
        return list(set(chain.from_iterable(_all_rows)))
