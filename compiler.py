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

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class BinOp(Node):
    def __init__(self, value):
        super().__init__(value)
    def Evaluate(self):
        l_child = self.children[0].Evaluate()
        r_child = self.children[1].Evaluate()
        if(self.value == "+"):
            return(l_child + r_child)
        elif(self.value == "-"):
            return(l_child - r_child)
        elif(self.value == "*"):
            return(l_child * r_child)
        elif(self.value == "/"):
            return(int(l_child / r_child))

class UnOp(Node):
    def __init__(self, value):
        super().__init__(value)
    def Evaluate(self):
        child = self.children[0].Evaluate()
        if(self.value == "+"):
            return(child)
        elif(self.value == "-"):
            return(-child)

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    def Evaluate(self):
        pass

class Parser:
    @staticmethod
    def parseExpression():
        tokens = parser.tokens
        result = parser.parseTerm()
        type_ = tokens.actual.type
        while(type_ == "PLUS" or type_ == "MINUS"):
            BinNode = BinOp(tokens.actual.value)
            BinNode.children.append(result)
            tokens.selectNext()

            BinNode.children.append(parser.parseTerm())
            result = BinNode
            type_ = tokens.actual.type
        return(result)

    @staticmethod
    def parseTerm():
        tokens = parser.tokens
        result = parser.parseFactor()
        type_ = tokens.actual.type
        while(type_ == "MULTIPLY" or type_ == "DIVIDE"):
            BinNode = BinOp(tokens.actual.value)
            BinNode.children.append(result)
            tokens.selectNext()

            BinNode.children.append(parser.parseFactor())
            result = BinNode
            type_ = tokens.actual.type
        return(result)

    @staticmethod
    def parseFactor():
        tokens = parser.tokens
        type_ = tokens.actual.type
        if(type_ == "INT"):
            result = IntVal(tokens.actual.value)
            tokens.selectNext()
        elif(type_ == "PLUS" or type_ == "MINUS"):
            result = UnOp(tokens.actual.value)
            tokens.selectNext()
            result_factor = parser.parseFactor()
            result.children.append(result_factor)
        elif(type_ == "OPEN_PAR"):
            tokens.selectNext()
            result = parser.parseExpression()
            if(tokens.actual.type != "CLOSE_PAR"):
                raise Exception("Parentesis não fechado")
            tokens.selectNext()
        else:
            raise Exception("Deu errado")
        return result

    @staticmethod
    def run(code):
        clean = PrePro.filter(code)
        parser.tokens = Tokenizer(clean)
        parser.tokens.selectNext()
        result = parser.parseExpression()
        if(parser.tokens.actual.type != "EOF"):
            raise Exception("Não terminou direito")
        else:
            return(result)

f = open(sys.argv[1], "r")
entrada = []
entrada.append(str(f.read()))

parser = Parser()
result = parser.run(entrada[0])
print(result.Evaluate())


#SO PULA 1 QUANDO EH BOLINHA!!