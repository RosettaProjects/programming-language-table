SECTIONS = {"H1", "H2", "H3", "H4", "H5"}


def is_section(token_class: str) -> bool:
    return token_class in SECTIONS


def increment(level:str) -> str:
    num = int(level[1])
    return f"H{num + 1}"


def decrement(level:str) -> str:
    num = int(level[1])
    return f"H{num - 1}"


def superlevels(level: str) -> set[str]:
    return {lvl for lvl in SECTIONS if lvl < level}


def next_class(tokens: list[tuple[str, str]]) -> tuple[str, str]:
    return tokens[0][0]


def next_is_section(tokens: list[tuple[str, str]]) -> bool:
    return (next_class(tokens) in SECTIONS)


def parse(tokens: list[tuple[str, str]]) -> tuple[str, tuple]:
    def parse_code_block(tokens: list[tuple[str, str]]) -> tuple[str, tuple]:
        assert next_class(tokens) == "CODE_START"
        tokens.pop(0)
        code = tokens.pop(0)[1]
        language, code = code.split("\n", maxsplit=1)
        assert next_class(tokens) == "CODE_END"
        tokens.pop(0)
        return ("CODE", ("LANGUAGE", language), ("CONTENT", code))

    def parse_content(tokens: list[tuple[str, str]]) -> tuple[str, tuple]:
        assert next_class(tokens) == "TITLE"
        title_token = tokens.pop(0)
        print(title_token)

        loose_content = []
        while tokens and not next_is_section(tokens):
            if next_class(tokens) == "CODE_START":
                loose_content.append(parse_code_block(tokens))
            elif next_class(tokens) == "BLANK_LINE":
                tokens.pop(0)
            elif next_class(tokens) == "TEXT_LINE":
                loose_content.append(tokens.pop(0))
            else:
                raise ValueError(f"Invalid token class for content: {tokens.pop(0)}")

        return (title_token, *loose_content)

    def parse_subsection(tokens: list[tuple[str, str]], level: str) -> tuple[tuple, ...]:
        if not tokens:
            return tuple()
        assert (tok := next_class(tokens)) == level, f"level: {level}, token: {str(tok)}"
        head = tokens.pop(0)
        content = parse_content(tokens)
        subsecs = parse_subsections(tokens, increment(level))
        return (head[0], (*content, ("SUBSECTIONS", *subsecs)))

    def parse_subsections(tokens: list[tuple[str, str]], level: str) -> tuple[tuple, ...]:
        if (not tokens):
            return tuple()
        if next_class(tokens) in superlevels(level):
            return tuple()
        # assert next_is_section(tokens)
        assert (tok := next_class(tokens)) == level, f"level: {level}, token: {str(tok)}"
        subsections = []
        while tokens and (not next_class(tokens) in superlevels(level)):
            subsections.append(parse_subsection(tokens, level))

        return tuple(subsections)

    assert next_class(tokens) == "H1"
    H1, _ = tokens.pop(0)
    
    h1_content = parse_content(tokens)
    subsections = parse_subsections(tokens, "H2")

    return (H1, (*h1_content, ("SUBSECTIONS", *subsections)))


# ("H1", ("TITLE", "..."), ("TEXT", "..."), ("CODE", ("LANGUAGE", "..."), ("CONTENT", "...")), ("SUBSECTIONS", ("H2", (...)), ...))

def as_dict(parse_tuple: tuple[str, tuple]) -> dict[str, dict]:
    def process_code(code_tuple: tuple) -> dict:
        print("%%%%%%%%%", code_tuple)
        out = {}
        for child in code_tuple:
            if child[0] == "LANGUAGE":
                out.update({"language": child[1]})
            elif child[0] == "CONTENT":
                out.update({"content": child[1]})
            else:
                raise ValueError(str(child))

        return {"code": out}


    def process_section(subtuple: tuple) -> dict:
        subdict = {"CONTENT": [], "SUBSECTIONS": []}
        for child in subtuple[1]:
            print("======== CHILD:", child)
            if child[0] == "TITLE":
                subdict.update({"TITLE": child[1]})
            elif child[0] == "SUBSECTIONS":
                subdict["SUBSECTIONS"] = process_subsections(child[1:])
            elif child[0] == "CODE":
                subdict["CONTENT"].append(process_code(child[1:]))
            elif child[0] == "TEXT_LINE":
                subdict["CONTENT"].append({"text_line": child[1]})
            else:
                raise ValueError(str(child))
        return subdict
    
    def process_subsections(subsecs: tuple[tuple, ...]) -> list[dict]:
        print("------------------------------- processing subsections -------------------------------------")
        out = []
        for subsec in subsecs:
            print("======== SUBSECTION:", subsec)
            out.append(process_section(subsec))
        return out

        
    return process_section(parse_tuple)


def extract_paths(subdict: dict, prefix: str = "") -> list[str]:
        new_prefix = subdict["TITLE"] if not prefix else "<>".join((prefix, subdict["TITLE"]))
        new_paths = [new_prefix]
        for subsection in subdict.get("SUBSECTIONS", []):
            new_paths.extend(extract_paths(subsection, prefix=new_prefix))
        return new_paths



# if __name__ == "__main__":
#     from pathlib import Path
#     # from .tokenizer import tokenize

#     text = Path("/home/isaac/repos/programming-language-table/markdown_lang_view/python.md").read_text()
#     toks = tokenize(text)
#     tup = parse(toks)
#     print(tup)
#     d = as_dict(tup)
#     print(d)
#     e = extract_paths()
