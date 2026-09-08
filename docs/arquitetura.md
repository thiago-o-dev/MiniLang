# Arquitetura

A tabela léxica é dado. O lexer a percorre sem conter o nome de nenhuma classe
nem de nenhum token: acrescentar uma classe é acrescentar uma linha em
`tabela.py`.

## Estrutura de arquivos

```
minilang/
├── spec/
│   ├── alfabeto.py     ΣFonte e os conjuntos derivados (slides 70, 76, 77)
│   ├── tokens.py       TokenType e o registro Token
│   ├── tabela.py       As 11 classes, com os 9 itens do slide 90
│   ├── casos.py        86 casos por classe, colunas do slide 96
│   └── interacoes.py   28 interações nos 8 blocos do slide 98
│
├── analise/
│   ├── lexer.py        tokenizar(): maior lexema + reclassificação
│   └── erros.py        ErroLexico, com posição e motivo
│
├── tests/              Cinco arquivos (ver como-rodar.md)
└── __main__.py         Linha de comando
```

## Duas decisões

**Conflito de prefixo se resolve por maior lexema.** `/` e `//`, `=` e `==`,
`int` e `intx` (slide 80). O lexer tenta todas as classes na posição atual e
fica com o casamento mais longo. A ordem das linhas na tabela só desempataria
padrões de mesmo comprimento, e não há nenhum.

**Palavra reservada reclassifica, não varre.** `KEYWORD_CORE` e `KEYWORD_EXT`
ficam fora da varredura: o lexer reconhece `int` como `IDENT_BASE` e depois
pergunta se o lexema inteiro é reservado (slide 72). É o que faz `intx`
continuar `IDENT`.
