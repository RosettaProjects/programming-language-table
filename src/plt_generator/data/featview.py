import re
from itertools import chain
from pathlib import Path
from typing import Self

from ..utils.recency import time_modified_readable
from .md_parsing import parse_feat_file, split_file

from .illustration import Illustration
from .row_id import RowID
from .utils import Language, Row, len_non_none, standardize

FeatWalk = dict[tuple[int, int | None, int | None], tuple[Row, Path, str, str]]


class SingleFeature:
    def __init__(
        self,
        *,
        index: tuple[int, int | None, int | None],
        row: Row,
        name: str,
        path: Path,
        content: dict[Language, Illustration],
        recency: str = "",
    ):
        self.index = index
        self.row = row
        self.name = name
        self.path = path
        self._lang_dict = content
        self.recency = recency

    @property
    def languages(self) -> list[Language]:
        return list(self._lang_dict.keys())

    def __repr__(self) -> str:
        ind = ".".join(map(str, filter(lambda x: x is not None, self.index))) + "."
        # return str(self._lang_dict)
        return (
            "SingleFeature(\n"
            f"        {ind:<10} {self.row:<15} {self.name:<15} (from {self.path})\n"
            f"        last modified: {self.recency or 'NA'}\n"
            f"        languages: {', '.join(self.languages)}\n    )"
        )

    def __getitem__(self, key: Language) -> Illustration:
        return self._lang_dict[key]

    @classmethod
    def from_file(
        cls,
        file_path: Path,
        *,
        index: tuple[int, int | None, int | None],
        row: Row,
    ) -> Self:

        recency = time_modified_readable(file_path)
        lang_dict = parse_feat_file(file_path.read_text())
        print(lang_dict)

        return cls(
            index=index,
            row=row,
            name=row,
            path=file_path,
            content=lang_dict,
            recency=recency,
        )


class FeatView:
    """
    Parsed contents of `markdown_feat_view` folder.
    """

    def __init__(self, row_dict: dict[RowID, SingleFeature]) -> None:
        self._row_dict = row_dict
        self.languages: list[Language] = self.get_languages(row_dict)

    @property
    def rows(self) -> list[RowID]:
        return list(self._row_dict)

    @property
    def cells(self) -> list[tuple]:
        cells = []
        for row, single_feature in self._row_dict.items():
            for lang in single_feature.languages:
                cells.append((lang, row, single_feature.recency))
        return cells

    @property
    def recencies(self) -> dict:
        d = {}
        for lang, row, recency in self.cells:
            d.update({(lang, row): recency})
        return d

    def __repr__(self) -> str:
        return "FeatView:\n    " + "\n    ".join(
            (f"{k!r:<45}\n    ↳ {v!r}" for k, v in self._row_dict.items())
        )

    def __getitem__(self, row_id: RowID) -> SingleFeature:
        return self._row_dict[row_id]

    @classmethod
    def from_directory(cls, featview_root: Path) -> "FeatView":
        _row_dict: dict[RowID, SingleFeature] = {}
        walk = cls.walk_directory(featview_root).items()
        # print("\n".join(map(str, walk)))
        for index, (_row, path, name, typ) in walk:
            row_id = RowID(
                main=index[0],
                sub=index[1],
                subsub=index[2],
                text=_row,
                octothorpes="#" * (len_non_none(index) + 1),
            )
            if typ == "md":
                single_feature = SingleFeature.from_file(
                    path,
                    index=index,
                    row=_row
                )
                
                # SingleFeature(
                #     index=index,
                #     row=_row,
                #     name=re.sub("^#+ ", "", path.read_text().split("\n")[0]),
                #     path=path,
                #     level=len(index),
                # )
            # else:
            #     single_feature = SingleFeature(
            #         index=index,
            #         row=_row,
            #         name=name,
            #         path=path,
            #         level=len(index),
            #     )

                _row_dict.update({row_id: single_feature})
        for k, v in _row_dict.items():
            print(k)
            print(type(v), v)
            print()
        return cls(_row_dict)

    def update_from_diff(self, lv, diff) -> Self:
        for (missing_lang, missing_row), recenct in diff.items():
            print(missing_lang, missing_row, recenct)
            # self.add_from_langview(lv, missing_lang, missing_row, recency) TODO
        return self

    def lookup(self, lang_id: Language, row_id: RowID) -> Illustration:
        return self._row_dict[row_id][lang_id]

    def write(self, featview_root: Path) -> None:
        for row, single_feature in self._row_dict.items():
            path = featview_root / f"{row}.md"
            with path.open("w") as f:
                f.write(str(single_feature))
            print(f"Written {path} with recency {single_feature.recency}")

    @staticmethod
    def walk_directory(
        featview_root: Path,
    ) -> FeatWalk:
        paths: FeatWalk = {}

        for i, directory in enumerate(filter(Path.is_dir, sorted(featview_root.iterdir()))):
            name = (directory / "name.txt").read_text().strip()
            paths.update({(i, None, None): (standardize(name), directory, name, "dir")})

            for j, subdirectory in enumerate(filter(Path.is_dir, sorted(directory.iterdir()))):
                subname = (subdirectory / "name.txt").read_text().strip()
                paths.update({(i, j, None): (standardize(subname), subdirectory, subname, "dir")})

                for k, filename in enumerate(sorted(subdirectory.glob("*.md"))):
                    number, name = filename.name.split("__")
                    number = number.replace("_", ".")
                    paths.update({(i, j, k): (standardize(name), filename, name, "md")})

        return paths

    @staticmethod
    def get_languages(row_dict: dict[RowID, SingleFeature]) -> list[Language]:
        all_languages = list(
            set(chain.from_iterable(map(lambda sf: sf.languages, row_dict.values())))
        )
        return all_languages
