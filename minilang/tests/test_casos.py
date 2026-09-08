"""Confronta cada caso do catalogo com o reconhecedor da classe (slides 95 e 96)."""

from collections import Counter

from ..spec.casos import CASOS, Categoria
from ..spec.tabela import TABELA_LEXICA

CLASSES = {classe.nome: classe for classe in TABELA_LEXICA}

MINIMOS_FINITA = {"rejeitadas": 3, "fronteiras": 2}
MINIMOS_INFINITA = {"aceitas": 4, "rejeitadas": 4, "fronteiras": 2}


def contagem(nome: str) -> Counter:
    casos = [caso for caso in CASOS if caso.classe == nome]
    return Counter(
        aceitas=sum(1 for caso in casos if caso.aceita),
        rejeitadas=sum(1 for caso in casos if not caso.aceita),
        fronteiras=sum(1 for caso in casos if caso.categoria is Categoria.FRONTEIRA),
    )


def test_esperado_bate_com_obtido():
    """A decisao e por correspondencia completa, nunca por busca (slide 95)."""
    for caso in CASOS:
        obtido = CLASSES[caso.classe].padrao.fullmatch(caso.entrada) is not None
        assert obtido == caso.aceita, f"{caso.classe} com {caso.entrada!r}: {caso.justificativa}"


def test_minimos_do_slide_96():
    """Linguagem finita e infinita tem exigencias diferentes de cobertura."""
    for nome in {caso.classe for caso in CASOS}:
        atual = contagem(nome)
        exigido = MINIMOS_FINITA if CLASSES[nome].linguagem_finita else MINIMOS_INFINITA
        for chave, minimo in exigido.items():
            assert atual[chave] >= minimo, f"{nome}: {atual[chave]} {chave}, minimo {minimo}"


def test_classe_finita_testa_todas_as_palavras():
    """Slide 96: em linguagem finita, enumere e teste a linguagem inteira."""
    for nome in {caso.classe for caso in CASOS}:
        classe = CLASSES[nome]
        if not classe.linguagem_finita:
            continue
        aceitas = {caso.entrada for caso in CASOS if caso.classe == nome and caso.aceita}
        assert aceitas == set(classe.exemplos), f"{nome}: falta testar {set(classe.exemplos) - aceitas}"
