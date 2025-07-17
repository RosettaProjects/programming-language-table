from itertools import chain
from pathlib import Path
from typing import Self

from plt_generator.utils.recency import time_modified_readable

from .illustration import Illustration
from .utils import Language, Row, RowID, len_non_none, standardize


class SingleFeature:
    def __init__(
        self,
        *,
        index: tuple[int, int | None, int | None],
        row: Row,
        name: str,
        path: Path,
        level: int,
        content: dict[Language, Illustration] = {},
        recency: str = "",
    ):
        self.index = index
        self.row = row
        self.name = name
        self.path = path
        self._lang_dict = content
        self.recency = recency

    def __repr__(self) -> str:
        ind = ".".join(map(str, self.index))
        return (
            f"{ind:<6} {self.row:<15} {self.name:<15} (from {self.path}),"
            f" last modified: {self.recency or 'NA'}"
        )

    def __getitem__(self, key: Language) -> Illustration:
        return self._lang_dict[key]

    @property
    def languages(self) -> list[Language]:
        return list(self._lang_dict.keys())

    @classmethod
    def from_file(
        cls, path: Path, *, index: tuple[int, int | None, int | None], row: Row, level: int
    ) -> Self:
        content: dict[Language, Illustration] = {}
        raw = path.read_text()
        name = raw.split("\n")[0].replace("# ", "")
        for section in raw.split("\n## ")[1:]:
            language, illustration_raw = section.split("\n", maxsplit=1)
            print(section)
            # TODO
            # content.update(
            #     {
            #         language.lower(): Illustration(
            #             illustration_raw,
            #             row=standardize(name),
            #             name=name,
            #             language=language,
            #             level=level,
            #         )
            #     }
            # )

        recency = time_modified_readable(path)

        return cls(
            index=index,
            row=row,
            name=name,
            level=level,
            path=path,
            content=content,
            recency=recency,
        )


class FeatView:
    """
    Parsed contents of `markdown_feat_view` folder.
    """

    def __init__(self, row_dict: dict[RowID, SingleFeature]) -> None:
        self._row_dict = row_dict
        self.languages: list[Language] = self.get_languages(row_dict)

    def __repr__(self) -> str:
        return "\n".join((f"{k:<20} ::: {v}" for k, v in self._row_dict.items()))

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

    @classmethod
    def from_directory(cls, featview_root: Path) -> "FeatView":
        _row_dict: dict[RowID, SingleFeature] = {}
        for _row, (index, path, name, typ) in cls.walk_directory(featview_root).items():
            row_id = RowID(
                main=index[0],
                sub=index[1],
                subsub=index[2],
                text=_row,
                octothorpes="#" * (len_non_none(index) + 1),
            )
            if typ == "md":
                single_feature = SingleFeature.from_file(
                    index=index, row=_row, path=path, level=len(index)
                )
            else:
                single_feature = SingleFeature(
                    index=index, row=_row, name=name, path=path, level=len(index)
                )

            _row_dict.update({row_id: single_feature})
        return cls(_row_dict)

    def __getitem__(self, row_id: RowID) -> SingleFeature:
        return self._row_dict[row_id]

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
    ) -> dict[Row, tuple[tuple[int, int | None, int | None], Path, str, str]]:
        paths: dict[Row, tuple[tuple[int, int | None, int | None], Path, str, str]] = {}
        for i, directory in enumerate(filter(Path.is_dir, sorted(featview_root.iterdir()))):
            name = (directory / "name.txt").read_text().strip()
            paths.update({standardize(name): ((i, None, None), directory, name, "dir")})
            # paths.update({standardize(name): (directory, name, "dir")})

            for j, subdirectory in enumerate(filter(Path.is_dir, sorted(directory.iterdir()))):
                name = (directory / "name.txt").read_text().strip()
                paths.update({standardize(name): ((i, j, None), subdirectory, name, "dir")})
                # paths.update({standardize(name): (directory, name, "dir")})

                for k, filename in enumerate(sorted(subdirectory.glob("*.md"))):
                    number, name = filename.name.split("__")
                    number = number.replace("_", ".")
                    paths.update({standardize(name): ((i, j, k), filename, name, "md")})
                    # paths.update({standardize(name): (filename, name, "md")})

        return paths

    @staticmethod
    def get_languages(row_dict: dict[RowID, SingleFeature]) -> list[Language]:
        all_languages = list(
            set(chain.from_iterable(map(lambda sf: sf.languages, row_dict.values())))
        )
        return all_languages
