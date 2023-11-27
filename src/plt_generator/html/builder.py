from ..highlighting import SyntaxHighlighter
from ..master_table import MasterTable


class HTMLBuilder:
    def __init__(self, highlighter: SyntaxHighlighter) -> None:
        self.highlighter: SyntaxHighlighter = highlighter

    def __call__(self, table: MasterTable) -> str:
        html = ""
        return html
