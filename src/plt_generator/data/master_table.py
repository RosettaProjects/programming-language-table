from pathlib import Path

# from ..sync import sync_bidirectional
from ..validation import validate_view_objects
from . import FeatView, LangView
from .illustration import Illustration
from .utils import RowID
from .utils.language import ProgLang


class MasterTable:
    """
    Data structure containing both FeatView and LangView and a composite
      'neutral' view obtained by combining both. Serves both to sync the two
      views and to prepare the data for html generation.
    """

    def __init__(self, featview: FeatView, langview: LangView) -> None:
        self.featview = featview
        self.langview = langview
        self.composite = self.build_master_table(self.featview, self.langview)
        self._rows: list[str]
        self._langs: list[str]

    @property
    def rows(self) -> list[RowID | Illustration]:
        """
        Returns a list of rows, which are either RowID or Illustration objects.
        """
        return []

    @property
    def languages(self) -> list[ProgLang]:
        return []

    # def sync(self) -> None:
    #     self.featview, self.langview = sync_bidirectional(self.featview, self.langview)

    def validate(self) -> None:
        validate_view_objects(self.featview, self.langview)

    def build_master_table(
        self, featview: FeatView, langview: LangView
    ) -> dict[tuple[RowID, ProgLang], Illustration | None]:
        composite: dict[tuple[RowID, ProgLang], Illustration | None] = {}
        return composite

    def write_featview(self, path: Path) -> None:
        """
        Writes the featview to the specified path.
        """
        self.featview.write(path)

    def write_langview(self, path: Path) -> None:
        """
        Writes the langview to the specified path.
        """
        self.langview.write(path)
