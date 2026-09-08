"""Tipos de token da MiniLang-Core e o registro produzido pelo lexer."""

from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    KW_INT = "KW_INT"
    KW_PRINT = "KW_PRINT"
    KW_IF = "KW_IF"
    KW_ELSE = "KW_ELSE"
    KW_WHILE = "KW_WHILE"

    IDENT = "IDENT"
    INT_LITERAL = "INT_LITERAL"

    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    # Tipos especificos da familia REL_OP, como ARITH_OP gera PLUS e MINUS (slide 79 - aula 03)
    EQ = "EQ"
    NE = "NE"
    LT = "LT"
    LE = "LE"
    GT = "GT"
    GE = "GE"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SEMICOLON = "SEMICOLON"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"

    # Reconhecidos e ignorados (slide 79).
    WHITESPACE = "WHITESPACE"
    LINE_COMMENT = "LINE_COMMENT"


@dataclass(frozen=True)
class Token:
    tipo: TokenType
    lexema: str
    pos: int

    def __str__(self) -> str:
        return f"{self.lexema!r} -> {self.tipo.value}"
