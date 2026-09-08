"""Suite de interacoes entre classes: os oito blocos do slide 98 - Aula 03.

Aqui a entrada é um trecho de programa, nao uma palavra candidata a lexema unico.
O que se verifica é a decisao do lexer, e nao a pertinencia a uma classe
"""

from dataclasses import dataclass
from enum import Enum


class Bloco(Enum):
    KEYWORD_CORE_X_IDENT_BASE = "KEYWORD_CORE x IDENT_BASE"
    KEYWORD_EXT_X_IDENT_BASE = "KEYWORD_EXT x IDENT_BASE"
    ASSIGN_X_REL_OP = "ASSIGN x REL_OP"
    ARITH_OP_X_LINE_COMMENT = "ARITH_OP x LINE_COMMENT"
    PREFIXOS_REL_OP = "Prefixos de REL_OP"
    ARITH_OP_X_INT_LITERAL = "ARITH_OP x INT_LITERAL"
    DELIMITADORES_ADJACENTES = "Delimitadores adjacentes"
    CLASSES_IGNORADAS = "Classes ignoradas"


@dataclass(frozen=True)
class Interacao:
    bloco: Bloco
    entrada: str
    emitidos: tuple[str, ...]
    justificativa: str
    ignorados: tuple[str, ...] = ()
    erro_na_posicao: int | None = None


