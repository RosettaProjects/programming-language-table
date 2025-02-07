from . import FeatView, LangView
# from ..sync import sync_bidirectional
from ..validation import validate_view_objects


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
    def rows() -> list[str]:
        ...

    @property
    def languages() -> list[str]:
        ...

    # def sync(self) -> None:
    #     self.featview, self.langview = sync_bidirectional(self.featview, self.langview)

    def validate(self) -> None:
        validate_view_objects(self.featview, self.langview)

    def build_master_table(
        self, featview: FeatView, langview: LangView
    ) -> dict:
        composite = {}
        return composite
