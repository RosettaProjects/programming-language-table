import pygments


class SyntaxHighlighter:
    """
    Tasked with generating html from all code sample for all languages.
    https://pygments.org/docs/quickstart/
    """

    ...

    def __call__(self, snippet: str, lang_code: str) -> str:
        """
        Generates an HTML object, given a code snippet and the programming language it is written
          in.
        """
        html = ""
        return html
