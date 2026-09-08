# Alfabeto-fonte da MiniLang e os conjuntos derivados dele (slides 70, 76 e 77)

import string

LETRAS = frozenset(string.ascii_letters)
DIGITOS = frozenset(string.digits)
ESPACOS_EM_BRANCO = frozenset(" \t\r\n")
SIMBOLOS_NUCLEO = frozenset("+-*/=();")
SIMBOLOS_EXTENSAO = frozenset("<>!{}")
SIMBOLOS = SIMBOLOS_NUCLEO | SIMBOLOS_EXTENSAO

INICIAL = LETRAS | {"_"}
CONTINUACAO = LETRAS | DIGITOS | {"_"}

ALFABETO_FONTE = LETRAS | DIGITOS | ESPACOS_EM_BRANCO | SIMBOLOS | {"_"}

CORPO_COMENTARIO = ALFABETO_FONTE - frozenset("\r\n")
