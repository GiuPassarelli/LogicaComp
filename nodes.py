symbol_table = {}

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class BinOp(Node):
    def Evaluate(self):
        l_child = self.children[0].Evaluate()
        r_child = self.children[1].Evaluate()
        # if(l_child[1] == "bool" and r_child[1] == "int"):
        #     if(l_child[[0]]):
        #         l_child[0] = 1
        #     else:
        #         l_child[0] = 0
        #     if(r_child[0] != 0):
        #         r_child[0] = True
        #     else:
        #         r_child[0] = True
        # if(l_child[1] == "int" and r_child[1] == "bool"):
        #     if(r_child[[0]]):
        #         r_child[0] = 1
        #     else:
        #         r_child[0] = 0
        #     if(l_child[0] != 0):
        #         l_child[0] = True
        #     else:
        #         l_child[0] = True
        
        if(l_child[1] == "string"):
            if(self.value == "=="):
                result = l_child == r_child
            elif(self.value != "*"):
                raise Exception("Operação não permitida")
            else:
                result = l_child[0]
                if(r_child[1] == "bool"):
                    if(r_child[0]):
                        result += "true"
                    else:
                        result += "false"
                if(r_child[1] == "int"):
                    result += str(r_child[0])
                if(r_child[1] == "string"):
                    result += r_child[0]
                return (result, "string")
        elif(r_child[1] == "string"):
            if(self.value == "=="):
                result = l_child == r_child
            elif(self.value != "*"):
                raise Exception("Operação não permitida")
            else:
                if(l_child[1] == "bool"):
                    if(l_child[0]):
                        result = "true"
                    else:
                        result = "false"
                if(l_child[1] == "int"):
                    result = str(l_child[0])
                result += r_child[0]
                return (result, "string")
            

        else:       
            l_child = l_child[0]
            r_child = r_child[0]
            if(self.value == "+"):
                result = l_child + r_child
            elif(self.value == "-"):
                result = l_child - r_child
            elif(self.value == "*"):

                result = l_child * r_child
            elif(self.value == "/"):
                result = int(l_child / r_child)
            elif(self.value == "&&"):
                result = l_child and r_child
            elif(self.value == "||"):
                result = l_child or r_child
            elif(self.value == ">"):
                result = l_child > r_child
            elif(self.value == "<"):
                result = l_child < r_child
            elif(self.value == "=="):
                result = l_child == r_child

        if(type(result) == bool):
            return (result, "bool")
        return (result, "int")

class UnOp(Node):
    def Evaluate(self):
        child = self.children[0].Evaluate()[0]
        if(self.value == "+"):
            return(child, "int")
        elif(self.value == "-"):
            return(-child, "int")
        elif(self.value == "!"):
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
        return (self.value, "int")

class BoolVal(Node):
    def Evaluate(self):
        if(self.value == "true"):
            return (True, "bool")
        if(self.value == "false"):
            return (False, "bool")

class StringVal(Node):
    def Evaluate(self):
        return (self.value, "string")

class PrintNode(Node):
    def Evaluate(self):
        child = self.children[0].Evaluate()
        if(child[1] == "bool"):
            if(child[0]):
                print("true")
            else:
                print("false")
        else:
            print(child[0])

class IndentifierNode(Node):
    def Evaluate(self):
        symbtable = SymbolTable(self.value)
        return symbtable.getter()

class InputNode(Node):
    def Evaluate(self):
        value = int(input())
        return (value, "int")

class WhileNode(Node):
    def Evaluate(self):
        while(self.children[0].Evaluate()[0]):
            self.children[1].Evaluate()

class IfNode(Node):
    def Evaluate(self):
        if(self.children[0].Evaluate()[0]):
            self.children[1].Evaluate()
        elif(len(self.children) == 3):
            self.children[2].Evaluate()

class ElseNode(Node):
    def Evaluate(self):
        self.children[0].Evaluate()

#Funcao para declarar tipo
def Definition(symbol, tipo):
    symbol_table[symbol] = [None, tipo]


#Node para "="
class Assignment(Node):
    def Evaluate(self):
        set_value = self.children[1].Evaluate()[0]
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
        if(self.symbol not in symbol_table):
            raise Exception("Variável não definida")
        symbol_table[self.symbol][0] = value