from collections import OrderedDict


# LANGUAGE_ABBREVS: OrderedDict[str, str] = {
#     "py": "Python",
#     "rs": "Rust",
#     "go": "Go",
#     "hs": "Haskell",
# }

LANGUAGE_ABBREVS: OrderedDict[str, str] = {
    "Python": {
        "order": 0,
        "abbreviation": "py",
        "categories": [
            "default",
            "popular",
            "c_family",
            "dynamically_typed",
            "garbage_collected",
            "interpreted",
        ],
    },
    "Rust": {
        "order": 0,
        "abbreviation": "rs",
        "categories": [
            "default",
            "popular",
            "c_family",
            "statically_typed",
            "compiled",
        ],
    },
    "Guile Scheme": {
        "order": 0,
        "abbreviation": "scm",
        "categories": [
            "default",
            "popular",
            "lisp",
            "dynamically_typed",
            "garbage_collection",
            "interpreted",
        ],
    },
    "Haskell": {
        "order": 0,
        "abbreviation": "hs",
        "categories": [
            "default",
            "popular",
            "functional",
            "pure",
            "statically_typed"
            "garbage_collection",
            "interpreted",
            "compiled",
        ],
    },
    "C": {
        "order": 0,
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Java": {
        "order": 0,
        "abbreviation": "",
        "categories": [
            "core",
            "garbage_collected",
            "",
        ],
    },
    "JavaScript": {
        "order": 0,
        "abbreviation": "",
        "categories": [
            "core",
            "garbage_collected",
            "",
        ],
    },
    "TypeScript": {
        "abbreviation": "",
        "categories": [
            "core",
            "garbage_collected",
            "",
        ],
    },
    "OCaml": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Common Lisp": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "C++": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Zig": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Ruby": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Scala": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Go": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Lua": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Julia": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Kotlin": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Erlang": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Ada": {
        "abbreviation": "",
        "categories": [
            "extended_core",
            "",
            "",
        ],
    },
    "Clojure": {
        "abbreviation": "",
        "categories": [
            "extended_core",
            "",
            "",
        ],
    },
    "D": {
        "abbreviation": "",
        "categories": [
            "extended_core",
            "",
            "",
        ],
    },
    "Elixir": {
        "abbreviation": "",
        "categories": [
            "core",
            "",
            "",
        ],
    },
    "Elm": {
        "abbreviation": "",
        "categories": [
            "extended_core",
            "",
            "",
        ],
    },
    "Fortran": {
        "abbreviation": "",
        "categories": [
            "extended_core",
            "",
            "",
        ],
    },
    "Gleam": {
        "abbreviation": "",
        "categories": [
            "extended_core",
            "",
            "",
        ],
    },
    "Haxe": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Idris": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Racket": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Raku": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "PureScript": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "PHP": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Perl": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Octave": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Nim": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Roc": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "R": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "F#": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "C#": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Typed Racket": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Crystal": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Dart": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "V (Vlang)": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Vala": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Tcl": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
    "Swift": {
            "abbreviation": "",
            "categories": [
                "extended_core",
                "",
                "",
            ],
        },
}

'''
https://rosettacode.org/wiki/Category:Languages_by_Feature
https://rosettacode.org/wiki/Language_Comparison_Table


=============== FUN/NICHE ==============
MoonScript
CoffeeScript
AngelScript
AWK
Binary Lambda Calculus
BQN
DreamBerd
DuckDB
EasyLang
Factor
Falcon
Fōrmulæ
Frink
GDL
Ghostscript
Grain
Groovy
Hare
Hexiscript
HolyC
Insitux
Io
J
Jinja
Joy
Komodo
Lobster
Make
Maxima
Mercury
MiniScript
Mojo
Monkey
Objeck
Odin https://odin-lang.org/
Onyx https://www.onyxlang.io/
Phix http://phix.x10.mx/
PlainTeX
Pony https://www.ponylang.io/
Processing https://processing.org/
Processing https://py.processing.org/
Processing.R https://processing-r.github.io/
Quackery https://github.com/GordonCharlton/Quackery
ReasonML https://reasonml.github.io/
Red https://www.red-lang.org/
Ring https://ring-lang.github.io/
Roc https://www.roc-lang.org/
S-lang https://www.jedsoft.org/slang/
Scratch https://scratch.mit.edu/
ScratchScript https://github.com/ScratchScript/ScratchScript
Sed https://www.gnu.org/software/sed/manual/sed.html
Self https://selflanguage.org/
Squirrel http://www.squirrel-lang.org/
Tailspin https://github.com/tobega/tailspin-v0
Wisp https://www.draketo.de/software/wisp
Wren https://wren.io/
YAMLScript https://yamlscript.org/

============== OTHER LISPS ==============
Chicken Scheme
Fennel
Owl Lisp
PicoLisp
NewLISP
Ol
EchoLisp
Emacs Lisp
Lush
Janet
Hy
ACL2
R7RS Scheme

============== SHELLS ==============
Nu
Bash
C Shell
Ksh
Friendly interactive shell
Zsh

============== HISTORICAL ==============
Simula
Modula
ALGOL 68
B
Object Pascal
Oberon
COBOL
Smalltalk
Miranda
Pascal
Standard ML
BASIC (FreeBASIC)
APL
Forth
Eiffel

============== ASSEMBERS ==============
6502 Assembly
AArch64 Assembly
RISC-V Assembly
Z80 Assembly
WebAssembly
X86 Assembly
X86-64 Assembly
LC3 Assembly (1 C, 8 P)
ARM Assembly
HLA
Little Man Computer

============== BYTECODE ==============
LLVM
JVM

============== MISCELLANEOUS ==============
LaTeX
Nix
Gnuplot
CMake
Terraform
Vim Script

============== LOGIC/MATHEMATICAL ==============
Prolog
Datalog
Sage
Agda2
SWI-Prolog

============== DATABASE/QUERY ==============
MariaDB
XQuery
GraphQL
SQL
Jq

'''