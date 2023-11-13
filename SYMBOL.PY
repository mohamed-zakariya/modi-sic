import dic as d

class File :
    def  __init__(self):
        
        self.hte_path = 'HTE.txt'
        self.conten=0
        self.lines=0
        self.hRecord=0
        
         
    def open_file(self):
        with open(self.hte_path, 'r') as file:
            self.content = file.read()
            # print(content[0])
            file.seek(0)
            self.lines = file.readlines()      

            
class Symbol:
    def __init__(self):
        self.symbolTable_path = "symbolTable.txt"
        self.programName=""
        self.start=0
        self.end=0
        self.length=""
        self.objectCodes = []
        self.objcode_1 = []
        self.objcode_3 = []
        self.objcode_3_imm = []
        self.symbolTable = {}
        self.symbolTable2 = []
        self.inst_ref = {}
        self.opCode=[]
        self.ref_num=0 


    def get_H_record(self,f):
        title = f.lines[0][1:7]
        
        flag = 1
        first = 1
        for letter in reversed(title):
           
            if letter != 'X' and first == 1:
                first = 0
                flag = 0
                self.programName += letter

            elif letter == 'X' and flag == 1:
                continue

            elif letter != 'X' or (letter == 'X' and first == 0): 
                flag = 0
                self.programName += letter               
        self.programName = self.programName[::-1]
        
        self.start = f.lines[0][7:13]
        self.length = f.lines[0][13:19]
        self.end = int(self.start, 16) + int(self.length, 16)
        self.end = hex(self.end).upper()
        self.end = self.end[2:]
        self.start = int(self.start, 16)
        self.start = hex(self.start).upper()
        self.start = self.start[2:]
       


    def check_Format1(self):

        return self.opCode in d.opcode_1

    def check_dic(self):
        return self.opCode in d.opcode_3

    def check_imd(self,):
        bit8 = bin(int(self.opCode, 16)).upper()
        bit8 = bit8[-1]
        return bit8 == '1'
    
    def get_trecord_objectCode(self,f, j):
        objcodes = f.lines[j][9:-1]
        
        i = 0
        while i < len(objcodes):
            self.opCode = objcodes[i:i+2]
            # print(opCode, ' ->', i, '->', )

            if self.check_Format1():
                self.objcode_1.append(self.opCode)
                i = i+2
            elif self.check_dic() and self.check_imd():
                self.objcode_3_imm.append(objcodes[i:i+6])
                i = i+6
            elif self.check_dic():
                self.objcode_3.append(objcodes[i:i+6])
                i = i+6
            else:
                i = i+6
               
            
      

    def get_trecord_symbolTable(self):
        
        for i in range(0, len(self.objcode_3)):
            self.symbolTable2.append(self.objcode_3[i][2:])
            self.inst_ref[self.objcode_3[i][2:]] = self.objcode_3[i][:2]


        ref = "ref"
        for symbol in self.symbolTable2:
            if symbol not in self.symbolTable:
                self.symbolTable[symbol] = ref+ str(self.ref_num)
                self.ref_num+=1  
        
           
                 
    def create_symbol_table(self):
       
        with open(self.symbolTable_path, 'w') as file2:
            file2.write("SYMBOLTABLE \t REFERNCES \n")
            for key, value in self.symbolTable.items():
                file2.write(f"{key} \t\t\t {value} \n") 
        

    
                  


   
def call_objectcode(f,s):
 for i in range (1 ,len(f.lines)-1): 
    s.get_trecord_objectCode(f,i)        


def mainfun(f,s):
   
    f.open_file()
    s.get_H_record(f)
    call_objectcode(f,s)
    s.get_trecord_symbolTable()
    s.create_symbol_table()
    
   
    


if __name__ == '__main__':
   
        f=File()
        s=Symbol()
       
        mainfun(f,s)
   