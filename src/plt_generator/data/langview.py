from pathlib import Path

import markdown_to_json

from .illustration import Illustration


# class FeatureSubsection:
#     """
    
#     """
#     def __getitem__(self, __item: int) -> "Illustration":
#         return Illustration()

class ParsedGroupSection:
    """
    Correspond to a level-2 heading (##) in a programming language markdown 
      file under `markdown_lang_view`.
    """
    def __getitem__(self, __item: int) -> "Illustration":
        return Illustration()
    
    def __getitem__(self, __id: int) -> "Illustration":
        ...


class ParsedLanguageFile:
    """
    Corresponds to a single file under `markdown_lang_view`, containing sections
      and subsectio which correspond, respectively, to feature groups and
      illustrations of individual features.
    """
    def __getitem__(self, __id: int) -> "ParsedGroupSection":
        return ParsedGroupSection()


class LangView:
    """
    Parsed contents of `markdown_feat_view` folder.
    """
    def __init__(self, lang: str) -> None:
        self.lang = lang
        self.groups: list[ParsedGroupSection] = []

    @classmethod
    def from_file(cls, langview_root: Path, lang_name: str) -> "LangView":
        with open(langview_root, encoding="utf-8") as f:
            raw_dict = markdown_to_json.dictify(f.read())
        
        return cls("")
    
    def __getitem__(self, __item: int) -> ParsedLanguageFile:
        return self.groups[__item]
