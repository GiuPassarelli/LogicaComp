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
        self.value_dict = {"+": "PLUS", "-": "MINUS", "*": "MULTIPLY", "/": "DIVIDE", "(": "OPEN_PAR", ")": "CLOSE_PAR"}

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

            elif(carac in self.value_dict):
                self.actual = Token(self.value_dict[carac], carac)

            elif(carac == " "):
                parser.blank = True
                type_ = self.actual.type
                self.position += 1
                pos = self.selectNext() - 1
                if(self.actual.type == "INT" and type_ == "INT"):
                    raise Exception("Números sem operação entre eles")
            else:
                raise Exception("Simbolo nao indentificado")

        else:
            self.actual = Token("EOF", "")

        pos += 1
        self.position = pos
        return self.position

class Parser:
    @staticmethod
    def parseExpression():
        tokens = parser.tokens
        result = parser.parseTerm()
        type_ = tokens.actual.type
        while(type_ == "PLUS" or type_ == "MINUS"):
            tokens.selectNext()
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
        type1 = tokens.actual.type
        
        if(type1 == "INT"):
            result = tokens.actual.value
            tokens.selectNext()
            type_ = tokens.actual.type

            while(type_ == "MULTIPLY" or type_ == "DIVIDE"):
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
                        result = int(result)
                    else:
                        raise Exception("Divisão não seguida por número")
                tokens.selectNext()
                type_ = tokens.actual.type

            return(result)
        else:
            raise Exception("Deu errado")

    @staticmethod
    def run(code):
        clean = PrePro.filter(code)
        parser.tokens = Tokenizer(clean)
        parser.tokens.selectNext()
        parser.parseExpression()
        if(parser.tokens.actual.type != "EOF"):
            raise Exception("Não terminou direito")

parser = Parser()
parser.run(sys.argv[1])


#SO PULA 1 QUANDO EH BOLINHA!!