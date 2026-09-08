"""Verificacao da entrega (slide 99 - Aula 03).

    python testes.py
"""

import sys

import pytest

if __name__ == "__main__":
    codigo = pytest.main(["-q", "minilang/tests"])

    if codigo == 0:
        print("\nSUCESSO: o catalogo passou em todos os testes.")
    else:
        print("\nFALHA: veja acima o caso que falhou.")

    sys.exit(codigo)
