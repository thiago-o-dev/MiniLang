# MiniLang - Catálogo Léxico

Especificação léxica completa da MiniLang: as 11 classes definidas na Aula 03,
com definição matemática, expressão regular formal, implementação executável e
suíte de testes.

> Para instalar, rodar o lexer e entender a arquitetura, veja **[docs/](docs/)**.
> Este arquivo é o catálogo em si.

---

## 1. Integrantes e identificação do grupo

<!-- PREENCHER: nome completo e matrícula de cada integrante -->

| Integrante | Matrícula |
| --- | --- |
| _a preencher_ | _a preencher_ |

**Disciplina:** Compiladores - Aula 03, Expressões Regulares e Especificação
Léxica da MiniLang.

---

## 2. Tabela geral das 11 classes

Oito classes da MiniLang-Core (slide 88) e três das extensões (slide 89).

| Classe | Regex de Python | Ação |
| --- | --- | --- |
| KEYWORD_CORE | `int\|print` | reclassificar |
| IDENT_BASE | `[A-Za-z_][A-Za-z0-9_]*` | emitir |
| INT_LITERAL | `[0-9]+` | emitir |
| ASSIGN | `=` | emitir |
| ARITH_OP | `[-+*/]` | emitir |
| DELIMITER_CORE | `[();]` | emitir |
| LINE_COMMENT | `//[^\r\n]*` | ignorar |
| WHITESPACE | `[ \t\r\n]+` | ignorar |
| KEYWORD_EXT | `if\|else\|while` | reclassificar |
| REL_OP | `==\|!=\|<=\|>=\|<\|>` | emitir |
| BLOCK_DELIMITER | `[{}]` | emitir |

As classes com ação **reclassificar** não participam da varredura: elas
reclassificam um lexema já reconhecido como `IDENT_BASE` (slide 72).

---

## 3. As classes, uma a uma

Cada seção segue os nove itens do slide 90. A coluna **Obtido** é conferida
por `re.fullmatch` (slide 95) a cada execução de `pytest`.

### KEYWORD_CORE

**Finalidade léxica:** Palavras reservadas do núcleo; reclassificam um lexema de IDENT_BASE. Linguagem finita contida em L_IdentBase: só o lexema inteiro reclassifica.

**Descrição:** As duas únicas palavras que a MiniLang-Core reserva. Nenhuma outra palavra pertence a classe, e a grafia tem que ser exata.

**Exemplos aceitos:** `int`, `print`

**Definição matemática:**

```
L_KeywordCore = RCore = {"int", "print"}
```

**Expressão regular formal:**

```
rKeywordCore = "int" ∪ "print"
```

**Regex de Python:** `r"int|print"`

**Ação do lexer:** reclassificar

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `int` | Aceita | Aceita | Fronteira | Menor palavra da classe e uma das duas únicas. |
| `print` | Aceita | Aceita | Comum | A outra palavra reservada do núcleo. |
| `in` | Rejeita | Rejeita | Fronteira | Um símbolo a menos que 'int': pertence a L_IdentBase, não aqui. |
| `intx` | Rejeita | Rejeita | Fronteira | Um símbolo a mais: intx ≠ int, então segue IDENT (slide 84 - Aula 03). |
| `Int` | Rejeita | Rejeita | Comum | Maiúsculas e minúsculas são diferentes (slide 67 - Aula 03). |
| `ε` | Rejeita | Rejeita | Fronteira | ε não pertence: a grafia tem que ser exata. |

### IDENT_BASE

**Finalidade léxica:** Padrão-base dos identificadores: produz os candidatos que as classes de palavra reservada podem reclassificar.

**Descrição:** Uma letra ou um underscore, seguido de zero ou mais letras, dígitos ou underscores. Maiúsculas e minúsculas são diferentes.

**Exemplos aceitos:** `_`, `A1`, `total2`, `resultado`, `intx`

**Definição matemática:**

```
L_IdentBase = {c_0 c_1 ... c_n | n ≥ 0, c_0 ∈ Inicial e c_i ∈ Continuação para 1 ≤ i ≤ n}
```

**Conjuntos auxiliares:**

- `Letra = a ∪ ... ∪ z ∪ A ∪ ... ∪ Z`
- `Dígito = 0 ∪ 1 ∪ ... ∪ 9`
- `Inicial = Letra ∪ "_"`
- `Continuação = Letra ∪ Dígito ∪ "_"`

