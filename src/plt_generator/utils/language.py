from enum import StrEnum, auto
from typing import Self
import re


class ProgLang(StrEnum):
    PYTHON = auto()
    JAVASCRIPT = auto()
    TYPESCRIPT = auto()
    C = auto()
    CPP = auto()
    RUST = auto()
    GO = auto()
    JULIA = auto()
    R = auto()
    BASH = auto()
    ZSH = auto()
    JAVA = auto()
    KOTLIN = auto()
    SCALA = auto()
    COMMONLISP = auto()
    FORTRAN = auto()
    LUA = auto()
    ADA = auto()
    HASKELL = auto()
    OCAML = auto()
    APL = auto()
    ZIG = auto()

    @classmethod
    def _missing_(cls, value: str) -> Self | None:
        value = re.sub(r"[^A-Z]", "", value.upper())
        for member in cls:
            if member.value == value:
                return member
        return None

    def __repr__(self) -> str:
        return f"ProgLang.{self.name}"


language_info: dict[str, dict[str, str]] = {
    ProgLang.PYTHON: dict(
        aliases={"PY"},
    ),
    ProgLang.JAVASCRIPT: dict(
        aliases={"JS", "ECMASCRIPT", "ES"},
    ),
    ProgLang.TYPESCRIPT: dict(
        aliases={"TS"},
    ),
    ProgLang.C: dict(
        aliases={"CLANG", "H"},
    ),
    ProgLang.CPP: dict(
        aliases={"C++", "CXX", "HPP", "HXX"},
    ),
    ProgLang.RUST: dict(
        aliases={"RS"},
    ),
    ProgLang.GO: dict(
        aliases={"GOLANG"},
    ),
    ProgLang.JULIA: dict(
        aliases={"JL"},
    ),
    ProgLang.R: dict(
        aliases={"RLANG"},
    ),
    ProgLang.BASH: dict(
        aliases={"SH", "SHELL"},
    ),
    ProgLang.ZSH: dict(
        aliases={"ZSHELL"},
    ),
    ProgLang.JAVA: dict(
        aliases={"JAVALANG"},
    ),
    ProgLang.KOTLIN: dict(
        aliases={"KT"},
    ),
    ProgLang.SCALA: dict(
        aliases={"SC"},
    ),
    ProgLang.COMMONLISP: dict(
        aliases={"CL"},
    ),
    ProgLang.FORTRAN: dict(
        aliases={"FT"},
    ),
    ProgLang.LUA: dict(
        aliases={"LUALANG"},
    ),
    ProgLang.ADA: dict(
        aliases={"ADALANG"},
    ),
    ProgLang.HASKELL: dict(
        aliases={"HS"},
    ),
    ProgLang.OCAML: dict(
        aliases={"ML", "MLI"},
    ),
    ProgLang.APL: dict(
        aliases={"APLLANG"},
    ),
    ProgLang.ZIG: dict(
        aliases={"ZIGLANG"},
    ),
}

language_lookup = {
    alias: standardized
    for standardized, alias_set in {
        k: v["aliases"] | {k.name} for k, v in language_info.items()
    }.items()
    for alias in alias_set
}


def language_resolver(lang_name: str) -> ProgLang | None:

    lookup_result = language_lookup.get(re.sub(r"[^A-Z]", "", lang_name.upper()))
    if not lookup_result:
        return None

    return lookup_result


assert len(ProgLang) == len(language_info)
