"""Roda a suite de interacoes do slide 98 e os gabaritos dos slides 82 e 84 - aula 03"""

import pytest

from ..analise.erros import ErroLexico
from ..analise.lexer import tokenizar
from ..spec.interacoes import EXERCICIO_10, EXERCICIO_11, INTERACOES, Bloco
from ..spec.tabela import TABELA_LEXICA, Acao

TIPOS_IGNORADOS = {classe.tipo for classe in TABELA_LEXICA if classe.acao is Acao.IGNORA}


def separa(entrada: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Devolve o que vai ao parser e o que e reconhecido e descartado (slide 79)."""
    tokens = tokenizar(entrada, True)
    return (
        tuple(t.tipo.value for t in tokens if t.tipo not in TIPOS_IGNORADOS),
        tuple(t.tipo.value for t in tokens if t.tipo in TIPOS_IGNORADOS),
    )


def confere(interacao) -> None:
    if interacao.erro_na_posicao is not None:
        with pytest.raises(ErroLexico) as erro:
            tokenizar(interacao.entrada)
        assert erro.value.pos == interacao.erro_na_posicao, interacao.justificativa
        return

    emitidos, ignorados = separa(interacao.entrada)
    assert emitidos == interacao.emitidos, f"{interacao.entrada!r}: {interacao.justificativa}"
    assert ignorados == interacao.ignorados, f"{interacao.entrada!r}: {interacao.justificativa}"


def test_todas_as_interacoes():
    for interacao in INTERACOES:
        confere(interacao)


def test_os_oito_blocos_estao_cobertos():
    """Slide 98 lista oito situacoes obrigatorias; nenhuma pode faltar."""
    cobertos = {interacao.bloco for interacao in INTERACOES}
    assert cobertos == set(Bloco), f"faltam {set(Bloco) - cobertos}"


def test_exercicio_10():
    """Gabarito do slide 82 - Aula 03."""
    confere(EXERCICIO_10)


def test_exercicio_11():
    """Gabarito do slide 84 - Aula 03."""
    confere(EXERCICIO_11)