**Expressão regular formal:**

```
rIdentBase = Inicial Continuação*
```

**Regex de Python:** `r"[A-Za-z_][A-Za-z0-9_]*"`

**Ação do lexer:** emitir

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `_` | Aceita | Aceita | Fronteira | Menor palavra válida: só o inicial, com continuação vazia. |
| `A1` | Aceita | Aceita | Comum | Inicial seguido de um dígito. |
| `total2` | Aceita | Aceita | Comum | Letras e dígito na continuação. |
| `resultado` | Aceita | Aceita | Comum | Continuação formada só por letras. |
| `intx` | Aceita | Aceita | Fronteira | Um símbolo a mais que 'int' devolve a palavra a esta classe. |
| `ε` | Rejeita | Rejeita | Fronteira | O inicial é obrigatório: ε não pertence. |
| `2total` | Rejeita | Rejeita | Fronteira | Dígito não pode ser o inicial (slide 67 - Aula 03). |
| `total-2` | Rejeita | Rejeita | Comum | O hífen não está em Continuação; são três lexemas. |
| `á` | Rejeita | Rejeita | Fronteira | Acento fica fora da MiniLang-Core (slide 67 - Aula 03). |

### INT_LITERAL

**Finalidade léxica:** Literais inteiros sem sinal: -10 é a sequência MINUS INT_LITERAL, não um literal.

**Descrição:** Uma ou mais ocorrências de dígito. Zeros à esquerda são permitidos, e o sinal não faz parte do literal.

**Exemplos aceitos:** `0`, `7`, `45`, `007`

**Definição matemática:**

```
L_IntLiteral = {d_1 d_2 ... d_n | n ≥ 1 e d_i ∈ Dígito}
```

**Conjuntos auxiliares:**

- `Dígito = 0 ∪ 1 ∪ ... ∪ 9`

**Expressão regular formal:**

```
rNum = Dígito+ ≡ Dígito Dígito*
```

**Regex de Python:** `r"[0-9]+"`

**Ação do lexer:** emitir

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `0` | Aceita | Aceita | Fronteira | Menor literal válido, com um único dígito. |
| `7` | Aceita | Aceita | Comum | Um dígito qualquer. |
| `45` | Aceita | Aceita | Comum | Uma ou mais ocorrências de dígito. |
| `007` | Aceita | Aceita | Comum | Zeros à esquerda são permitidos (slide 67 - Aula 03). |
| `1234567890` | Aceita | Aceita | Comum | Os dez dígitos, para cobrir todo o conjunto Dígito. |
| `ε` | Rejeita | Rejeita | Fronteira | Dígito+ exige ao menos um dígito: ε não pertence. |
| `-10` | Rejeita | Rejeita | Comum | O sinal não pertence ao literal; forma MINUS e INT_LITERAL. |
| `12a` | Rejeita | Rejeita | Fronteira | Um símbolo a mais, fora de Dígito, e a palavra inteira falha. |
| `1 2` | Rejeita | Rejeita | Comum | O espaço separa dois literais; não é uma palavra só. |
| `a` | Rejeita | Rejeita | Comum | Nenhum dígito: pertence a L_IdentBase, não a esta classe. |

### ASSIGN

**Finalidade léxica:** Operador de atribuição. Um '=' é atribuição; '==' pertence a REL_OP e casa um lexema mais longo.

**Descrição:** Linguagem finita de uma única palavra, o símbolo de igual sozinho.

**Exemplos aceitos:** `=`

**Definição matemática:**

```
L_Assign = {"="}
```

**Expressão regular formal:**

```
rAssign = "="
```

**Regex de Python:** `r"="`

**Ação do lexer:** emitir

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `=` | Aceita | Aceita | Fronteira | Única palavra da linguagem, logo também a menor. |
| `==` | Rejeita | Rejeita | Fronteira | Um símbolo a mais muda a classe: '==' pertence a L_RelOp. |
| `ε` | Rejeita | Rejeita | Fronteira | ε não pertence. |
| `=>` | Rejeita | Rejeita | Comum | Os dois símbolos existem, mas a sequência não é palavra da classe. |
| `:=` | Rejeita | Rejeita | Comum | Atribuição de outras linguagens; ':' nem está no alfabeto-fonte. |

### ARITH_OP

**Finalidade léxica:** Família dos operadores aritméticos; gera PLUS, MINUS, STAR e SLASH.

