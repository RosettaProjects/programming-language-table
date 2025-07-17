import os
from pathlib import Path

from .data.featview import FeatView
from .data.langview import LangView
from .sync import aggregate_from_diff, get_recent
from .utils.recency import save_timestamp

root = Path(os.environ.get("PLT_ROOT") or Path(__file__).parent.parent.parent)
metadata = root / "metadata"
history = metadata / "history"
generated = root / "generated"
langview_root = root / "markdown_lang_view"
featview_root = root / "markdown_feat_view"


def sync() -> None:
    """
    Ensures that the language-view and the feature-view markdown files are in a consistent state,
      updating one from the other as needed.
    """
    fv = FeatView.from_directory(featview_root)
    print(fv)
    lv = LangView.from_directory(langview_root)
    # print(lv["python"].rows)
    print(lv)
    # print("=======", fv.cells)
    # print("=======", lv.cells)
    # print("fv", [(s.row, s.name, s.path) for s in fv._row_dict.values()])
    # print("lv", [s.raw for s in lv._lang_dict.values()])

    recency = get_recent(fv, lv)
    print(recency)
    aggregate = aggregate_from_diff(fv, lv, recency)
    # for key, illustr in aggregate.items():
    #     print(key)
    #     print(illustr)
    aggregate.write_featview(featview_root)
    aggregate.write_featview(langview_root)

    # with open(history / f"diff_{make_timestamp()}", "w") as f:
    #     json.dump(diff, f)

    save_timestamp("synced", metadata / "timestamp.json")

    # fv_new.write(featview_root)
    # lv_new.write(langview_root)


def generate() -> None:
    """
    Creates the .html file, with embedded CSS and JavaScript.
    """
    print(root)
    print(generated)
    print(langview_root)
    print(featview_root)
    FeatView.from_directory(featview_root)
    # print(fv["0.0.0"])
    # print(fv["0.0.0"]["python"])
    save_timestamp("generated", metadata / "timestamp.json")


def dryrun() -> None:
    """
    Demonstrates what would happen if the command were run.
    """
