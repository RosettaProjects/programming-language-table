from itertools import chain
from pathlib import Path
from typing import Self

from .utils import Illustration, Language, Row


class SingleFeature:
    def __init__(self, *, row: Row, name: str, path: Path, content: dict[Language, Illustration] = {}):
        self.row = row
        self.name = name
        self.path = path
        self._lang_dict = content

    def __getitem__(self, key: Language) -> Illustration:
            print(self._lang_dict.keys())
            return self._lang_dict[key]

    @property
    def languages(self) -> list[Language]:
        return list(self._lang_dict.values())

    @classmethod
    def from_file(cls, path: Path, *, row: Row, name: str) -> Self:
        content: dict[Language, Illustration] = {}
        for section in path.read_text().split("\n## ")[1:]:
            language, illustration_raw = section.split("\n", maxsplit=1)
            print(section)
            content.update({language.lower(): illustration_raw})

        return cls(
            row=row,
            name=name,
            path=path,
            content=content,
        )


class FeatView:
    """
    Parsed contents of `markdown_feat_view` folder.
    """

    def __init__(self, row_dict: dict[Row, SingleFeature]) -> None:
        self._rows = row_dict
        self._langs: list[Language] = self.get_languages(row_dict)
        

    @classmethod
    def from_directory(cls, featview_root: Path) -> "FeatView":
        _rows = {}
        for row, (path, name, typ) in cls.walk_directory(featview_root).items():
            if typ == "md":
                single_feature = SingleFeature.from_file(row=row, name=name, path=path)
            else:
                single_feature = SingleFeature(row=row, name=name, path=path)
                
                
            _rows.update({row: single_feature})
        return cls(_rows)


    def __getitem__(self, row_id: Row) -> SingleFeature:
        return self._rows[row_id]
    
    def lookup(self, row_id: Row, lang_id: Language) -> Illustration:
        return self._rows[row_id][lang_id]
    
    @staticmethod
    def walk_directory(featview_root: Path) -> dict[Row, tuple[Path, str, str]]:
        paths = {}
        for directory in filter(Path.is_dir, sorted(featview_root.iterdir())):
            name = (directory / "name.txt").read_text().strip()
            paths.update({directory.name.split("__")[0].replace("_", "."): (directory, name, "dir")})
            for directory in filter(Path.is_dir, sorted(directory.iterdir())):
                name = (directory / "name.txt").read_text().strip()
                paths.update({directory.name.split("__")[0].replace("_", "."): (directory, name, "dir")})

                for filename in sorted(directory.glob("*.md")):
                    name = (directory / "name.txt").read_text().strip()
                    paths.update({filename.name.split("__")[0].replace("_", "."): (filename, name, "md")})
        
        return paths
    
    @staticmethod
    def get_languages(row_dict: dict[Row, SingleFeature]) -> list[Language]:
        all_languages = list(set(chain.from_iterable(map(lambda sf: sf.languages, row_dict.values()))))
        return all_languages