**Descrição:** Um dos quatro símbolos de operação aritmética, sempre um único caractere.

**Exemplos aceitos:** `+`, `-`, `*`, `/`

**Definição matemática:**

```
L_ArithOp = {"+", "-", "*", "/"}
```

**Expressão regular formal:**

```
rArith = "+" ∪ "-" ∪ "*" ∪ "/"
```

**Regex de Python:** `r"[-+*/]"`

**Ação do lexer:** emitir

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `+` | Aceita | Aceita | Comum | Soma. |
| `-` | Aceita | Aceita | Comum | Subtração; também aparece antes de literal, mas sempre como lexema próprio. |
| `*` | Aceita | Aceita | Comum | Multiplicação. |
| `/` | Aceita | Aceita | Fronteira | Prefixo de '//': uma barra sozinha é divisão. |
| `//` | Rejeita | Rejeita | Fronteira | Um símbolo a mais inicia comentário (slide 74 - Aula 03). |
| `ε` | Rejeita | Rejeita | Fronteira | ε não pertence. |
| `+-` | Rejeita | Rejeita | Comum | Dois operadores adjacentes são dois lexemas. |
| `%` | Rejeita | Rejeita | Comum | Resto não existe na MiniLang; '%' está fora do alfabeto-fonte. |

### DELIMITER_CORE

**Finalidade léxica:** Delimitadores do núcleo, que separam e agrupam construções. '()' não pertence à classe: é uma palavra de L_DelimiterCore².

**Descrição:** Parêntese de abertura, parêntese de fechamento ou ponto e vírgula, cada um como um lexema isolado.

**Exemplos aceitos:** `(`, `)`, `;`

**Definição matemática:**

```
L_DelimiterCore = DCore = {"(", ")", ";"}
```

**Expressão regular formal:**

```
rDelim = "(" ∪ ")" ∪ ";"
```

**Regex de Python:** `r"[();]"`

**Ação do lexer:** emitir

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `(` | Aceita | Aceita | Comum | Abertura de parênteses. |
| `)` | Aceita | Aceita | Comum | Fechamento de parênteses. |
| `;` | Aceita | Aceita | Comum | Fim de comando. |
| `()` | Rejeita | Rejeita | Fronteira | Um símbolo a mais: '()' pertence a L_DelimiterCore², são dois lexemas. |
| `);` | Rejeita | Rejeita | Comum | Delimitadores adjacentes continuam sendo dois lexemas. |
| `ε` | Rejeita | Rejeita | Fronteira | ε não pertence. |
| `{` | Rejeita | Rejeita | Comum | Chave pertence a L_BlockDelimiter, não ao núcleo. |

### LINE_COMMENT

**Finalidade léxica:** Comentário de linha; reconhecido e ignorado, nunca enviado ao parser. O corpo vazio é válido e a quebra encerra sem integrar o lexema.

**Descrição:** Começa com duas barras e segue até imediatamente antes da quebra de linha. O corpo pode ser vazio e a quebra não integra o lexema.

**Exemplos aceitos:** `//`, `//x`, `// comentário`, `////`

**Definição matemática:**

```
L_LineComment = {"//"w | w ∈ C*}
```

**Conjuntos auxiliares:**

- `ΣFonte = caracteres permitidos no arquivo-fonte`
- `CR = retorno de carro, NL = nova linha`
- `C = ΣFonte − {CR, NL}`

**Expressão regular formal:**

```
rComentário = "//" C*
```

**Regex de Python:** `r"//[^\r\n]*"`

**Ação do lexer:** ignorar

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `//` | Aceita | Aceita | Fronteira | Menor palavra válida: corpo vazio é permitido. |
| `//x` | Aceita | Aceita | Comum | Um caractere no corpo. |
| `// comentário` | Aceita | Aceita | Comum | Espaços são permitidos no corpo. |
| `////` | Aceita | Aceita | Comum | As duas últimas barras pertencem ao corpo. |
| `/` | Rejeita | Rejeita | Fronteira | Um símbolo a menos: uma barra sozinha é ARITH_OP. |
| `/x` | Rejeita | Rejeita | Comum | Não começa por '//'. |
| `ε` | Rejeita | Rejeita | Fronteira | ε não pertence: o '//' é obrigatório. |
| `//a\nb` | Rejeita | Rejeita | Fronteira | A quebra encerra o comentário; '//a' seria lexema separado. |
| `x//` | Rejeita | Rejeita | Comum | O comentário tem que começar no início do lexema. |

