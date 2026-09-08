from ..spec.tabela import TABELA_LEXICA, Acao, ClasseLexica
from ..spec.tokens import Token, TokenType
from .erros import ErroLexico

VARREDURA = [classe for classe in TABELA_LEXICA if classe.acao is not Acao.RECLASSIFICA]
RECLASSIFICADORAS = [classe for classe in TABELA_LEXICA if classe.acao is Acao.RECLASSIFICA]


def tokenizar(fonte: str, incluir_ignorados: bool = False) -> list[Token]:

    tokens: list[Token] = []
    pos = 0

    while pos < len(fonte):
        classe, lexema = _maior_lexema(fonte, pos)

        if incluir_ignorados or classe.acao is Acao.EMITE:
            tokens.append(Token(_tipo_final(classe, lexema), lexema, pos))

        pos += len(lexema)

    return tokens


def _tipo_final(classe: ClasseLexica, lexema: str) -> TokenType:

    for reclassificadora in RECLASSIFICADORAS:
        if reclassificadora.padrao.fullmatch(lexema):
            return reclassificadora.tipo_de(lexema)

    return classe.tipo_de(lexema)


def _maior_lexema(fonte: str, pos: int) -> tuple[ClasseLexica, str]:

    classe_vencedora, lexema_vencedor = None, ""

    for classe in VARREDURA:
        casamento = classe.padrao.match(fonte, pos)

        # Vence o maior lexema - caso  empate, a classe declarada primeiro
        if casamento and len(casamento.group()) > len(lexema_vencedor):
            classe_vencedora, lexema_vencedor = classe, casamento.group()

    if classe_vencedora is None:
        raise ErroLexico(fonte[pos], pos)
    
    return classe_vencedora, lexema_vencedor
