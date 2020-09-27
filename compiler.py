#!/usr/bin/python

import re
import sys
from tokenizer import Tokenizer
from nodes import *

class PrePro:
    @staticmethod
    def filter(code):
        clean = re.sub(r'#=[\D\d]*?=#', '', code)
        return clean

class Parser:
    @staticmethod
    def parseBlock():
        tokens = parser.tokens
        StatNode = Statements(None)
        while(tokens.actual.type != "EOF"):
            result = parser.parseCommand()
            StatNode.children.append(result)
        return StatNode

    @staticmethod
    def parseCommand():
        tokens = parser.tokens
        type_ = tokens.actual.type
        result = NoOp(None)
        if(type_ == "IDENTIFIER"):
            VarNode = IndentifierNode(tokens.actual.value)
            tokens.selectNext()
            type_ = tokens.actual.type

            if(type_ != "IGUAL"):
                raise Exception("Variável solta no código")

            EqNode = Assignment(None)
            EqNode.children.append(VarNode)

            tokens.selectNext()
            EqNode.children.append(parser.parseExpression())
            result = EqNode
                
        if(type_ == "PRINT"):
            PNode = PrintNode(None)

            tokens.selectNext()
            type_ = tokens.actual.type

            if(type_ != "OPEN_PAR"):
                raise Exception("Print deve ser seguido de parêntesis")

            tokens.selectNext()
            PNode.children.append(parser.parseExpression())
            result = PNode

            type_ = tokens.actual.type
            tokens.selectNext()

            if(type_ != "CLOSE_PAR"):
                raise Exception("Parêntesis do print não fechado")
                
        type_ = tokens.actual.type
        if(type_ == "ENTER"):
            tokens.selectNext()
            return (result)

        raise Exception("Dê enter após operações")


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
        elif(type_ == "IDENTIFIER"):
            INode = IndentifierNode(tokens.actual.value)
            result = INode
            tokens.selectNext()
        else:
            raise Exception("Deu errado")
        return result

    @staticmethod
    def run(code):
        clean = PrePro.filter(code)
        parser.tokens = Tokenizer(clean)
        parser.tokens.selectNext()
        result = parser.parseBlock()
        if(parser.tokens.actual.type != "EOF"):
            raise Exception("Não terminou direito")
        return(result)

f = open(sys.argv[1], "r")
entrada = []
entrada.append(str(f.read()))

parser = Parser()
result = parser.run(entrada[0])
result.Evaluate()

#SO PULA 1 QUANDO EH BOLINHA!!