### WHITESPACE

**Finalidade léxica:** Separador de lexemas; reconhecido e ignorado, nunca enviado ao parser. Exige ao menos um caractere: ε ∉ L_Whitespace.

**Descrição:** Uma ou mais ocorrências de espaço, tabulação, retorno de carro ou nova linha, em qualquer combinação.

**Exemplos aceitos:** ` `, `\t`, `  `, ` \t\n`

**Definição matemática:**

```
L_Whitespace = {b_1 b_2 ... b_n | n ≥ 1 e b_i ∈ B}
```

**Conjuntos auxiliares:**

- `ESP = espaço, TAB = tabulação, CR = retorno de carro, NL = nova linha`
- `B = {ESP, TAB, CR, NL}`

**Expressão regular formal:**

```
rEspaço = B+ ≡ B B*
```

**Regex de Python:** `r"[ \t\r\n]+"`

**Ação do lexer:** ignorar

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| ` ` | Aceita | Aceita | Fronteira | Menor palavra válida: uma única ocorrência. |
| `\t` | Aceita | Aceita | Comum | Tabulação também pertence a B. |
| `  ` | Aceita | Aceita | Comum | Várias ocorrências do mesmo caractere. |
| ` \t\n` | Aceita | Aceita | Comum | Combinação de espaço, tabulação e nova linha. |
| `\r\n` | Aceita | Aceita | Comum | CR e NL, a quebra de linha do Windows. |
| `ε` | Rejeita | Rejeita | Fronteira | B+ exige ao menos um caractere: ε não pertence. |
| `a` | Rejeita | Rejeita | Comum | Letra não pertence a B. |
| ` a` | Rejeita | Rejeita | Fronteira | Um símbolo fora de B faz a palavra inteira falhar. |
| `\x0b` | Rejeita | Rejeita | Comum | Tabulação vertical não está em B nem no alfabeto-fonte. |

### KEYWORD_EXT

**Finalidade léxica:** Palavras reservadas das extensões; reclassificam um lexema de IDENT_BASE, na mesma relação de KEYWORD_CORE: ifx continua IDENT.

**Descrição:** As três palavras que as extensões reservam para controle de fluxo.

**Exemplos aceitos:** `if`, `else`, `while`

**Definição matemática:**

```
L_KeywordExt = RExt = {"if", "else", "while"}
```

**Expressão regular formal:**

```
rKeywordExt = "if" ∪ "else" ∪ "while"
```

**Regex de Python:** `r"if|else|while"`

**Ação do lexer:** reclassificar

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `if` | Aceita | Aceita | Fronteira | Menor palavra da classe, com dois caracteres. |
| `else` | Aceita | Aceita | Comum | Alternativa do condicional. |
| `while` | Aceita | Aceita | Comum | Repetição. |
| `ifx` | Rejeita | Rejeita | Fronteira | Um símbolo a mais: 'ifx' segue IDENT (slide 98 - Aula 03). |
| `els` | Rejeita | Rejeita | Fronteira | Um símbolo a menos que 'else'. |
| `IF` | Rejeita | Rejeita | Comum | Maiúsculas e minúsculas são diferentes. |
| `ε` | Rejeita | Rejeita | Fronteira | ε não pertence. |

### REL_OP

**Finalidade léxica:** Família dos operadores relacionais; gera EQ, NE, LT, LE, GT e GE. '!' sozinho não pertence à classe; '=>' tampouco.

**Descrição:** Um dos seis operadores de comparação, de um ou dois caracteres.

**Exemplos aceitos:** `==`, `!=`, `<`, `<=`, `>`, `>=`

**Definição matemática:**

```
L_RelOp = {"==", "!=", "<", "<=", ">", ">="}
```

**Expressão regular formal:**

```
rRel = "==" ∪ "!=" ∪ "<=" ∪ ">=" ∪ "<" ∪ ">"
```

**Regex de Python:** `r"==|!=|<=|>=|<|>"`

