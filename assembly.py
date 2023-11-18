import dic as d
import symbolTable as st


class assembly:    
    def __init__(self):
        self.assembly_path = "assembly.txt"
        self.locationCounter = []
        self.start_t_record={}
        self.wb = []
        self.reswb = []
        self.code_counter=0
        self.assembly_lines=[]
        self.lines_number=0
        self.flaf_3=True
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
                
            
                if(lower_limit <= value < upper_limit)  and key in s.inst_ref and key not in self.reswb:
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
        pointerLC = pointerLC[2:]
        
        self.locationCounter.append(pointerLC)

        self.save_objectCodes(s)
        self.get_resw(s)
        self.get_res_index()
        
        i = 0
       
        while i < self.code_counter:
            
            # not a ref and format 1 will count 1    
            if pointerLC not in s.symbolTable and s.objectCodes_all[i] in s.objcode_1:
                pointerLC = hex(int(pointerLC, 16) +1)
            

            #if it is jump + 3
            elif pointerLC not in s.symbolTable  or (pointerLC in s.symbolTable and s.inst_ref[pointerLC] in d.opCode_j):
                pointerLC = hex(int(pointerLC, 16) + 3)

            # if it is byte or word
            elif pointerLC in s.symbolTable and s.inst_ref[pointerLC] in d.opcode_3 and  self.check_res(pointerLC):
                #print(s.objectCodes_all[i])
                self.wb_values.append(s.objectCodes_all[i][2:])
                self.wb.append(pointerLC)
                pointerLC = hex(int(pointerLC, 16) + int(len(s.objectCodes_all[i]) / 2))
                
            #if it is res
            else:
                pointerLC = hex(int(pointerLC, 16) + int(self.get_resw_element()))
                #print(pointerLC)
                i -=1

            pointerLC = pointerLC[2:].upper()
            self.locationCounter.append(pointerLC)
            i += 1 
            
        self.modi_wb()
       
   
       
        
    def create_first_assembly_line(self,s):
        self.assembly_lines.append(['0',s.programName,'START',s.start])
        self.lines_number=int(s.start,16)
       
        self.end=int(s.end,16)
        #self.end=hex(self.end)[2:]
        

    def check_labels(self,s,current_line):
        if current_line in s.symbolTable:  
                   
            return s.symbolTable[current_line]  
        
    def get_instruction_name(self,s,i):
         if s.all_opcodes[i] in d.opcode_1:
           self.flaf_3=False
           return d.opcode_1[s.all_opcodes[i]]
         elif s.all_opcodes[i] in d.opcode_3:
           self.flaf_3=True
           return d.opcode_3[s.all_opcodes[i]]
         
         
    def get_labels(self,s,i):
       
        if s.objectCodes_all[i][2:] in s.symbolTable:
            
           
            return s.symbolTable[s.objectCodes_all[i][2:]]
        
    def get_res_size(self,i):
        differ=int(self.locationCounter[i+1],16)-int(self.locationCounter[i],16)
        
        return differ

            
    def create_assembly_lines(self,s):
      i=0
      j=0
      self.locationCounter.append(s.end) 
     
     
      while int(self.locationCounter[i],16)!= self.end:
         
          ref=self.check_labels(s,self.locationCounter[i])
         
         
          if(self.locationCounter[i] in self.wb and j< self.code_counter):
                  value="x'{}'".format(s.objectCodes_all[j])
                
                  self.assembly_lines.append([self.locationCounter[i],ref,'BYTE',value,s.objectCodes_all[j]])

                  if s.objectCodes_all[j][2:] in s.symbolTable:
                          del s.symbolTable[s.objectCodes_all[j][2:] ]
                  s.create_symbol_table()    
                  j+=1
                  
          elif(self.locationCounter[i] in self.res_index and i< self.code_counter):
              size=self.get_res_size(i)
              self.assembly_lines.append([self.locationCounter[i],ref,'RESB',size])
           
          elif(j< self.code_counter):
              
              instruction=self.get_instruction_name(s,j)
              label=self.get_labels(s,j)
              self.assembly_lines.append([self.locationCounter[i],ref,instruction, label ,s.objectCodes_all[j]])
              j+=1

          i+=1
             

    def modi_wb(self):
        i = 0
        
        while i < len(self.wb_values):
            if self.wb_values[i] in self.locationCounter:
                
                try:
                    self.wb.remove(self.wb_values[i])
                    
                except ValueError:
                    print(f"ValueError: {self.wb_values[i]} not found in self.wb")
                 
            i += 1
            
    
   
    



        


