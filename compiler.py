#!/usr/bin/python

import sys

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 1
        self.actual = None

    def selectNext(self):
        pos = self.position
        carac = self.origin[pos]
        #print(self.origin[self.position])
        if(carac.isdigit()):
            pos += 1
            while((self.origin[pos]).isdigit()):
                carac += self.origin[pos]
                #print(carac)
                pos += 1
            self.actual = Token("INT", int(carac))
        
        else:
            if(carac == "+"):
                self.actual = Token("PLUS", carac)
            elif(carac == "-"):
                self.actual = Token("MINUS", carac)
            elif(carac == "'"):
                self.actual = Token("EOF", carac)
            # else:
            #     raise Exception("Simbolo nao indentificado")
            pos += 1
        
        #print(pos)
        self.position = pos

class Parser:
    #tokens = 1

    @staticmethod
    def parseExpression():
        tokens = parser.tokens
        tokens.selectNext()
        value = tokens.actual.value
        if(isinstance(value, int)):
            result = value
            tokens.selectNext()
            type_ = tokens.actual.type
            while(type_ == "PLUS" or type_ == "MINUS"):
                tokens.selectNext()
                type2 = tokens.actual.type
                if(type_ == "PLUS"):
                    if(type2 == "INT"):
                        result += tokens.actual.value
                    else:
                        raise Exception("Soma não seguida por número")
                if(type_ == "MINUS"):
                    if(type2 == "INT"):
                        result -= tokens.actual.value
                    else:
                        raise Exception("Subtração não seguida por número")
                tokens.selectNext()
                type_ = tokens.actual.type
            print(result)
        else:
            raise Exception("Não começa com número")

    @staticmethod
    def run(code):
        parser.tokens = Tokenizer(code)
        parser.parseExpression()

#print ('Argument:', sys.argv[1:])

parser = Parser()

arg = ""
for i in sys.argv[1:]:
    arg += i

#print("ARG", arg)

parser.run(arg)


#print(parser.tokens)