**Ação do lexer:** emitir

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `==` | Aceita | Aceita | Comum | Igualdade, o primeiro dos seis operadores. |
| `!=` | Aceita | Aceita | Comum | Diferença, única palavra da classe que começa por '!'. |
| `<=` | Aceita | Aceita | Comum | Menor ou igual, de dois caracteres. |
| `>=` | Aceita | Aceita | Comum | Maior ou igual, de dois caracteres. |
| `<` | Aceita | Aceita | Fronteira | Menor palavra válida da classe, com um caractere. |
| `>` | Aceita | Aceita | Fronteira | A outra palavra de um caractere só. |
| `!` | Rejeita | Rejeita | Fronteira | Um símbolo a menos que '!=': '!' sozinho não pertence. |
| `=>` | Rejeita | Rejeita | Comum | Os dois símbolos existem, mas nessa ordem não formam palavra. |
| `=` | Rejeita | Rejeita | Fronteira | Pertence a L_Assign; um '=' a mais é que faz virar REL_OP. |
| `<==` | Rejeita | Rejeita | Fronteira | Um símbolo a mais que '<=' sai da linguagem. |
| `ε` | Rejeita | Rejeita | Fronteira | ε não pertence a L_RelOp. |

### BLOCK_DELIMITER

**Finalidade léxica:** Delimitadores de bloco das extensões. Como DELIMITER_CORE, '{}' são dois lexemas, não um.

**Descrição:** Chave de abertura ou chave de fechamento, cada uma como um lexema isolado.

**Exemplos aceitos:** `{`, `}`

**Definição matemática:**

```
L_BlockDelimiter = DBloco = {"{", "}"}
```

**Expressão regular formal:**

```
rBloco = "{" ∪ "}"
```

**Regex de Python:** `r"[{}]"`

**Ação do lexer:** emitir

**Testes e interações:**

| Entrada | Esperado | Obtido | Categoria | Justificativa |
| --- | --- | --- | --- | --- |
| `{` | Aceita | Aceita | Comum | Abertura de bloco. |
| `}` | Aceita | Aceita | Comum | Fechamento de bloco. |
| `{}` | Rejeita | Rejeita | Fronteira | Um símbolo a mais: são dois lexemas, não um. |
| `ε` | Rejeita | Rejeita | Fronteira | ε não pertence. |
| `(` | Rejeita | Rejeita | Comum | Parêntese pertence a L_DelimiterCore, não às extensões. |

---

## 4. Casos de interação

As oito situações obrigatórias do slide 98. Aqui a entrada é um trecho de
programa, não uma palavra candidata a lexema único: o que se verifica é a
decisão do lexer diante de um conflito, não a pertinência a uma classe.

#### KEYWORD_CORE x IDENT_BASE

| Entrada | Emitidos ao parser | Ignorados | Justificativa |
| --- | --- | --- | --- |
| `int` | `KW_INT` | - | O lexema inteiro é a palavra reservada, entao reclassifica. |
| `intx` | `IDENT` | - | Maior lexema vence: IDENT_BASE casa 4 caracteres e KEYWORD_CORE só 3. |
| `print` | `KW_PRINT` | - | A outra reservada do nucleo, tambem por lexema inteiro. |
| `print2` | `IDENT` | - | Um digito no fim ja tira a palavra de RCore. |

#### KEYWORD_EXT x IDENT_BASE

| Entrada | Emitidos ao parser | Ignorados | Justificativa |
| --- | --- | --- | --- |
| `if` | `KW_IF` | - | Lexema inteiro pertence a RExt. |
| `ifx` | `IDENT` | - | Um caractere a mais e a palavra volta a ser identificador. |
| `else2` | `IDENT` | - | Digito na continuacao afasta de 'else'. |
| `while1` | `IDENT` | - | Mesma situacao de else2. |

#### ASSIGN x REL_OP

| Entrada | Emitidos ao parser | Ignorados | Justificativa |
| --- | --- | --- | --- |
| `=` | `ASSIGN` | - | Um so '=' é atribuicao. |
| `==` | `EQ` | - | Maior lexema: REL_OP casa dois caracteres, ASSIGN casaria um. |
| `===` | `EQ`, `ASSIGN` | - | O lexer consome '==' e sobra '=', que vira ASSIGN. |

#### ARITH_OP x LINE_COMMENT

| Entrada | Emitidos ao parser | Ignorados | Justificativa |
| --- | --- | --- | --- |
| `/` | `SLASH` | - | Uma barra sozinha é divisao. |
| `//` | - | `LINE_COMMENT` | Duas barras iniciam comentario, que é ignorado. |
| `//x` | - | `LINE_COMMENT` | O corpo segue ate a quebra de linha; nada e emitido. |

