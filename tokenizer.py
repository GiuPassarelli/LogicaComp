class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.value_dict = {"+": "PLUS", "-": "MINUS", "*": "MULTIPLY", "/": "DIVIDE", "(": "OPEN_PAR", 
                            ")": "CLOSE_PAR", "=": "IGUAL", "\n": "ENTER", "!": "NOT", ">": "MAIOR",
                            "<": "MENOR"}
        self.reserved_dict = {"println": "PRINT", "if": "IF", "elseif": "ELSEIF", "else": "ELSE", 
                            "while": "WHILE", "end": "END", "readline": "INPUT"}

    def selectNext(self):
        pos = self.position
        if(len(self.origin)>pos):
            carac = self.origin[pos]
            if(carac.isdigit()):
                while(len(self.origin)>(pos+1) and (self.origin[pos+1]).isdigit()):
                    pos += 1
                    carac += self.origin[pos]
                self.actual = Token("INT", int(carac))
            
            elif(carac.isalpha()):
                while(len(self.origin)>(pos+1) and ((self.origin[pos+1]).isalpha() or (self.origin[pos+1]).isdigit() or (self.origin[pos+1]) == "_")):
                    carac += self.origin[pos+1]
                    pos += 1
                if(carac in self.reserved_dict):
                    self.actual = Token(self.reserved_dict[carac], carac)
                else:
                    self.actual = Token("IDENTIFIER", carac)
    
            elif(carac == "&" and self.origin[pos+1] == "&"):
                pos+=1
                self.actual = Token("AND", "&&")
            elif(carac == "|" and self.origin[pos+1] == "|"):
                pos+=1
                self.actual = Token("OR", "||")
            elif(carac == "=" and self.origin[pos+1] == "="):
                pos+=1
                self.actual = Token("COMPARACAO", "==")
            
            elif(carac in self.value_dict):
                self.actual = Token(self.value_dict[carac], carac)

            elif(carac == " "):
                if(self.actual is not None):
                    type1 = self.actual.type
                else:
                    type1 = "None"

                while(carac == " "):
                    self.position += 1
                    pos = self.selectNext() - 1
                    carac = self.origin[pos]
                type2 = self.actual.type
                if((type2 == "INT" or type2 == "IDENTIFIER") and (type1 == "INT" or type1 == "IDENTIFIER")):
                    raise Exception("Números sem operação entre eles")
            
            else:
                raise Exception("Caractér não reconhecido")

        else:
            self.actual = Token("EOF", "")

        pos += 1
        self.position = pos
        return self.position