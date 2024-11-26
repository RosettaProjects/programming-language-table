import re


token_specification = (
        ("BLANK_LINE", "\n\n+"),
        ("H1", r"^# "),
        ("H2", r"(?<=\n)## "),
        ("H3", r"(?<=\n)### "),
        ("H4", r"(?<=\n)#### "),
        ("H5", r"(?<=\n)##### "),
        ("TITLE", r"(?<=# )[^\n]+"),
        # ("CODE_LANGUAGE", r"(?<=^```)[a-z]+(?=\n)"),
        ("CODE", r"(?<=\n```)[a-z]+\n.*?(?=\n```)"),
        ("CODE_START", r"(?<=\n)```(?=[a-z])"),
        ("CODE_END", r"(?<=\n)```(?=\n)"),
        # ("TEXT", r"\n\n.+\n\n"),
        ("TEXT_LINE", r"(?<=\n)[^\n`#][^\n]*"),
        ("LINE_BREAK", r"\n"),
        ("BAD", r"."),
)

token_regex = re.compile("|".join(f"(?P<{token_class}>{token_pattern})" for token_class, token_pattern in token_specification), re.UNICODE | re.DOTALL)
# t = tokenize(text)
# print(t)

def tokenize(md_text: str) -> list[tuple[str, str]]:
    
    tokens = []
    for mo in re.finditer(token_regex, md_text):
            kind = mo.lastgroup
            value = mo.group()

            if kind in {"BLANK_LINE", "LINE_BREAK"}:
                 continue
            
            print(kind, value)
            if kind == "BAD":
                raise RuntimeError(f"Unexpected character: {value}")
            tokens.append((kind, value))
    return tokens