#### Prefixos de REL_OP

| Entrada | Emitidos ao parser | Ignorados | Justificativa |
| --- | --- | --- | --- |
| `<` | `LT` | - | Palavra de um caractere da classe. |
| `<=` | `LE` | - | Maior lexema vence sobre '<'. |
| `>` | `GT` | - | Simetrico de '<'. |
| `>=` | `GE` | - | Simetrico de '<='. |
| `!` | erro léxico na posição 0 | - | '!' esta no alfabeto mas nao casa com classe nenhuma: so existe em '!='. |
| `!=` | `NE` | - | Com o '=' ao lado, a palavra passa a pertencer a REL_OP. |

#### ARITH_OP x INT_LITERAL

| Entrada | Emitidos ao parser | Ignorados | Justificativa |
| --- | --- | --- | --- |
| `-10` | `MINUS`, `INT_LITERAL` | - | O sinal nao pertence ao literal (slide 73 - Aula 03). |
| `+7` | `PLUS`, `INT_LITERAL` | - | Mesma decisao para o '+'. |

#### Delimitadores adjacentes

| Entrada | Emitidos ao parser | Ignorados | Justificativa |
| --- | --- | --- | --- |
| `()` | `LPAREN`, `RPAREN` | - | '()' pertence a L_DelimiterCore², nao a L_DelimiterCore. |
| `{}` | `LBRACE`, `RBRACE` | - | Mesma regra para as chaves das extensoes. |
| `);` | `RPAREN`, `SEMICOLON` | - | Delimitadores de lexemas diferentes tambem nao se fundem. |

#### Classes ignoradas

| Entrada | Emitidos ao parser | Ignorados | Justificativa |
| --- | --- | --- | --- |
| `x = 1` | `IDENT`, `ASSIGN`, `INT_LITERAL` | `WHITESPACE`, `WHITESPACE` | Os espacos separam os lexemas e somem na saida. |
| `x=1 // fim` | `IDENT`, `ASSIGN`, `INT_LITERAL` | `WHITESPACE`, `LINE_COMMENT` | Comentario no fim da linha nao produz token. |
| `int\tx;` | `KW_INT`, `IDENT`, `SEMICOLON` | `WHITESPACE` | Tabulacao tambem é WHITESPACE e tambem é ignorada. |

### Gabaritos da aula

Os Exercícios 10 e 11 são a resposta do slide, e servem de prova de que o
catálogo concorda com a aula.

| Exercício | Entrada | Resultado | Slide |
| --- | --- | --- | --- |
| 10 | `print(total-2); // ok` | `KW_PRINT`, `LPAREN`, `IDENT`, `MINUS`, `INT_LITERAL`, `RPAREN`, `SEMICOLON` | 82 |
| 11 | `intx==10//fim` | `IDENT`, `EQ`, `INT_LITERAL` | 84 |

---

## 5. Teste cruzado e correções

| Divergência | Correção |
| --- | --- |
| `KEYWORD_CORE` não existia como classe própria | Virou classe própria, com definição, regex e testes |
| A tabela tinha 4 dos 9 itens do slide 90 | Os 4 itens faltantes viraram campos obrigatórios |
| `rNum = Dígito⁺` usava sobrescrito | Voltou para `Dígito+`, como no slide 73 |

---

## 6. Limitações e decisões assumidas

| Decisão assumida | Motivo |
| --- | --- |
| O corpo do comentário aceita caracteres fora de `ΣFonte`: `// olá @` passa | `//[^\r\n]*` é a tradução do próprio slide 76; a definição `C = ΣFonte − {CR, NL}` é mais estrita |
| `REL_OP` emite tipos específicos: `==` vira `EQ` | Slide 79, que gera `PLUS`, `MINUS`, `STAR` e `SLASH` a partir de `ARITH_OP`. O teste do Exercício 11 confere também pela classe |
| `RExt` e `DBloco` são nomes nossos | Os slides batizam `RCore` (72) e `DCore` (77), mas não os conjuntos das extensões |
| `!` sozinho é erro léxico, não token | Está no alfabeto-fonte, mas só forma lexema dentro de `!=` |
| O token guarda a posição absoluta, não linha e coluna | Slide 79: linha e coluna ficam para a Aula 5 |
| Acentos produzem erro léxico | Slide 67: acentos ficam fora da MiniLang-Core |
