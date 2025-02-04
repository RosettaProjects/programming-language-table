from pathlib import Path

import markdown_to_json

from .utils import Illustration, Language, Row

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
    ...


class LangView:
    """
    Parsed contents of `markdown_feat_view` folder.
    """

    def __init__(self) -> None:
        self._rows: dict[Language, SingleLanguage]
        self.languages = list[Language]

    @classmethod
    def from_directory(cls, langview_root: Path, lang_name: str) -> "LangView":
        with open(langview_root, encoding="utf-8") as f:
            raw_dict = markdown_to_json.dictify(f.read())

        return cls("")

    def __getitem__(self, row_id: Row) -> dict[Language, Illustration]:
        return self._rows[row_id]
    
    def lookup(self, row_id: Row, lang_id: Language) -> Illustration:
        return self._rows[row_id][lang_id]
