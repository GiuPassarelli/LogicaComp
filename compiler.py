#!/usr/bin/python

import re
import sys

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

class PrePro:
    @staticmethod
    def filter(code):
        clean = re.sub(r'#=[\D\d]*?=#', '', code)
        clean = " ".join(clean.split())
        return clean

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):
        parser.blank = False
        pos = self.position
        if(len(self.origin)>pos):
            carac = self.origin[pos]
            if(carac.isdigit()):
                while(len(self.origin)>(pos+1) and (self.origin[pos+1]).isdigit()):
                    carac += self.origin[pos+1]
                    pos += 1
                self.actual = Token("INT", int(carac))

            elif(carac == "+"):
                self.actual = Token("PLUS", carac)
            elif(carac == "-"):
                self.actual = Token("MINUS", carac)
            elif(carac == "*"):
                self.actual = Token("MULTIPLY", carac)
            elif(carac == "/"):
                self.actual = Token("DIVIDE", carac)
            elif(carac == " "):
                parser.blank = True
            elif(carac != " "):
                raise Exception("Simbolo nao indentificado")

        else:
            self.actual = Token("EOF", "")

        pos += 1
        self.position = pos

class Parser:
    @staticmethod
    def parseExpression():
        tokens = parser.tokens
        result = parser.parseTerm()
        type_ = tokens.actual.type
        while(type_ == "PLUS" or type_ == "MINUS"):
            term_result = parser.parseTerm()
            if(type_ == "PLUS"):
                result += term_result
            if(type_ == "MINUS"):
                result -= term_result
            type_ = tokens.actual.type

        print(result)

    @staticmethod
    def parseTerm():
        tokens = parser.tokens
        tokens.selectNext()
        type1 = tokens.actual.type

        #Resolve entradas tipo "1+ 2"
        if((type1 == "PLUS" or type1 == "MINUS") and parser.blank):
            tokens.selectNext()
            type1 = tokens.actual.type
        
        if(type1 == "INT"):
            result = tokens.actual.value
            tokens.selectNext()
            type_ = tokens.actual.type

            #Resolve entradas tipo "1 +2"
            if(type_ == "INT"):
                tokens.selectNext()
                type_ = tokens.actual.type
                if(type_ == "INT"):
                    raise Exception("Números sem operação entre eles")

            while(type_ == "MULTIPLY" or type_ == "DIVIDE"):
                tokens.selectNext()
                type2 = tokens.actual.type
                if(type2 != "INT" and type2 != "EOF" and parser.blank):
                    tokens.selectNext()
                    type2 = tokens.actual.type
                if(type_ == "MULTIPLY"):
                    if(type2 == "INT"):
                        result *= tokens.actual.value
                    else:
                        raise Exception("Multiplicação não seguida por número")
                if(type_ == "DIVIDE"):
                    if(type2 == "INT"):
                        result /= tokens.actual.value
                    else:
                        raise Exception("Divisão não seguida por número")
                tokens.selectNext()
                type_ = tokens.actual.type
                
                #Resolve entradas tipo "1*2 *3"
                if(type_ == "INT"):
                    tokens.selectNext()
                    type_ = tokens.actual.type

            return(result)
        else:
            raise Exception("Não começa ou não termina com número ou possui simbolos repetidos")

    @staticmethod
    def run(code):
        clean = PrePro.filter(code)
        parser.tokens = Tokenizer(clean)
        parser.parseExpression()

parser = Parser()
parser.run(sys.argv[1])


#PROBLEMAS: 
# "2++3"
# Chamada de selectNext antes do term (no run)