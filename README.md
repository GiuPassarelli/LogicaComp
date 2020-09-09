# LogicaComp


## Diagrama sintático:

![Diagrama Sintatico](https://github.com/GiuPassarelli/LogicaComp/blob/master/diagrama-sintatico.png)

## EBNF:

EXPRESSION = TERM, {("+" | "-"), TERM};

TERM = FACTOR, {("*" | "/"), FACTOR};

FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number;
