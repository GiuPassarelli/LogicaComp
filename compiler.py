#!/usr/bin/python

import sys

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):
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
            #else:
            #    raise Exception("Simbolo nao indentificado")

        else:
            self.actual = Token("EOF", "")
        
        pos += 1
        self.position = pos

class Parser:
    @staticmethod
    def parseExpression():
        tokens = parser.tokens
        value = tokens.actual.value
        if(isinstance(value, int)):
            result = value
            tokens.selectNext()
            type_ = tokens.actual.type
            if((type_ != "PLUS" and type_ != "MINUS") and parser.isNumberRepeated == True):
                raise Exception("Números sem operação entre eles")
            while(type_ == "PLUS" or type_ == "MINUS"):
                tokens.selectNext()
                type2 = tokens.actual.type
                if(type_ == "PLUS"):
                    if(type2 != "INT" and type2 != "EOF"):
                        tokens.selectNext()
                        type2 = tokens.actual.type
                    if(type2 == "INT"):
                        result += tokens.actual.value
                    else:
                        raise Exception("Soma não seguida por número")
                if(type_ == "MINUS"):
                    if(type2 != "INT" and type2 != "EOF"):
                        tokens.selectNext()
                        type2 = tokens.actual.type
                    if(type2 == "INT"):
                        result -= tokens.actual.value
                    else:
                        raise Exception("Subtração não seguida por número")
                tokens.selectNext()
                type_ = tokens.actual.type
                tokens.actual.value = result
                parser.isNumberRepeated = False

            if(type_ != "EOF"):
                parser.isNumberRepeated = True
                parser.parseExpression()
            else:
                print(result)
        else:
            raise Exception("Não começa com número")

    @staticmethod
    def run(code):
        parser.tokens = Tokenizer(code)
        parser.tokens.selectNext()
        parser.isNumberRepeated = False
        parser.parseExpression()

#print ('Argument:', sys.argv[1])
arg = sys.argv[1]
arg = " ".join(arg.split())

#print("arg",arg)

parser = Parser()

parser.run(arg.strip())

#print(parser.tokens)