INTERACOES: list[Interacao] = [
    # 1. Sobreposicao completa: as reservadas casam com o padrao-base.
    Interacao(Bloco.KEYWORD_CORE_X_IDENT_BASE, "int", ("KW_INT",),
              "O lexema inteiro é a palavra reservada, entao reclassifica."),
    Interacao(Bloco.KEYWORD_CORE_X_IDENT_BASE, "intx", ("IDENT",),
              "Maior lexema vence: IDENT_BASE casa 4 caracteres e KEYWORD_CORE só 3."),
    Interacao(Bloco.KEYWORD_CORE_X_IDENT_BASE, "print", ("KW_PRINT",),
              "A outra reservada do nucleo, tambem por lexema inteiro."),
    Interacao(Bloco.KEYWORD_CORE_X_IDENT_BASE, "print2", ("IDENT",),
              "Um digito no fim ja tira a palavra de RCore."),

    # 2. Mesma sobreposicao, agora com as reservadas das extensoes.
    Interacao(Bloco.KEYWORD_EXT_X_IDENT_BASE, "if", ("KW_IF",),
              "Lexema inteiro pertence a RExt."),
    Interacao(Bloco.KEYWORD_EXT_X_IDENT_BASE, "ifx", ("IDENT",),
              "Um caractere a mais e a palavra volta a ser identificador."),
    Interacao(Bloco.KEYWORD_EXT_X_IDENT_BASE, "else2", ("IDENT",),
              "Digito na continuacao afasta de 'else'."),
    Interacao(Bloco.KEYWORD_EXT_X_IDENT_BASE, "while1", ("IDENT",),
              "Mesma situacao de else2."),

    # 3. Prefixo comum entre atribuicao e igualdade.
    Interacao(Bloco.ASSIGN_X_REL_OP, "=", ("ASSIGN",),
              "Um so '=' é atribuicao."),
    Interacao(Bloco.ASSIGN_X_REL_OP, "==", ("EQ",),
              "Maior lexema: REL_OP casa dois caracteres, ASSIGN casaria um."),
    Interacao(Bloco.ASSIGN_X_REL_OP, "===", ("EQ", "ASSIGN"),
              "O lexer consome '==' e sobra '=', que vira ASSIGN."),

    # 4. Prefixo comum entre divisao e comentario.
    Interacao(Bloco.ARITH_OP_X_LINE_COMMENT, "/", ("SLASH",),
              "Uma barra sozinha é divisao."),
    Interacao(Bloco.ARITH_OP_X_LINE_COMMENT, "//", (),
              "Duas barras iniciam comentario, que é ignorado.",
              ignorados=("LINE_COMMENT",)),
    Interacao(Bloco.ARITH_OP_X_LINE_COMMENT, "//x", (),
              "O corpo segue ate a quebra de linha; nada e emitido.",
              ignorados=("LINE_COMMENT",)),

    # 5. Prefixos dentro da propria familia REL_OP.
    Interacao(Bloco.PREFIXOS_REL_OP, "<", ("LT",), "Palavra de um caractere da classe."),
    Interacao(Bloco.PREFIXOS_REL_OP, "<=", ("LE",), "Maior lexema vence sobre '<'."),
    Interacao(Bloco.PREFIXOS_REL_OP, ">", ("GT",), "Simetrico de '<'."),
    Interacao(Bloco.PREFIXOS_REL_OP, ">=", ("GE",), "Simetrico de '<='."),
    Interacao(Bloco.PREFIXOS_REL_OP, "!", (),
              "'!' esta no alfabeto mas nao casa com classe nenhuma: so existe em '!='.",
              erro_na_posicao=0),
    Interacao(Bloco.PREFIXOS_REL_OP, "!=", ("NE",),
              "Com o '=' ao lado, a palavra passa a pertencer a REL_OP."),

    # 6. Operador e literal em sequencia, nunca um lexema so.
    Interacao(Bloco.ARITH_OP_X_INT_LITERAL, "-10", ("MINUS", "INT_LITERAL"),
              "O sinal nao pertence ao literal (slide 73 - Aula 03)."),
    Interacao(Bloco.ARITH_OP_X_INT_LITERAL, "+7", ("PLUS", "INT_LITERAL"),
              "Mesma decisao para o '+'."),

    # 7. Delimitadores encostados continuam sendo lexemas separados.
    Interacao(Bloco.DELIMITADORES_ADJACENTES, "()", ("LPAREN", "RPAREN"),
              "'()' pertence a L_DelimiterCore², nao a L_DelimiterCore."),
    Interacao(Bloco.DELIMITADORES_ADJACENTES, "{}", ("LBRACE", "RBRACE"),
              "Mesma regra para as chaves das extensoes."),
    Interacao(Bloco.DELIMITADORES_ADJACENTES, ");", ("RPAREN", "SEMICOLON"),
              "Delimitadores de lexemas diferentes tambem nao se fundem."),

    # 8. Espacos e comentarios sao reconhecidos e nao chegam ao parser.
    Interacao(Bloco.CLASSES_IGNORADAS, "x = 1", ("IDENT", "ASSIGN", "INT_LITERAL"),
              "Os espacos separam os lexemas e somem na saida.",
              ignorados=("WHITESPACE", "WHITESPACE")),
    Interacao(Bloco.CLASSES_IGNORADAS, "x=1 // fim", ("IDENT", "ASSIGN", "INT_LITERAL"),
              "Comentario no fim da linha nao produz token.",
              ignorados=("WHITESPACE", "LINE_COMMENT")),
    Interacao(Bloco.CLASSES_IGNORADAS, "int\tx;", ("KW_INT", "IDENT", "SEMICOLON"),
              "Tabulacao tambem é WHITESPACE e tambem é ignorada.",
              ignorados=("WHITESPACE",)),
]


# Gabaritos do slide, usados como prova de que o catalogo bate com a aula
EXERCICIO_10 = Interacao(
    Bloco.CLASSES_IGNORADAS,
    "print(total-2); // ok",
    ("KW_PRINT", "LPAREN", "IDENT", "MINUS", "INT_LITERAL", "RPAREN", "SEMICOLON"),
    "Resultado do slide 82 - Aula 03.",
    ignorados=("WHITESPACE", "LINE_COMMENT"),
)

EXERCICIO_11 = Interacao(
    Bloco.ASSIGN_X_REL_OP,
    "intx==10//fim",
    ("IDENT", "EQ", "INT_LITERAL"),
    "Resultado do slide 84 - Aula 03, que nomeia o segundo token pela classe REL_OP.",
    ignorados=("LINE_COMMENT",),
)