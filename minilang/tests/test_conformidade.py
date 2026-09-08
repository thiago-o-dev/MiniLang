"""Cobra do catalogo o que os slides 88, 89, 90 e 96 exigem - aula 03"""

from ..spec.casos import CASOS
from ..spec.tabela import TABELA_LEXICA

CLASSES = {classe.nome: classe for classe in TABELA_LEXICA}

CLASSES_EXIGIDAS = {
    # Slide 88 - MiniLang-Core
    "KEYWORD_CORE", "IDENT_BASE", "INT_LITERAL", "ASSIGN",
    "ARITH_OP", "DELIMITER_CORE", "LINE_COMMENT", "WHITESPACE",
    # Slide 89 - extensoes
    "KEYWORD_EXT", "REL_OP", "BLOCK_DELIMITER",
}

ITENS_OBRIGATORIOS = (
    "finalidade", "descricao", "exemplos",
    "definicao_matematica", "expressao_formal", "regex",
)


def test_as_onze_classes_do_slide_88_e_89():
    assert set(CLASSES) == CLASSES_EXIGIDAS, (
        f"faltam {CLASSES_EXIGIDAS - set(CLASSES)}; sobram {set(CLASSES) - CLASSES_EXIGIDAS}"
    )


def test_nenhum_item_obrigatorio_vazio():
    """Slide 90: a secao de cada classe tem nove itens, e nenhum e opcional."""
    for classe in TABELA_LEXICA:
        for item in ITENS_OBRIGATORIOS:
            assert getattr(classe, item), f"{classe.nome} esta sem {item}"


def test_exemplo_pertence_a_propria_classe():
    """Slide 90, item 3: os exemplos sao palavras que pertencem a linguagem."""
    for classe in TABELA_LEXICA:
        for exemplo in classe.exemplos:
            assert classe.padrao.fullmatch(exemplo), f"{classe.nome} rejeita {exemplo!r}"


def test_toda_classe_tem_caso_de_teste():
    """Slide 96 pede a suite por classe; nenhuma pode ficar de fora."""
    testadas = {caso.classe for caso in CASOS}
    assert set(CLASSES) <= testadas, f"sem caso de teste: {set(CLASSES) - testadas}"
