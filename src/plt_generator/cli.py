import os
from pathlib import Path
from .data.master_table import MasterTable
from .data.featview import FeatView
from .data.langview import LangView
from .html import HTMLBuilder
from .utils import path_manager


def sync() -> None:
    """
    Ensures that the language-view and the feature-view markdown files are in a consistent state,
      updating one from the other as needed.
    """
    ...


def generate() -> None:
    """
    Creates the .html file, with embedded CSS and JavaScript.
    """
    root = os.environ.get("PLT_ROOT") or Path(__file__).parent.parent.parent
    print(root)
    langview_root = root / "markdown_lang_view"
    featview_root = root / "markdown_feat_view"
    print(langview_root)
    print(featview_root)
    fv = FeatView.from_directory(featview_root)
    print(fv["0.0.0"])
    print(fv["0.0.0"]["python"])


def dryrun() -> None:
    """
    Demonstrates what would
    """
