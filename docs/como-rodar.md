# Como rodar

## Requisitos

Python 3.10 ou mais novo. A única dependência é o `pytest`, usado só nos testes.

## Instalação

A partir da raiz do repositório:

```bash
python -m venv .venv
```

```powershell
.\.venv\Scripts\activate      # Windows, PowerShell
```

```bash
source .venv/bin/activate     # Linux, macOS ou Git Bash
```

```bash
pip install -r minilang/requirements.txt
```

## Rodar o lexer

```bash
python -m minilang
```

```
MiniLang> int x = 40 + 2;
   0  KW_INT        'int'
   4  IDENT         'x'
   6  ASSIGN        '='
   8  INT_LITERAL   '40'
  11  PLUS          '+'
  13  INT_LITERAL   '2'
  14  SEMICOLON     ';'
```

A primeira coluna é a posição no texto-fonte. Espaços e comentários não
aparecem: são reconhecidos e descartados (slide 79).

```
MiniLang> print(a @ 2);
posicao 8: '@' fora do alfabeto-fonte
```

## Rodar os testes

```bash
python testes.py     # verificação da entrega (slide 99): termina com SUCESSO ou FALHA
pytest               # mesma suíte, saída crua do pytest
```

| Arquivo | O que verifica |
| --- | --- |
| `test_conformidade.py` | O catálogo: 11 classes, 9 itens preenchidos, nenhuma sem caso de teste |
| `test_casos.py` | Os casos por classe do slide 96, nos mínimos exigidos |
| `test_interacoes.py` | Os oito blocos do slide 98 e os Exercícios 10 e 11 |
| `test_lexer.py` | O lexer: posição, fonte vazia, família ARITH_OP, alfabeto |
