import re

from .illustration import Illustration
from .row_id import RowID

FEAT_SECTION_REGEX: re.Pattern = re.compile(
    r"\n(?P<octothorpes>#+) +"
    r"((?P<id0>\d+)\.)((?P<id1>\d+)\.)?((?P<id2>\d+)\.)? +"
    r"(?P<title>[^\n]+)"
    r"\n(\n*(?P<note>[^\n>#].+?)\n\n)?"
    r"(\n*> Snippet:\n\n```(?P<lang>[a-z]+)\n(?P<snippet>.*?)\n```\n\n)?"
    r"(\n*> Output:\n\n```txt\n(?P<snippet_output>.*?)\n```\n\n)?"
    r"(\n*> Full:\n\n```(?P<lang_full>[a-z]+)\n(?P<full_code>.*?)\n```\n\n)?"
    r"(\n*> Output:\n\n```txt\n(?P<full_output>.*?)\n```)?",
    re.DOTALL,
)

LANG_SECTION_REGEX: re.Pattern = re.compile(
    r"#+ (?P<language>[^\n]+)\n\n"
    r"(\n*(?P<note>[^>#].+?)\n\n)?"
    r"(\n*> Snippet:\n\n```(?P<lang>[a-z]+)\n(?P<snippet>.*?)\n```\n\n)?"
    r"(\n*> Output:\n\n```txt\n(?P<snippet_output>.*?)\n```\n\n)?"
    r"(\n*> Full:\n\n```(?P<lang_full>[a-z]+)\n(?P<full_code>.*?)\n```\n\n)?"
    r"(\n*> Output:\n\n```txt\n(?P<full_output>.*?)\n```)?",
    re.DOTALL,
)


"""
Cases:
0) snippet and full are the same (only snippet is given)
1) snippet output and full output exist and differ
1) no snippet output, but full output
2) no full output -> same as snippet output
3) neither has output (should full always have output?)



for result in re.finditer(SECTION_REGEX, "\n" + raw_md):
    for key, value in result.groupdict().items():
        if value is not None:
            print(f"{key}: {value!r}")
    print()
"""


def split_file(raw_md: str) -> list[str]:
    """
    Splits the raw markdown file into sections based on the octothorpes.
    """
    return re.split(r"\n(?=#)", raw_md.strip())


def parse_feat_block(raw_md_block: str) -> Illustration:
    """
    Parses the raw markdown block and returns a RowID or (if possible) an Illustration.
    """
    # print("\n" + raw_md_block + "\n")
    result = re.search(FEAT_SECTION_REGEX, "\n" + raw_md_block + "\n")
    if not result:
        raise ValueError(f"Invalid block:\n{raw_md_block}")
    groups = result.groupdict()
    if not groups["snippet"]:
        return RowID(
            main=int(groups["id0"]),
            sub=int(groups["id1"]) if groups["id1"] else None,
            subsub=int(groups["id2"]) if groups["id2"] else None,
            text=groups["title"],
            octothorpes=groups["octothorpes"],
        )
    return Illustration.from_dict(**groups)


def parse_lang_block(raw_md_block: str) -> None | tuple[str, Illustration]:
    """
    Parses the raw markdown block and returns a RowID or (if possible) an Illustration.
    """
    print("\n" + raw_md_block + "\n")
    result = re.search(LANG_SECTION_REGEX, "\n" + raw_md_block + "\n")
    if not result:
        raise ValueError(f"Invalid block:\n{raw_md_block}")
    groups = result.groupdict()
    if not groups["snippet"]:
        return None
        raise ValueError(f"No snippet found in '''{raw_md_block}'''")
    return groups["language"], Illustration.from_dict_rowless(**groups)


def parse_lang_file(raw_md: str) -> dict[RowID, None | Illustration]:
    sections: dict[RowID, None | Illustration] = {}

    raw_blocks = split_file(raw_md)[1:]
    for block in raw_blocks:
        parsed = parse_feat_block(block)
        if isinstance(parsed, RowID):
            sections.update({parsed.numbers: parsed})
        else:
            sections.update({parsed.row.numbers: parsed})
    return sections


def parse_feat_file(raw_md: str) -> dict[str, Illustration]:
    sections: dict[RowID, None | Illustration] = {}

    # s = re.search(FEAT_SECTION_REGEX, raw_md)
    # if not s:
    #     raise ValueError(f"No feature information found in '''{raw_md[:200]}\n...'''")

    raw_blocks = split_file(raw_md)[1:]
    for block in raw_blocks:
        if (parsed := parse_lang_block(block)):
            lang, illustration = parsed
            sections.update({lang: illustration})
    return sections
