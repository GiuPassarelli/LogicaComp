#!/usr/bin/python

import sys

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

class Tokenizer:
    def __init__(self, origin, position, actual):
        self.origin = origin
        self.position = position
        self.actual = actual

    def selectNext(self):
        pos = self.position
        carac = self.origin[pos]
        if(carac.isdigit()):
            pos += 1
            while((self.origin[pos]).isdigit()):
                carac += self.origin[pos]
                print(carac)
                pos += 1
        
        else:
            if(carac == "+"):
                actual = Token("PLUS", carac)
            elif(carac == "-"):
                actual = Token("MINUS", carac)
            elif(carac == "'"):
                actual = Token("EOF", carac)
            pos += 1
        
        print(pos)
        self.position = pos
        


class Parser:
    #tokens = 1

    @staticmethod
    def parseExpression():
        pass

    @staticmethod
    def run(code):
        pass

print ('Argument:', sys.argv[1])

parser = Parser()
parser.tokens = Tokenizer(sys.argv[1], 1, None)
parser.tokens.selectNext()

#print(parser.tokens)

