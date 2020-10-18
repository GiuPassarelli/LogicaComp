symbol_table = {}

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class BinOp(Node):
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
        elif(self.value == "&&"):
            return(l_child and r_child)
        elif(self.value == "||"):
            return(l_child or r_child)
        elif(self.value == ">"):
            return(l_child > r_child)
        elif(self.value == "<"):
            return(l_child < r_child)
        elif(self.value == "=="):
            return(l_child == r_child)

class UnOp(Node):
    def Evaluate(self):
        child = self.children[0].Evaluate()
        if(self.value == "+"):
            return(child)
        elif(self.value == "-"):
            return(-child)
        elif(self.value == "!"):
            return(not child)

class NoOp(Node):
    def Evaluate(self):
        pass

class Statements(Node):
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class IntVal(Node):
    def Evaluate(self):
        return self.value

class PrintNode(Node):
    def Evaluate(self):
        print(self.children[0].Evaluate())

class IndentifierNode(Node):
    def Evaluate(self):
        symbtable = SymbolTable(self.value)
        return symbtable.getter()

class InputNode(Node):
    def Evaluate(self):
        value = int(input())
        return value

class WhileNode(Node):
    def Evaluate(self):
        while(self.children[0].Evaluate()):
            self.children[1].Evaluate()

class IfNode(Node):
    def Evaluate(self):
        if(self.children[0].Evaluate()):
            self.children[1].Evaluate()
        elif(len(self.children) == 3):
            self.children[2].Evaluate()

class ElseNode(Node):
    def Evaluate(self):
        self.children[0].Evaluate()

#Node para "="
class Assignment(Node):
    def Evaluate(self):
        set_value = self.children[1].Evaluate()
        symbtable = SymbolTable(self.children[0].value)
        symbtable.setter(set_value)

class SymbolTable:
    def __init__(self, symbol):
        self.symbol = symbol

    def getter(self):
        if(self.symbol in symbol_table):
            return symbol_table[self.symbol]
        else:
            raise Exception("Variável não achada")

    def setter(self, value):
        symbol_table[self.symbol] = value