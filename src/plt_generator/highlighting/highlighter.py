import html

from pygments.lexers import get_lexer_by_name
from pygments.token import Token
from pygments.token import _TokenType as TokenType

mapping = {
    Token.Keyword: "",
    Token.Keyword.Declaration: "keyword",
    Token.Keyword.Pseudo: "keyword",
    Token.Keyword.Reserved: "keyword",
    Token.Keyword.Type: "type",
    Token.Literal.Number.Integer: "number",
    Token.Literal.String: "string",
    Token.Literal.String.Char: "string",
    Token.Name: "identifier",
    Token.Name.Builtin: "keyword",
    Token.Name.Class: "thing",
    Token.Name.Function: "action",
    Token.Name.Function.Magic: "action",
    Token.Name.Namespace: "thing",
    Token.Operator: "operator",
    Token.Operator.Word: "operator",
    Token.Punctuation: "structural",
    Token.Text.Whitespace: "structural",
}


def get_mapping(tok: TokenType) -> str:
    if tok in mapping:
        return mapping[tok]
    elif tok.parent in mapping:
        return mapping[tok.parent]
    return "structural"


t = """
use std::any::type_name;
use std::fmt::Binary;
use std::fmt::Display;
use std::mem::size_of;

fn get_type<T>(_: &T) -> &str {
    type_name::<T>()
}

fn print_info<T: Binary + Copy + Display>(varname: &str, variable: T) {
    let bit_width = size_of::<T>() * 8;
    println!("{varname}: type '{vartype}'", vartype = get_type(&variable));
    println!("  decimal: {}", variable);
    println!("  stored as: {:0bit_width$b} binary\n", variable, bit_width = bit_width);
}

fn main() {
    let signed_8bit: i8 = 27;
    let signed_16bit: i16 = -3;
    let signed_32bit: i32 = -666;
    let signed_64bit: i64 = 42;
    let signed_128bit: i128 = 999999;

    let unsigned_8bit: u8 = 56;
    let unsigned_16bit: u16 = 1;
    let unsigned_32bit: u32 = 0;
    let unsigned_64bit: u64 = 1234567;
    let unsigned_128bit: u128 = 123456789;

    print_info("signed_8bit", signed_8bit);
    print_info("signed_16bit", signed_16bit);
    print_info("signed_32bit", signed_32bit);
    print_info("signed_64bit", signed_64bit);
    print_info("signed_128bit", signed_128bit);

    print_info("unsigned_8bit", unsigned_8bit);
    print_info("unsigned_16bit", unsigned_16bit);
    print_info("unsigned_32bit", unsigned_32bit);
    print_info("unsigned_64bit", unsigned_64bit);
    print_info("unsigned_128bit", unsigned_128bit);
}
"""


def escape_string(s: str) -> str:
    return html.escape(s).replace(" ", "&nbsp;").replace("\n", "<br>")


def make_span(toktype: TokenType, tokval: str) -> str:
    return f'<span class="{get_mapping(toktype)}">{escape_string(tokval)}</span>'


def make_block(code: str, language: str) -> str:
    lexer = get_lexer_by_name(language)
    return "".join(make_span(*pair) for pair in lexer.get_tokens(t))


# for :
#     print(f"{escape_string(tokval):<20} new: {get_mapping(toktype):<20}, orig: {toktype}")
#     # print()


class SyntaxHighlighter:
    """
    Tasked with generating html from all code sample for all languages.
    https://pygments.org/docs/quickstart/
    """

    ...

    def __call__(self, code: str, lang_id: str) -> str:
        """
        Generates an HTML object, given a code snippet and the programming language it is written
          in.
        """
        html = ""
        return html


# from pygments.lexers.rust import RustLexer
