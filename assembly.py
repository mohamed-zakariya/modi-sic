import dic as d
import symbolTable as st


class assembly:    
    def __init__(self):
        self.assembly_path = "Outputs/assembly.txt"
        self.locationCounter = []
        self.start_t_record={}
        self.wb = []
        self.reswb = []
        self.code_counter=0
        self.assembly_lines=[]
        self.lines_number=0
        self.end=0
        self.assemblyTable = []
        self.wb = []
        self.reswb = []
        self.res_index=[]
        self.wb_values = []

   
    
    def save_objectCodes(self, s):
        self.code_counter=len(s.objectCodes_all)
      


    def get_resw_element(self):
    
        if len(self.reswb) > 1:
            
            if(int(self.reswb[1][0], 16) - int(self.reswb[0][0], 16) < int(self.reswb[0][1], 16) - int(self.reswb[0][0], 16)):
                diff = int(self.reswb[1][0], 16) - int(self.reswb[0][0], 16)

            else:
                diff = int(self.reswb[0][1], 16) - int(self.reswb[0][0], 16)
                
            self.reswb.pop(0)
            return diff
        diff = int(self.reswb[0][1], 16) - int(self.reswb[0][0], 16)
        self.reswb.pop(0)
        
        return diff
    
    
    def get_resw(self, s):
        for key in s.inst_ref.keys():
            i = 0
            while i < len(s.recordLimits)-1:
                lower_limit = int(s.recordLimits[i][1], 16)
                upper_limit = int(s.recordLimits[i+1][0], 16)
                value = int(key, 16)
            
                if(lower_limit <= value < upper_limit)  and key in s.inst_ref:
                    self.reswb.append([key, s.recordLimits[i+1][0]])
                    break
                i += 1

        unique_data = list(set(tuple(row) for row in self.reswb))   
        unique_data = [list(row) for row in unique_data]
        self.reswb = sorted(unique_data, key=lambda x: int(x[0], 16)) 
        
    def get_res_index(self):
        self.res_index=[sublist[0] for sublist in self.reswb]   

    def check_res(self, target_value):
        i = 0
        while i < len(self.reswb):
            if target_value == self.reswb[i][0]:
                return False
            i += 1
        return True
    
   
    def get_assembly_code(self, s,f):
        pointerLC = hex(int(s.start,16))
        pointerLC = pointerLC[2:].upper()
        pointerLC = pointerLC.zfill(4)
        
        self.locationCounter.append(pointerLC)
        self.create_first_assembly_line(s)
        self.save_objectCodes(s)
        self.get_resw(s)
        self.get_res_index()
        self.end = hex(self.end).upper()
        self.end = self.end[2:]
        
        i = 0
       
        while pointerLC <= self.end:
            
            if pointerLC not in s.symbolTable and i < self.code_counter and s.objectCodes_all[i] in s.objcode_1:
                pointerLC = hex(int(pointerLC, 16) +1)
            

            elif pointerLC not in s.symbolTable  or (pointerLC in s.symbolTable and s.inst_ref[pointerLC] in d.opCode_j):
                pointerLC = hex(int(pointerLC, 16) + 3)

            elif pointerLC in s.symbolTable and i < self.code_counter and  s.inst_ref[pointerLC] in d.opcode_3 and  self.check_res(pointerLC):
                self.wb_values.append(s.objectCodes_all[i][2:])
                self.wb.append(pointerLC)
                pointerLC = hex(int(pointerLC, 16) + int(len(s.objectCodes_all[i]) / 2))
                
            else:
                pointerLC = hex(int(pointerLC, 16) + int(self.get_resw_element()))
                i -=1
            pointerLC = hex(int(pointerLC, 16))
            pointerLC = pointerLC[2:].upper()
            pointerLC = pointerLC.zfill(4)

            self.locationCounter.append(pointerLC)
            i += 1 
            
        self.modi_wb()
       
   
       
        
    def create_first_assembly_line(self,s):
        self.assembly_lines.append(['0',s.programName ,'START',s.start, "None"])
       
        self.end=int(s.end,16)
        
    def create_last_assembly_line(self,s):
        self.assembly_lines.append([self.locationCounter[-2],"None" ,'END', s.start, "None"])

    def check_labels(self,s,current_line):
        if current_line in s.symbolTable:
                   
            return s.symbolTable[current_line]  
        
    def get_instruction_name(self,s,i):
         if s.all_opcodes[i] in d.opcode_1:
          
           return d.opcode_1[s.all_opcodes[i]]
         elif s.all_opcodes[i] in d.opcode_3:
          
           return d.opcode_3[s.all_opcodes[i]]
         
         
    def get_labels(self,s,i):
        value = s.check_indexing(s.objectCodes_all[i])
        value = value[2:]
        if value in s.symbolTable:
            return s.symbolTable[value]
        
    def get_res_size(self,i):
        differ=int(self.locationCounter[i+1],16)-int(self.locationCounter[i],16)
        
        return differ

    def check_indexing(self, s, i):
        value = s.objectCodes_all[i]
        bit_1 = int(value[2], 16)
        return bit_1 >= 8
    
            
    def create_assembly_lines(self,s):
        i=0
        j=0
        self.locationCounter.append(s.end) 
        self.locationCounter.append("000")    
        #print(s.symbolTable)
        self.modifiy_symbol_table(s)
        #print(s.symbolTable)
        while self.locationCounter[i] != "000":
            ref=self.check_labels(s,self.locationCounter[i])

            lc = self.locationCounter[i]
            
            if(self.locationCounter[i] in self.wb and j< self.code_counter):
                   
                    value_int = int(s.objectCodes_all[j], 16)

                    self.assembly_lines.append([lc ,ref,'BYTE',"x'"+s.objectCodes_all[j]+"'",s.objectCodes_all[j]])
                    j+=1
                    
            elif(self.locationCounter[i] in self.res_index):
                size=self.get_res_size(i)
                self.assembly_lines.append([lc,ref,'RESB',size, "None"])
            
            elif(j< self.code_counter):
                instruction=self.get_instruction_name(s,j)
                label= str(self.get_labels(s,j))
                if self.check_indexing(s, j): 
                    self.assembly_lines.append([lc, ref,instruction, label+",x" ,s.objectCodes_all[j]])
                else:
                    self.assembly_lines.append([lc, ref,instruction, label ,s.objectCodes_all[j]])
                j+=1  
            i+=1
        self.create_last_assembly_line(s)     
    
    def create_assembly_table(self):
       
        with open(self.assembly_path, 'w') as file2:
            file2.write("Location Counter\tLabel\t\tInstruction\t    Reference\t    ObjectCode\n")
            for i in range(len(self.assembly_lines)):
                file2.write(f"{str(self.assembly_lines[i][0]):<19}\t{str(self.assembly_lines[i][1]):<10}"
                            f"\t{str(self.assembly_lines[i][2]):<12}\t{str(self.assembly_lines[i][3]):<12}"
                            f"\t{str(self.assembly_lines[i][4])}\n")

            file2.write("\n")

    
    
    def modi_wb(self):
        i = 0
        
        while i < len(self.wb_values):
            if self.wb_values[i] in self.locationCounter:
                
                try:
                    self.wb.remove(self.wb_values[i])
                    
                except ValueError:
                    print(f"ValueError: {self.wb_values[i]} not found in self.wb")
                 
            i += 1
            
    
    def modifiy_symbol_table(self,s):
        i=0
        j=0
        print(self.wb)
        while self.locationCounter[i] != "000":    
            if(self.locationCounter[i] in self.wb and j< self.code_counter):
                    print("location",self.locationCounter[i])
                    print("befor", s.objectCodes_all[j][2:]) 
                    if s.objectCodes_all[j][2:] in s.symbolTable:
                            #print(j)
                            print("after", s.objectCodes_all[j][2:])
                            del s.symbolTable[s.objectCodes_all[j][2:] ]
                            
            elif(self.locationCounter[i] in self.res_index): 
                i+=1 
                continue

            s.create_symbol_table()                        
            i+=1
            j+=1
        print(i)


        


