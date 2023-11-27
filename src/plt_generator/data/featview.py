from pathlib import Path

import markdown_to_json

from .illustration import Illustration


class ParsedFeatureFile:
    """
    Corresponds to a file in a subdirectory of `markdown_feat_view`. Each file
      contains a single feature illustrated in multiple programming languages.
    """
    def __getitem__(self, __item: int) -> "Illustration":
        return Illustration()

class ParsedGroupFolder:
    """
    Corresponds to a folder inside of `markdown_feat_view`, each of which contains a number of
      semantically related files each containing a single feature illustrated in multiple
      programming languages.
    """
    def __getitem__(self, __item: int) -> "ParsedFeatureFile":
        return ParsedFeatureFile()


class FeatView:
    """
    Parsed contents of `markdown_feat_view` folder.
    """
    def __init__(self, lang: str) -> None:
        self.lang = lang
        self.groups: list[ParsedGroupFolder] = []

    @classmethod
    def from_file(cls, featview_root: Path, feat_name: str) -> "FeatView":
        with open(featview_root, encoding="utf-8") as f:
            raw_dict = markdown_to_json.dictify(f.read())
        
        return cls("")

    def __getitem__(self, __item: int) -> ParsedGroupFolder:
        return self.groups[__item]
