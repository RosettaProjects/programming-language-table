from .master_table import MasterTable
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


def dryrun() -> None:
    """
    Demonstrates what would
    """
