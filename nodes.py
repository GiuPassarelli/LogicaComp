symbol_table = {}
func_table = {}

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class BinOp(Node):
    def Evaluate(self, table):
        l_child = self.children[0].Evaluate(table)
        r_child = self.children[1].Evaluate(table)
        
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
    def Evaluate(self, table):
        child = self.children[0].Evaluate(table)[0]
        if(self.value == "+"):
            return(child, "int")
        elif(self.value == "-"):
            return(-child, "int")
        elif(self.value == "!"):
            return(not child, "bool")

class NoOp(Node):
    def Evaluate(self, table):
        pass

class Statements(Node):
    def Evaluate(self, table):
        if(table == 0):
            table = symbol_table
        for child in self.children:
            child.Evaluate(table)

class IntVal(Node):
    def Evaluate(self, table):
        return (self.value, "int")

class BoolVal(Node):
    def Evaluate(self, table):
        if(self.value == "true"):
            return (True, "bool")
        if(self.value == "false"):
            return (False, "bool")

class StringVal(Node):
    def Evaluate(self, table):
        return (self.value, "string")

class PrintNode(Node):
    def Evaluate(self, table):
        child = self.children[0].Evaluate(table)
        if(child[1] == "bool"):
            if(child[0]):
                print("true")
            else:
                print("false")
        else:
            print(child[0])

class IndentifierNode(Node):
    def Evaluate(self, table):
        symbtable = SymbolTable(self.value)
        return symbtable.getter(table)

class InputNode(Node):
    def Evaluate(self, table):
        value = int(input())
        return (value, "int")

class WhileNode(Node):
    def Evaluate(self, table):
        value, tipo = self.children[0].Evaluate(table)
        if(tipo == "string"):
            raise Exception("Notação inválida")
        while(value):
            self.children[1].Evaluate(table)
            value = self.children[0].Evaluate(table)[0]

class IfNode(Node):
    def Evaluate(self, table):
        value, tipo = self.children[0].Evaluate(table)
        if(tipo == "string"):
            raise Exception("Notação inválida")
        if(value):
            self.children[1].Evaluate(table)
        elif(len(self.children) == 3):
            self.children[2].Evaluate(table)

class ElseNode(Node):
    def Evaluate(self, table):
        self.children[0].Evaluate(table)

class FuncDec(Node):
    def Evaluate(self, table):
        if(self.value in symbol_table or self.value in func_table):
            raise Exception("Nome ja esta em uso")
        func_table[self.value] = FuncDec(self.value)
        func_table[self.value].children = self.children

class FuncCall(Node):
    def Evaluate(self, table):
        new_table = {}
        if(self.value not in func_table):
            raise Exception("Funcao nao declarada")
        funcao = func_table[self.value]
        if (len(funcao.children) - 1) != len(self.children):
            raise Exception("Numero diferente de argumentos")

        for i in range(len(self.children)):
            #0 é valor, 1 é tipo
            retorno_lista = self.children[i].Evaluate(table)
            funcao.children[i].Evaluate(new_table)
            if(new_table[funcao.children[i].value[0]][1] != retorno_lista[1]):
                raise Exception("Tipos sao diferentes")

            new_table[funcao.children[i].value[0]][0] = retorno_lista[0]
        funcao.children[len(self.children)].Evaluate(new_table)
        if("return" in new_table):
            return new_table["return"]


class Definition(Node):
    def Evaluate(self, table):
        symbol = self.value[0]
        tipo = self.value[1]

        if(tipo == 'String'):
            table[symbol] = [None, 'string']
        elif(tipo == 'Bool'):
            table[symbol] = [None, 'bool']
        elif(tipo == 'Int'):
            table[symbol] = [None, 'int']

class ReturnNode(Node):
    def Evaluate(self, table):
        table["return"] = self.children[0].Evaluate(table)

#Funcao para declarar tipo
# def Definition(symbol, tipo):
#     if(tipo == 'String'):
#         symbol_table[symbol] = [None, 'string']
#     elif(tipo == 'Bool'):
#         symbol_table[symbol] = [None, 'bool']
#     elif(tipo == 'Int'):
#         symbol_table[symbol] = [None, 'int']


#Node para "="
class Assignment(Node):
    def Evaluate(self, table):
        set_value = self.children[1].Evaluate(table)[0]
        symbtable = SymbolTable(self.children[0].value)
        symbtable.setter(set_value, table)

class SymbolTable:
    def __init__(self, symbol):
        self.symbol = symbol

    def getter(self, table):
        if(self.symbol in table):
            return table[self.symbol]
        else:
            raise Exception("Variável não achada")

    def setter(self, value, table):
        if(self.symbol not in table):
            raise Exception("Variável não definida")
        if(self.symbol in func_table):
            raise Exception("Nome já existe")
            
        table[self.symbol][0] = value