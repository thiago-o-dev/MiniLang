import re
from dataclasses import dataclass, field
from enum import Enum

from .tokens import TokenType


class Acao(Enum):
    EMITE = "emitido ao parser"
    IGNORA = "reconhecido e ignorado"
    RECLASSIFICA = "reclassifica o lexema de outra classe"


@dataclass(frozen=True)
class ClasseLexica:
    """Uma classe lexica com os nove itens que o slide 90 exige da secao."""

    nome: str                                   # 1, com finalidade
    finalidade: str
    descricao: str                              # 2
    exemplos: tuple[str, ...]                   # 3
    definicao_matematica: str                   # 4
    expressao_formal: str                       # 6
    regex: str                                  # 7
    acao: Acao
    linguagem_finita: bool          # slide 96 cobra minimos diferentes

    conjuntos_auxiliares: tuple[str, ...] = ()  # 5, so quando a estrutura exigir

    # 8: a implementacao e o par padrao/tipo_de.
    tipo: TokenType | None = None
    tipo_por_lexema: dict[str, TokenType] = field(default_factory=dict)


    @property
    def padrao(self) -> re.Pattern:
        return re.compile(self.regex)

    def tipo_de(self, lexema: str) -> TokenType:
        tipo = self.tipo_por_lexema.get(lexema, self.tipo)
        if tipo is None:
            raise KeyError(f"{self.nome} nao classifica {lexema!r}")
        return tipo


