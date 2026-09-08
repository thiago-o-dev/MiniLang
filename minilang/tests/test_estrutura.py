import pytest

from ..analise.erros import ErroLexico
from ..analise.lexer import tokenizar
from ..spec.tabela import TABELA_LEXICA

FORA_DO_ALFABETO = [
    ("tot@l", 3),
    ("a#b", 1),
    ("valor $ 2", 6),
    ("%", 0),
]


def test_palavra_vazia_rejeitada():
    """Se alguma classe aceitasse a palavra vazia, o cursor do lexer nao avancaria."""
    for classe in TABELA_LEXICA:
        assert classe.padrao.fullmatch("") is None, classe.nome


def test_simbolo_fora_do_alfabeto():
    """Simbolo fora do alfabeto-fonte levanta ErroLexico na posicao exata."""
    for fonte, pos in FORA_DO_ALFABETO:
        with pytest.raises(ErroLexico) as erro:
            tokenizar(fonte)
        assert erro.value.pos == pos, f"{fonte!r} apontou {erro.value.pos}"
