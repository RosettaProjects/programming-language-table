"""
Restrictions on syncing:

-

"""

from ..data.featview import FeatView
from ..data.langview import LangView
from ..data.master_table import MasterTable
from ..utils.diff import DiffDict, get_dictionary_diff, get_list_diff
from .bidirectional_sync import sync_bidirectional

if False:
    print(DiffDict)  # TODO
    print(get_dictionary_diff)  # TODO
    print(sync_bidirectional)  # TODO


def get_recent(featview: FeatView, langview: LangView) -> dict:
    fv_recencies = featview.recencies
    lv_recencies = langview.recencies
    updated = {}
    for k, v in fv_recencies.items():
        if k in lv_recencies:
            updated.update({k: "fv" if v > lv_recencies[k] else "lv"})
        else:
            updated.update({k: "fv"})
    for k, v in lv_recencies.items():
        if k not in updated:
            updated.update({k: "lv" if v > lv_recencies[k] else "fv"})
    return updated


def get_missing(featview: FeatView, langview: LangView):
    return get_recent(featview, langview)

    def first_two(tuples: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
        return [t[:2] for t in tuples]

    return get_list_diff(*map(first_two, (featview.cells, langview.cells)))


def aggregate_from_diff(featview: FeatView, langview: LangView, recency: dict) -> MasterTable:
    out = {}
    for key, val in recency.items():
        if val == "fv":
            out.update({key: featview.lookup(*key)})
        else:
            out.update({key: langview.lookup(*key)})
    return MasterTable(featview, langview)  # TODO


# def update_from_diff(featview: FeatView, langview: LangView, diff: DiffDict):
#     featview.update_from_diff(langview, diff)
#     langview.update_from_diff(featview, diff)

#     return featview, langview
