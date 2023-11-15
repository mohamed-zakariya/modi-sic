import dic as d
import symbolTable as st


class assembly:    
    def __init__(self):
        self.assembly_path = "assembly.txt"
        self.assemblyTable = []
        self.locationCounter = []
        self.start_t_record={}
        self.wb = []
        self.reswb = []

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
                    break;
                i += 1

        unique_data = list(set(tuple(row) for row in self.reswb))   
        unique_data = [list(row) for row in unique_data]
        self.reswb = sorted(unique_data, key=lambda x: int(x[0], 16)) 

      
        

            
    def save_objectCodes(self, s, f):
    
        i = 1
        j = 0
        counter = 0
        while i < len(f.lines)-1:
            objcodes = f.lines[i][9:-1]
            j = 0
            while j < len(objcodes):
                opCode = objcodes[j:j+2]
                if opCode in s.objcode_1:
                    s.objectCodes.append(objcodes[j:j+2])
                    j = j+2
                else:
                    s.objectCodes.append(objcodes[j:j+6])
                    j = j+6
                
                counter += 1
 
            i += 1
        return   counter  
    
    def check_res(self, target_value):
        i = 0
        while i < len(self.reswb):
            if target_value == self.reswb[i][0]:
                return False
            i += 1
        return True


    def get_assembly_code(self, s,f):
        pointerLC = hex(int(s.hRecord["start"], 16))
        pointerLC = pointerLC[2:]
        end = s.hRecord["end"]
        self.locationCounter.append(pointerLC)

        counter = self.save_objectCodes(s, f)
        self.get_resw(s)

        i = 0
        while i < counter:
    
            if pointerLC not in s.symbolTable and s.objectCodes[i] in s.objcode_1:
                pointerLC = hex(int(pointerLC, 16) +1)
            
            
            elif pointerLC not in s.symbolTable  or pointerLC in s.symbolTable and s.inst_ref[pointerLC] in d.opCode_j:
                pointerLC = hex(int(pointerLC, 16) + 3)


            elif pointerLC in s.symbolTable and s.inst_ref[pointerLC] in d.opcode_3 and  self.check_res(pointerLC):
                self.wb.append(pointerLC)
                pointerLC = hex(int(pointerLC, 16) + int(len(s.objectCodes[i]) / 2))

            else:
                pointerLC = hex(int(pointerLC, 16) + int(self.get_resw_element()))
                i -=1

            pointerLC = pointerLC[2:].upper()
            self.locationCounter.append(pointerLC)
            i += 1 


        


