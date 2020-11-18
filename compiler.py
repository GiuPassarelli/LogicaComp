#!/usr/bin/python
 # pylint: disable=unused-wildcard-import, method-hidden

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
        bockTypes = ["EOF", "END", "ELSEIF", "ELSE"]
        tokens = parser.tokens
        StatNode = Statements(None)
        while(tokens.actual.type not in bockTypes):
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

            tokens.selectNext()
            type_ = tokens.actual.type

            EqNode = Assignment(None)
            EqNode.children.append(VarNode)

            if(type_ == "INPUT"):
                readNode = InputNode(None)
                tokens.selectNext()
                type1 = tokens.actual.type
                tokens.selectNext()
                type2 = tokens.actual.type
                tokens.selectNext()
                if(type1 != "OPEN_PAR" or type2 != "CLOSE_PAR"):
                    raise Exception("readline nao seguido de ()")
                EqNode.children.append(readNode)
            else:
                EqNode.children.append(parser.parseRelExpression())
            
            result = EqNode
                
        elif(type_ == "PRINT"):
            PNode = PrintNode(None)

            tokens.selectNext()
            type_ = tokens.actual.type

            if(type_ != "OPEN_PAR"):
                raise Exception("Print deve ser seguido de parêntesis")

            tokens.selectNext()
            PNode.children.append(parser.parseRelExpression())
            result = PNode

            type_ = tokens.actual.type
            tokens.selectNext()

            if(type_ != "CLOSE_PAR"):
                raise Exception("Parêntesis do print não fechado")
        
        elif(type_ == "WHILE"):
            whileNode = WhileNode(None)
            
            tokens.selectNext()
            whileNode.children.append(parser.parseRelExpression())

            type_ = tokens.actual.type
            if(type_ != "ENTER"):
                raise Exception("Pule linha depois do while")

            tokens.selectNext()
            whileNode.children.append(parser.parseBlock())

            result = whileNode

            type_ = tokens.actual.type
            if(type_ != "END"):
                raise Exception("Coloque END depois de um while")
            
            tokens.selectNext()

        elif(type_ == "IF"):
            originalNode = IfNode(None)
            ifNode = originalNode
            while(type_ == "IF" or type_ == "ELSEIF"):
                
                tokens.selectNext()
                ifNode.children.append(parser.parseRelExpression())

                type1 = tokens.actual.type
                if(type1 != "ENTER"):
                    raise Exception("Pule linha depois do if")

                tokens.selectNext()
                ifNode.children.append(parser.parseBlock())

                type_ = tokens.actual.type
                if(type_ == "ELSEIF"):
                    elseifNode = IfNode(None)
                    ifNode.children.append(elseifNode)
                    ifNode = elseifNode
                
                elif(type_ == "ELSE"):
                    elseNode = ElseNode(None)
                    ifNode.children.append(elseNode)

                    tokens.selectNext()
                    type1 = tokens.actual.type
                    if(type1 != "ENTER"):
                        raise Exception("Pule linha depois do if")

                    tokens.selectNext()
                    elseNode.children.append(parser.parseBlock())

            type_ = tokens.actual.type
            if(type_ != "END"):
                raise Exception("Coloque END depois de um if")
            
            result = originalNode
            tokens.selectNext()

        elif(type_ == "LOCAL"):
            tokens.selectNext()
            type_ = tokens.actual.type
            symb = tokens.actual.value
            if(type_ != "IDENTIFIER"):
                raise Exception("Local definido errado")
            tokens.selectNext()
            type_ = tokens.actual.type
            if(type_ != "DEFINICAO"):
                raise Exception("Local definido errado")
            tokens.selectNext()
            type_ = tokens.actual.value
            if(type_ != "Int" and type_ != "Bool" and type_ != "String"):
                raise Exception("Local definido errado")
            
            Definition(symb, type_)
            tokens.selectNext()
        
        type_ = tokens.actual.type
        if(type_ == "ENTER"):
            tokens.selectNext()
            return (result)

        raise Exception("Dê enter após operações")

    @staticmethod
    def parseRelExpression():
        relExpTypes = ["MAIOR", "MENOR", "COMPARACAO"]
        tokens = parser.tokens
        result = parser.parseExpression()
        type_ = tokens.actual.type
        while(type_ in relExpTypes):
            BinNode = BinOp(tokens.actual.value)
            BinNode.children.append(result)
            tokens.selectNext()

            BinNode.children.append(parser.parseExpression())
            result = BinNode
            type_ = tokens.actual.type
        return(result)

    @staticmethod
    def parseExpression():
        expressionTypes = ["PLUS", "MINUS", "OR"]
        tokens = parser.tokens
        result = parser.parseTerm()
        type_ = tokens.actual.type
        while(type_ in expressionTypes):
            BinNode = BinOp(tokens.actual.value)
            BinNode.children.append(result)
            tokens.selectNext()

            BinNode.children.append(parser.parseTerm())
            result = BinNode
            type_ = tokens.actual.type
        return(result)

    @staticmethod
    def parseTerm():
        termTypes = ["MULTIPLY", "DIVIDE", "AND"]
        tokens = parser.tokens
        result = parser.parseFactor()
        type_ = tokens.actual.type
        while(type_ in termTypes):
            BinNode = BinOp(tokens.actual.value)
            BinNode.children.append(result)
            tokens.selectNext()

            BinNode.children.append(parser.parseFactor())
            result = BinNode
            type_ = tokens.actual.type
        return(result)

    @staticmethod
    def parseFactor():
        factorTypes = ["PLUS", "MINUS", "NOT"]
        tokens = parser.tokens
        type_ = tokens.actual.type
        if(type_ == "INT"):
            result = IntVal(tokens.actual.value)
            tokens.selectNext()
        elif(type_ in factorTypes):
            result = UnOp(tokens.actual.value)
            tokens.selectNext()
            result_factor = parser.parseFactor()
            result.children.append(result_factor)
        elif(type_ == "OPEN_PAR"):
            tokens.selectNext()
            result = parser.parseRelExpression()
            if(tokens.actual.type != "CLOSE_PAR"):
                raise Exception("Parentesis não fechado")
            tokens.selectNext()
        elif(type_ == "IDENTIFIER"):
            INode = IndentifierNode(tokens.actual.value)
            result = INode
            tokens.selectNext()
        elif(type_ == "TRUE" or type_ == "FALSE"):
            result = BoolVal(tokens.actual.value)
            tokens.selectNext()
        elif(type_ == "STRING"):
            result = StringVal(tokens.actual.value)
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

Assembler().initText()

parser = Parser()
result = parser.run(entrada[0])
result.Evaluate()

Assembler().endText()

#SO PULA 1 QUANDO EH BOLINHA!!