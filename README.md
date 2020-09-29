# LogicaComp


## Diagrama sintático:

![Diagrama Sintatico](https://github.com/GiuPassarelli/LogicaComp/blob/master/diagrama-sintatico.png)

## EBNF:

BLOCK = { COMMAND };

COMMAND = ( sigma | ASSIGNMENT | PRINT ), "\n" ;

ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;

EXPRESSION = TERM, {("+" | "-"), TERM};

TERM = FACTOR, {("*" | "/"), FACTOR};

FACTOR = (("+" | "-") FACTOR) | "(", EXPRESSION, ")" | NUMBER | IDENTIFIER;

