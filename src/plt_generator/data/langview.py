from functools import partial
from itertools import chain
from pathlib import Path
import re
from typing import Self

import markdown_to_json

from plt_generator.utils.recency import time_modified_readable

from .illustration import Illustration
from ..utils.diff import NestedDict, NestedTupleDict
from .utils import Language, Row, standardize

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
    def __init__(self, language: str, raw_md: str, parsed: dict, recency: str):
        self.language: str = language
        self.raw = raw_md
        self.parsed = parsed
        self.recency = recency

    def __repr__(self):
        return f"rows: {', '.join(self.rows)}; last modified {self.recency}"
    
    def __getitem__(self, name: str) -> Illustration:
        return self.parsed.get(name, "NOT_FOUND")

    @property
    def dictionary(self) -> NestedDict: ...

    @property
    def rows(self) -> list[tuple[str, ...]]:
        # print(list(self.parsed.values()))[0]
        return [ill.row for ill in self.parsed.values() if ill.level == 3]

    @classmethod
    def from_markdown(cls, raw_md: str) -> Self:
        return cls(raw_md)
    
    @classmethod
    def from_file(cls, p: Path) -> Self:

        recency = time_modified_readable(p)
        with open(p, encoding="utf-8") as f:
            raw_page = f.read()
            lang_name = p.name.replace(".md", "")

        sections = cls.parse_md(raw_page)
        
        return cls(lang_name, raw_page, sections, recency)
    
    @staticmethod
    def parse_md(raw_md: str) -> dict[str, Illustration]:
        # regex = re.compile(r"(?P<section_type>\n####) (?P<number>[\d\.]+) (?P<title>[^\n]+)\n+(?P<main>[^\n]+)", re.DOTALL)
        # sections = re.findall(regex, raw_md)
        language = re.search(r"(?<=# )[^\n]+", raw_md).group(0)
        sections = list(map(lambda md: Illustration.from_langview(md, language=language), re.split(r"\n#(?=#{1,3} )", raw_md)[1:]))
        print(sections)
        return {illustr.row: illustr for illustr in sections}


class LangView:
    """
    Parsed contents of `markdown_feat_view` folder.
    """

    def __init__(self, lang_dict: dict[Language, SingleLanguage]) -> None:
        self._lang_dict: dict[Language, SingleLanguage] = lang_dict
        self.languages: list[Language] = list(lang_dict.keys())

    def __repr__(self) -> str:
        return "\n".join((f"{lang:<10} ::: {lang_item}" for lang, lang_item in self._lang_dict.items()))

    @property
    def rows(self) -> list[tuple[str, ...]]:
        return self.get_rows(self._lang_dict)
    
    @property
    def recencies(self) -> dict:
        d = {}
        for (lang, row, recency) in self.cells:
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
            single_feature = SingleLanguage.from_file(md_path)
            lang_dict.update({single_feature.language: single_feature})
        return cls(lang_dict)
            
    def __getitem__(self, row_id: Row) -> dict[Language, Illustration]:
        return self._lang_dict[row_id]
    
    def update_from_diff(self, fv, diff) -> Self:
        for (missing_lang, missing_row), recent in diff.items():
            print(missing_lang, missing_row, recent)
            # self.add_from_featview(fv, missing_lang, missing_row, recency) TODO
        return self
    
    def lookup(self, lang_id: Language, row_id: Row) -> Illustration:
        return self._lang_dict[lang_id][row_id]
    
    @staticmethod
    def get_rows(row_dict: dict[Language, SingleLanguage]) -> list[Language]:
        all_rows = list(set(chain.from_iterable(map(lambda sf: sf.rows, row_dict.values()))))
        return all_rows
