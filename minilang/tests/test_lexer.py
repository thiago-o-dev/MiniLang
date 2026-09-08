"""O lexer sobre um trecho de fonte, no que casos.py e interacoes.py nao cobrem."""

import pytest

from ..analise.erros import ErroLexico
from ..analise.lexer import tokenizar

FORA_DO_ALFABETO = [
    ("tot@l", 3),
    ("a#b", 1),
    ("valor $ 2", 6),
    ("%", 0),
]


def test_fonte_vazia_nao_produz_token():
    """Fonte vazia e um programa valido de zero tokens, nao um erro lexico."""
    assert tokenizar("") == []


def test_posicao_e_o_indice_do_lexema_na_fonte():
    assert [token.pos for token in tokenizar("x = 50")] == [0, 2, 4]


def test_arith_op_gera_os_quatro_tipos():
    """Slide 79 - Aula 03: a familia ARITH_OP gera PLUS, MINUS, STAR e SLASH."""
    tipos = [token.tipo.value for token in tokenizar("a + b - c * d / e")]
    assert tipos[1::2] == ["PLUS", "MINUS", "STAR", "SLASH"]


def test_simbolo_fora_do_alfabeto():
    """Simbolo fora do alfabeto-fonte levanta ErroLexico na posicao exata."""
    for fonte, pos in FORA_DO_ALFABETO:
        with pytest.raises(ErroLexico) as erro:
            tokenizar(fonte)
        assert erro.value.pos == pos, f"{fonte!r} apontou {erro.value.pos}"
