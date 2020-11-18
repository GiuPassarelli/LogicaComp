import itertools
symbol_table = {}

class Node:
    id_generator = itertools.count(0)
    def __init__(self, value):
        self.value = value
        self.children = []
        self.id = next(self.id_generator)

class BinOp(Node):
    def Evaluate(self):
        ass = Assembler()
        l_child = self.children[0].Evaluate()
        ass.receiveString("PUSH EBX")
        r_child = self.children[1].Evaluate()
        ass.receiveString("POP EAX")

        l_child = l_child[0]
        r_child = r_child[0]
        if(self.value == "+"):
            ass.receiveString("ADD EAX, EBX")
            ass.receiveString("MOV EBX, EAX")
            result = l_child + r_child
        elif(self.value == "-"):
            ass.receiveString("SUB EAX, EBX")
            ass.receiveString("MOV EBX, EAX")
            result = l_child - r_child
        elif(self.value == "*"):
            ass.receiveString("IMUL EBX")
            ass.receiveString("MOV EBX, EAX")
            result = l_child * r_child
        elif(self.value == "/"):
            ass.receiveString("DIV EBX")
            ass.receiveString("MOV EBX, EAX")
            result = int(l_child / r_child)
        elif(self.value == "&&"):
            ass.receiveString("AND EAX, EBX")
            ass.receiveString("MOV EBX, EAX")
            result = l_child and r_child
        elif(self.value == "||"):
            ass.receiveString("OR EAX, EBX")
            ass.receiveString("MOV EBX, EAX")
            result = l_child or r_child
        elif(self.value == ">"):
            ass.receiveString("CMP EAX, EBX")
            ass.receiveString("CALL binop_jg")
            result = l_child > r_child
        elif(self.value == "<"):
            ass.receiveString("CMP EAX, EBX")
            ass.receiveString("CALL binop_jl")
            result = l_child < r_child
        elif(self.value == "=="):
            ass.receiveString("CMP EAX, EBX")
            ass.receiveString("CALL binop_je")
            result = l_child == r_child

        if(type(result) == bool):
            return (result, "bool")
        return (result, "int")

class UnOp(Node):
    def Evaluate(self):
        child = self.children[0].Evaluate()[0]
        if(self.value == "+"):
            Assembler().receiveString("MOV EBX, " + str(child))
            return(child, "int")
        elif(self.value == "-"):
            Assembler().receiveString("MOV EBX, -" + str(child))
            return(-child, "int")
        elif(self.value == "!"):
            Assembler().receiveString("MOV EBX, !" + str(child))
            return(not child, "bool")

class NoOp(Node):
    def Evaluate(self):
        pass

class Statements(Node):
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class IntVal(Node):
    def Evaluate(self):
        comando = "MOV EBX, " + str(self.value)
        Assembler().receiveString(comando)
        return (self.value, "int")

class BoolVal(Node):
    def Evaluate(self):
        if(self.value == "true"):
            Assembler().receiveString("MOV EBX, True")
            return (True, "bool")
        if(self.value == "false"):
            Assembler().receiveString("MOV EBX, False")
            return (False, "bool")

class StringVal(Node):
    def Evaluate(self):
        return (self.value, "string")

class PrintNode(Node):
    def Evaluate(self):
        ass = Assembler()
        self.children[0].Evaluate()
        ass.receiveString("PUSH EBX")
        ass.receiveString("CALL print")
        ass.receiveString("POP EBX")

class IndentifierNode(Node):
    def Evaluate(self):
        symbtable = SymbolTable(self.value)
        Assembler().receiveString("MOV EBX, [EBP" + str(symbtable.getter()[2]) + "]")
        return (symbtable.getter()[0], symbtable.getter()[1])

class InputNode(Node):
    def Evaluate(self):
        value = int(input())
        return (value, "int")

class WhileNode(Node):
    def Evaluate(self):
        ass = Assembler()
        ass.receiveString("LOOP_" + str(self.id) + ": ")
        self.children[0].Evaluate()
        ass.receiveString("CMP EXB, False")
        ass.receiveString("JE EXIT_" + str(self.id))
        self.children[1].Evaluate()
        ass.receiveString("JMP LOOP_" + str(self.id))
        ass.receiveString("EXIT_" + str(self.id))


class IfNode(Node):
    def Evaluate(self):
        ass = Assembler()
        ass.receiveString("LOOP_" + str(self.id) + ": ")
        self.children[0].Evaluate()
        ass.receiveString("CMP EXB, False")
        if(len(self.children) == 3):
            ass.receiveString("JMP LOOP_" + str(self.children[2].id))
        else:
            ass.receiveString("JE EXIT_" + str(self.id))
        self.children[1].Evaluate()
        ass.receiveString("JE EXIT_" + str(self.id))
        if(len(self.children) == 3):
            self.children[2].Evaluate()
        ass.receiveString("EXIT_" + str(self.id))

class ElseNode(Node):
    def Evaluate(self):
        self.children[0].Evaluate()

shift = 0

#Funcao para declarar tipo
def Definition(symbol, tipo):
    global shift
    shift -= 4
    symbol_table[symbol] = [None, tipo, shift]

    Assembler().receiveString("PUSH DWORD 0")

#Node para "="
class Assignment(Node):
    def Evaluate(self):
        set_value = self.children[1].Evaluate()[0]
        symbtable = SymbolTable(self.children[0].value)
        symbtable.setter(set_value)

        Assembler().receiveString("MOV [EBP" + str(symbtable.getter()[2]) + "], EBX")

class SymbolTable:
    def __init__(self, symbol):
        self.symbol = symbol

    def getter(self):
        if(self.symbol in symbol_table):
            return symbol_table[self.symbol]
        else:
            raise Exception("Variável não achada")

    def setter(self, value):
        if(self.symbol not in symbol_table):
            raise Exception("Variável não definida")
        symbol_table[self.symbol][0] = value

class Assembler:
    @staticmethod
    def initText():
        with open('program.asm', 'w') as f1:
            for line in open('startText.txt'):
                f1.write(line)


    @staticmethod
    def receiveString(comando):
        with open("program.asm", "a") as f1:
            f1.write("\n" + comando)
    
    @staticmethod
    def endText():
        with open("program.asm", "a") as f1:
            f1.write("\n" + "POP EBP")
            f1.write("\n" + "MOV EAX, 1")
            f1.write("\n" + "INT 0x80")