# A ordem so desempata padroes que casem o MESMO numero de caracteres. Conflitos
# de prefixo ("/" vs "//", "=" vs "==") sao resolvidos pelo tamanho do lexema.
# As classes de palavra reservada nao participam da varredura: elas reclassificam
# um lexema ja reconhecido como IDENT_BASE (slide 72 - Aula 03)
TABELA_LEXICA: list[ClasseLexica] = [
    ClasseLexica(
        nome="KEYWORD_CORE",
        linguagem_finita=True,
        finalidade="Palavras reservadas do núcleo; reclassificam um lexema de IDENT_BASE. "
                   "Linguagem finita contida em L_IdentBase: só o lexema inteiro reclassifica.",
        descricao="As duas únicas palavras que a MiniLang-Core reserva. Nenhuma outra "
                  "palavra pertence a classe, e a grafia tem que ser exata.",
        exemplos=("int", "print"),
        definicao_matematica='L_KeywordCore = RCore = {"int", "print"}',
        expressao_formal='rKeywordCore = "int" ∪ "print"',
        regex=r"int|print",
        acao=Acao.RECLASSIFICA,
        tipo_por_lexema={
            "int": TokenType.KW_INT,
            "print": TokenType.KW_PRINT,
        },
    ),
    ClasseLexica(
        nome="IDENT_BASE",
        linguagem_finita=False,
        finalidade="Padrão-base dos identificadores: produz os candidatos que as "
                   "classes de palavra reservada podem reclassificar.",
        descricao="Uma letra ou um underscore, seguido de zero ou mais letras, "
                  "dígitos ou underscores. Maiúsculas e minúsculas são diferentes.",
        exemplos=("_", "A1", "total2", "resultado", "intx"),
        definicao_matematica=(
            "L_IdentBase = {c_0 c_1 ... c_n | n ≥ 0, c_0 ∈ Inicial e "
            "c_i ∈ Continuação para 1 ≤ i ≤ n}"
        ),
        conjuntos_auxiliares=(
            "Letra = a ∪ ... ∪ z ∪ A ∪ ... ∪ Z",
            "Dígito = 0 ∪ 1 ∪ ... ∪ 9",
            'Inicial = Letra ∪ "_"',
            'Continuação = Letra ∪ Dígito ∪ "_"',
        ),
        expressao_formal="rIdentBase = Inicial Continuação*",
        regex=r"[A-Za-z_][A-Za-z0-9_]*",
        acao=Acao.EMITE,
        tipo=TokenType.IDENT,
    ),
    ClasseLexica(
        nome="INT_LITERAL",
        linguagem_finita=False,
        finalidade="Literais inteiros sem sinal: -10 é a sequência MINUS INT_LITERAL, não um literal.",
        descricao="Uma ou mais ocorrências de dígito. Zeros à esquerda são permitidos, "
                  "e o sinal não faz parte do literal.",
        exemplos=("0", "7", "45", "007"),
        definicao_matematica="L_IntLiteral = {d_1 d_2 ... d_n | n ≥ 1 e d_i ∈ Dígito}",
        conjuntos_auxiliares=("Dígito = 0 ∪ 1 ∪ ... ∪ 9",),
        expressao_formal="rNum = Dígito+ ≡ Dígito Dígito*",
        regex=r"[0-9]+",
        acao=Acao.EMITE,
        tipo=TokenType.INT_LITERAL,
    ),
    ClasseLexica(
        nome="ASSIGN",
        linguagem_finita=True,
        finalidade="Operador de atribuição. Um '=' é atribuição; '==' pertence a REL_OP "
                   "e casa um lexema mais longo.",
        descricao="Linguagem finita de uma única palavra, o símbolo de igual sozinho.",
        exemplos=("=",),
        definicao_matematica='L_Assign = {"="}',
        expressao_formal='rAssign = "="',
        regex=r"=",
        acao=Acao.EMITE,
        tipo=TokenType.ASSIGN,
    ),
    ClasseLexica(
        nome="ARITH_OP",
        linguagem_finita=True,
        finalidade="Família dos operadores aritméticos; gera PLUS, MINUS, STAR e SLASH.",
        descricao="Um dos quatro símbolos de operação aritmética, sempre um único caractere.",
        exemplos=("+", "-", "*", "/"),
        definicao_matematica='L_ArithOp = {"+", "-", "*", "/"}',
        expressao_formal='rArith = "+" ∪ "-" ∪ "*" ∪ "/"',
        regex=r"[-+*/]",
        acao=Acao.EMITE,
        tipo_por_lexema={
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
        },
    ),
    ClasseLexica(
        nome="DELIMITER_CORE",
        linguagem_finita=True,
        finalidade="Delimitadores do núcleo, que separam e agrupam construções. '()' não "
                   "pertence à classe: é uma palavra de L_DelimiterCore².",
        descricao="Parêntese de abertura, parêntese de fechamento ou ponto e vírgula, "
                  "cada um como um lexema isolado.",
        exemplos=("(", ")", ";"),
        definicao_matematica='L_DelimiterCore = DCore = {"(", ")", ";"}',
        expressao_formal='rDelim = "(" ∪ ")" ∪ ";"',
        regex=r"[();]",
        acao=Acao.EMITE,
        tipo_por_lexema={
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            ";": TokenType.SEMICOLON,
        },
    ),
    ClasseLexica(
        nome="LINE_COMMENT",
        linguagem_finita=False,
        finalidade="Comentário de linha; reconhecido e ignorado, nunca enviado ao parser. "
                   "O corpo vazio é válido e a quebra encerra sem integrar o lexema.",
        descricao="Começa com duas barras e segue até imediatamente antes da quebra de "
                  "linha. O corpo pode ser vazio e a quebra não integra o lexema.",
        exemplos=("//", "//x", "// comentário", "////"),
        definicao_matematica='L_LineComment = {"//"w | w ∈ C*}',
        conjuntos_auxiliares=(
            "ΣFonte = caracteres permitidos no arquivo-fonte",
            "CR = retorno de carro, NL = nova linha",
            "C = ΣFonte − {CR, NL}",
        ),
        expressao_formal='rComentário = "//" C*',
        regex=r"//[^\r\n]*",
        acao=Acao.IGNORA,
        tipo=TokenType.LINE_COMMENT,
    ),
    ClasseLexica(
        nome="WHITESPACE",
        linguagem_finita=False,
        finalidade="Separador de lexemas; reconhecido e ignorado, nunca enviado ao parser. "
                   "Exige ao menos um caractere: ε ∉ L_Whitespace.",
        descricao="Uma ou mais ocorrências de espaço, tabulação, retorno de carro ou "
                  "nova linha, em qualquer combinação.",
        exemplos=(" ", "\t", "  ", " \t\n"),
        definicao_matematica="L_Whitespace = {b_1 b_2 ... b_n | n ≥ 1 e b_i ∈ B}",
        conjuntos_auxiliares=(
            "ESP = espaço, TAB = tabulação, CR = retorno de carro, NL = nova linha",
            "B = {ESP, TAB, CR, NL}",
        ),
        expressao_formal="rEspaço = B+ ≡ B B*",
        regex=r"[ \t\r\n]+",
        acao=Acao.IGNORA,
        tipo=TokenType.WHITESPACE,
    ),
    ClasseLexica(
        nome="KEYWORD_EXT",
        linguagem_finita=True,
        finalidade="Palavras reservadas das extensões; reclassificam um lexema de IDENT_BASE, "
                   "na mesma relação de KEYWORD_CORE: ifx continua IDENT.",
        descricao="As três palavras que as extensões reservam para controle de fluxo.",
        exemplos=("if", "else", "while"),
        definicao_matematica='L_KeywordExt = RExt = {"if", "else", "while"}',
        expressao_formal='rKeywordExt = "if" ∪ "else" ∪ "while"',
        regex=r"if|else|while",
        acao=Acao.RECLASSIFICA,
        tipo_por_lexema={
            "if": TokenType.KW_IF,
            "else": TokenType.KW_ELSE,
            "while": TokenType.KW_WHILE,
        },
    ),
    ClasseLexica(
        nome="REL_OP",
        linguagem_finita=True,
        finalidade="Família dos operadores relacionais; gera EQ, NE, LT, LE, GT e GE. "
                   "'!' sozinho não pertence à classe; '=>' tampouco.",
        descricao="Um dos seis operadores de comparação, de um ou dois caracteres.",
        exemplos=("==", "!=", "<", "<=", ">", ">="),
        definicao_matematica='L_RelOp = {"==", "!=", "<", "<=", ">", ">="}',
        expressao_formal='rRel = "==" ∪ "!=" ∪ "<=" ∪ ">=" ∪ "<" ∪ ">"',
        regex=r"==|!=|<=|>=|<|>",
        acao=Acao.EMITE,
        tipo_por_lexema={
            "==": TokenType.EQ,
            "!=": TokenType.NE,
            "<": TokenType.LT,
            "<=": TokenType.LE,
            ">": TokenType.GT,
            ">=": TokenType.GE,
        },
    ),
    ClasseLexica(
        nome="BLOCK_DELIMITER",
        linguagem_finita=True,
        finalidade="Delimitadores de bloco das extensões. Como DELIMITER_CORE, '{}' são "
                   "dois lexemas, não um.",
        descricao="Chave de abertura ou chave de fechamento, cada uma como um lexema isolado.",
        exemplos=("{", "}"),
        definicao_matematica='L_BlockDelimiter = DBloco = {"{", "}"}',
        expressao_formal='rBloco = "{" ∪ "}"',
        regex=r"[{}]",
        acao=Acao.EMITE,
        tipo_por_lexema={
            "{": TokenType.LBRACE,
            "}": TokenType.RBRACE,
        },
    ),
]
