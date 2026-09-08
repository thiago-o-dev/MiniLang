"""Casos de teste por classe, com as colunas que o slide 96 - aula 03 exige"""

from dataclasses import dataclass
from enum import Enum


class Categoria(Enum):
    COMUM = "Comum"
    FRONTEIRA = "Fronteira"


@dataclass(frozen=True)
class Caso:
    classe: str
    entrada: str
    aceita: bool
    categoria: Categoria
    justificativa: str


CASOS: list[Caso] = [
    # KEYWORD_CORE - finita: as duas palavras, mais rejeicoes e fronteiras.
    Caso("KEYWORD_CORE", "int", True, Categoria.FRONTEIRA, "Menor palavra da classe e uma das duas únicas."),
    Caso("KEYWORD_CORE", "print", True, Categoria.COMUM, "A outra palavra reservada do núcleo."),
    Caso("KEYWORD_CORE", "in", False, Categoria.FRONTEIRA, "Um símbolo a menos que 'int': pertence a L_IdentBase, não aqui."),
    Caso("KEYWORD_CORE", "intx", False, Categoria.FRONTEIRA, "Um símbolo a mais: intx ≠ int, então segue IDENT (slide 84 - Aula 03)."),
    Caso("KEYWORD_CORE", "Int", False, Categoria.COMUM, "Maiúsculas e minúsculas são diferentes (slide 67 - Aula 03)."),
    Caso("KEYWORD_CORE", "", False, Categoria.FRONTEIRA, "ε não pertence: a grafia tem que ser exata."),

    # IDENT_BASE - infinita.
    Caso("IDENT_BASE", "_", True, Categoria.FRONTEIRA, "Menor palavra válida: só o inicial, com continuação vazia."),
    Caso("IDENT_BASE", "A1", True, Categoria.COMUM, "Inicial seguido de um dígito."),
    Caso("IDENT_BASE", "total2", True, Categoria.COMUM, "Letras e dígito na continuação."),
    Caso("IDENT_BASE", "resultado", True, Categoria.COMUM, "Continuação formada só por letras."),
    Caso("IDENT_BASE", "intx", True, Categoria.FRONTEIRA, "Um símbolo a mais que 'int' devolve a palavra a esta classe."),
    Caso("IDENT_BASE", "", False, Categoria.FRONTEIRA, "O inicial é obrigatório: ε não pertence."),
    Caso("IDENT_BASE", "2total", False, Categoria.FRONTEIRA, "Dígito não pode ser o inicial (slide 67 - Aula 03)."),
    Caso("IDENT_BASE", "total-2", False, Categoria.COMUM, "O hífen não está em Continuação; são três lexemas."),
    Caso("IDENT_BASE", "á", False, Categoria.FRONTEIRA, "Acento fica fora da MiniLang-Core (slide 67 - Aula 03)."),

    # INT_LITERAL - infinita.
    Caso("INT_LITERAL", "0", True, Categoria.FRONTEIRA, "Menor literal válido, com um único dígito."),
    Caso("INT_LITERAL", "7", True, Categoria.COMUM, "Um dígito qualquer."),
    Caso("INT_LITERAL", "45", True, Categoria.COMUM, "Uma ou mais ocorrências de dígito."),
    Caso("INT_LITERAL", "007", True, Categoria.COMUM, "Zeros à esquerda são permitidos (slide 67 - Aula 03)."),
    Caso("INT_LITERAL", "1234567890", True, Categoria.COMUM, "Os dez dígitos, para cobrir todo o conjunto Dígito."),
    Caso("INT_LITERAL", "", False, Categoria.FRONTEIRA, "Dígito+ exige ao menos um dígito: ε não pertence."),
    Caso("INT_LITERAL", "-10", False, Categoria.COMUM, "O sinal não pertence ao literal; forma MINUS e INT_LITERAL."),
    Caso("INT_LITERAL", "12a", False, Categoria.FRONTEIRA, "Um símbolo a mais, fora de Dígito, e a palavra inteira falha."),
    Caso("INT_LITERAL", "1 2", False, Categoria.COMUM, "O espaço separa dois literais; não é uma palavra só."),
    Caso("INT_LITERAL", "a", False, Categoria.COMUM, "Nenhum dígito: pertence a L_IdentBase, não a esta classe."),

    # ASSIGN - finita: uma unica palavra.
    Caso("ASSIGN", "=", True, Categoria.FRONTEIRA, "Única palavra da linguagem, logo também a menor."),
    Caso("ASSIGN", "==", False, Categoria.FRONTEIRA, "Um símbolo a mais muda a classe: '==' pertence a L_RelOp."),
    Caso("ASSIGN", "", False, Categoria.FRONTEIRA, "ε não pertence."),
    Caso("ASSIGN", "=>", False, Categoria.COMUM, "Os dois símbolos existem, mas a sequência não é palavra da classe."),
    Caso("ASSIGN", ":=", False, Categoria.COMUM, "Atribuição de outras linguagens; ':' nem está no alfabeto-fonte."),

    # ARITH_OP - finita: os quatro operadores.
    Caso("ARITH_OP", "+", True, Categoria.COMUM, "Soma."),
    Caso("ARITH_OP", "-", True, Categoria.COMUM, "Subtração; também aparece antes de literal, mas sempre como lexema próprio."),
    Caso("ARITH_OP", "*", True, Categoria.COMUM, "Multiplicação."),
    Caso("ARITH_OP", "/", True, Categoria.FRONTEIRA, "Prefixo de '//': uma barra sozinha é divisão."),
    Caso("ARITH_OP", "//", False, Categoria.FRONTEIRA, "Um símbolo a mais inicia comentário (slide 74 - Aula 03)."),
    Caso("ARITH_OP", "", False, Categoria.FRONTEIRA, "ε não pertence."),
    Caso("ARITH_OP", "+-", False, Categoria.COMUM, "Dois operadores adjacentes são dois lexemas."),
    Caso("ARITH_OP", "%", False, Categoria.COMUM, "Resto não existe na MiniLang; '%' está fora do alfabeto-fonte."),

    # DELIMITER_CORE - finita: os tres delimitadores.
    Caso("DELIMITER_CORE", "(", True, Categoria.COMUM, "Abertura de parênteses."),
    Caso("DELIMITER_CORE", ")", True, Categoria.COMUM, "Fechamento de parênteses."),
    Caso("DELIMITER_CORE", ";", True, Categoria.COMUM, "Fim de comando."),
    Caso("DELIMITER_CORE", "()", False, Categoria.FRONTEIRA, "Um símbolo a mais: '()' pertence a L_DelimiterCore², são dois lexemas."),
    Caso("DELIMITER_CORE", ");", False, Categoria.COMUM, "Delimitadores adjacentes continuam sendo dois lexemas."),
    Caso("DELIMITER_CORE", "", False, Categoria.FRONTEIRA, "ε não pertence."),
    Caso("DELIMITER_CORE", "{", False, Categoria.COMUM, "Chave pertence a L_BlockDelimiter, não ao núcleo."),

    # LINE_COMMENT - infinita.
    Caso("LINE_COMMENT", "//", True, Categoria.FRONTEIRA, "Menor palavra válida: corpo vazio é permitido."),
    Caso("LINE_COMMENT", "//x", True, Categoria.COMUM, "Um caractere no corpo."),
    Caso("LINE_COMMENT", "// comentário", True, Categoria.COMUM, "Espaços são permitidos no corpo."),
    Caso("LINE_COMMENT", "////", True, Categoria.COMUM, "As duas últimas barras pertencem ao corpo."),
    Caso("LINE_COMMENT", "/", False, Categoria.FRONTEIRA, "Um símbolo a menos: uma barra sozinha é ARITH_OP."),
    Caso("LINE_COMMENT", "/x", False, Categoria.COMUM, "Não começa por '//'."),
    Caso("LINE_COMMENT", "", False, Categoria.FRONTEIRA, "ε não pertence: o '//' é obrigatório."),
    Caso("LINE_COMMENT", "//a\nb", False, Categoria.FRONTEIRA, "A quebra encerra o comentário; '//a' seria lexema separado."),
    Caso("LINE_COMMENT", "x//", False, Categoria.COMUM, "O comentário tem que começar no início do lexema."),

    # WHITESPACE - infinita.
    Caso("WHITESPACE", " ", True, Categoria.FRONTEIRA, "Menor palavra válida: uma única ocorrência."),
    Caso("WHITESPACE", "\t", True, Categoria.COMUM, "Tabulação também pertence a B."),
    Caso("WHITESPACE", "  ", True, Categoria.COMUM, "Várias ocorrências do mesmo caractere."),
    Caso("WHITESPACE", " \t\n", True, Categoria.COMUM, "Combinação de espaço, tabulação e nova linha."),
    Caso("WHITESPACE", "\r\n", True, Categoria.COMUM, "CR e NL, a quebra de linha do Windows."),
    Caso("WHITESPACE", "", False, Categoria.FRONTEIRA, "B+ exige ao menos um caractere: ε não pertence."),
    Caso("WHITESPACE", "a", False, Categoria.COMUM, "Letra não pertence a B."),
    Caso("WHITESPACE", " a", False, Categoria.FRONTEIRA, "Um símbolo fora de B faz a palavra inteira falhar."),
    Caso("WHITESPACE", "\v", False, Categoria.COMUM, "Tabulação vertical não está em B nem no alfabeto-fonte."),

    # KEYWORD_EXT - finita: as tres palavras.
    Caso("KEYWORD_EXT", "if", True, Categoria.FRONTEIRA, "Menor palavra da classe, com dois caracteres."),
    Caso("KEYWORD_EXT", "else", True, Categoria.COMUM, "Alternativa do condicional."),
    Caso("KEYWORD_EXT", "while", True, Categoria.COMUM, "Repetição."),
    Caso("KEYWORD_EXT", "ifx", False, Categoria.FRONTEIRA, "Um símbolo a mais: 'ifx' segue IDENT (slide 98 - Aula 03)."),
    Caso("KEYWORD_EXT", "els", False, Categoria.FRONTEIRA, "Um símbolo a menos que 'else'."),
    Caso("KEYWORD_EXT", "IF", False, Categoria.COMUM, "Maiúsculas e minúsculas são diferentes."),
    Caso("KEYWORD_EXT", "", False, Categoria.FRONTEIRA, "ε não pertence."),

    # REL_OP - finita: as seis palavras.
    Caso("REL_OP", "==", True, Categoria.COMUM, "Igualdade, o primeiro dos seis operadores."),
    Caso("REL_OP", "!=", True, Categoria.COMUM, "Diferença, única palavra da classe que começa por '!'."),
    Caso("REL_OP", "<=", True, Categoria.COMUM, "Menor ou igual, de dois caracteres."),
    Caso("REL_OP", ">=", True, Categoria.COMUM, "Maior ou igual, de dois caracteres."),
    Caso("REL_OP", "<", True, Categoria.FRONTEIRA, "Menor palavra válida da classe, com um caractere."),
    Caso("REL_OP", ">", True, Categoria.FRONTEIRA, "A outra palavra de um caractere só."),
    Caso("REL_OP", "!", False, Categoria.FRONTEIRA, "Um símbolo a menos que '!=': '!' sozinho não pertence."),
    Caso("REL_OP", "=>", False, Categoria.COMUM, "Os dois símbolos existem, mas nessa ordem não formam palavra."),
    Caso("REL_OP", "=", False, Categoria.FRONTEIRA, "Pertence a L_Assign; um '=' a mais é que faz virar REL_OP."),
    Caso("REL_OP", "<==", False, Categoria.FRONTEIRA, "Um símbolo a mais que '<=' sai da linguagem."),
    Caso("REL_OP", "", False, Categoria.FRONTEIRA, "ε não pertence a L_RelOp."),

    # BLOCK_DELIMITER - finita: as duas chaves.
    Caso("BLOCK_DELIMITER", "{", True, Categoria.COMUM, "Abertura de bloco."),
    Caso("BLOCK_DELIMITER", "}", True, Categoria.COMUM, "Fechamento de bloco."),
    Caso("BLOCK_DELIMITER", "{}", False, Categoria.FRONTEIRA, "Um símbolo a mais: são dois lexemas, não um."),
    Caso("BLOCK_DELIMITER", "", False, Categoria.FRONTEIRA, "ε não pertence."),
    Caso("BLOCK_DELIMITER", "(", False, Categoria.COMUM, "Parêntese pertence a L_DelimiterCore, não às extensões."),
]
