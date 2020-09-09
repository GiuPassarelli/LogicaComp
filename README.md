# LogicaComp


## Diagrama sintático:

![Diagrama Sintatico](https://github.com/GiuPassarelli/LogicaComp/blob/master/diagrama-sintatico.png)

## EBNF:

DIGIT = 0 | 1 | ... | 9;

NUMBER = DIGIT, {DIGIT};

TERM = NUMBER, {("*" | "/"), NUMBER};

EXPRESSION = TERM, {("+" | "-"), TERM}
