from dataclasses import dataclass
from pathlib import Path


@dataclass
class PathManager:
    root = Path(__file__).parent
    feat_view_dir = root / "markdown_feat_view"
    lang_view_dir = root / "markdown_lang_view"
    output_dir = root / "html"
    build_dir = root / "build"
