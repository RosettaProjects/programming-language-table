from typing import TypeVar

T = TypeVar("T")
type NestedDict = dict[str, dict[str, list[str]]]
type NestedTupleDict = dict[tuple[str], dict[tuple[str, str], list[tuple[str, str, str]]]]
type DiffDict = dict


def flatten_dict(d: NestedDict) -> set[tuple[str, ...]]:
    out: set[tuple[str, ...]] = set()
    for k, v in d.items():
        out.add((k,))
        for kk, vv in v.items():
            out.add((k, kk))
            for kkk in vv:
                out.add((k, kk, kkk))
    return out


def get_dictionary_diff(fv: NestedDict, lv: NestedDict) -> DiffDict:
    flat_fv, flat_lv = map(flatten_dict, (fv, lv))
    return {
        "featview_missing": flat_fv - flat_lv,
        "langview_missing": flat_lv - flat_fv,
    }


def get_list_diff(fv: list[T], lv: list[T]) -> DiffDict:
    set_fv, set_lv = map(set, (fv, lv))
    return {
        "featview_missing": set_fv - set_lv,
        "langview_missing": set_lv - set_fv,
    }


"""
test1 = {"A": {"AA": ["AAA", "BBB"]}}
test2 = {"A": {"AA": ["BBB", "CCC"]}, "B": {}}

result = {
    "missing": [("A", "AA", "AAA")],
    "added": [("A", "AA", "CCC"), ("B",)],
}
"""
