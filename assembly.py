import dic as d
import symbolTable as st


class assembly:    
    def __init__(self):
        self.assembly_path = "assembly.txt"
        self.locationCounter = []
        self.start_t_record={}
        self.wb = []
        self.reswb = []


    def get_diff(start_t_record):
        for i in range (len(start_t_record)):
            if(hex(int(start_t_record[i+1],16)-int(start_t_record[i],16)) not in start_t_record[i]):
                return start_t_record[i],start_t_record[i+1]


    def get_resw(self, s):
        for key in s.inst_ref.keys():
            i = 0
            while i < len(s.recordLimits)-1:
                lower_limit = int(s.recordLimits[i][1], 16)
                upper_limit = int(s.recordLimits[i+1][0], 16)
                value = int(key, 16)
                # print(key)
                # print( not ( lower_limit <= value < upper_limit) )
                if   (lower_limit <= value < upper_limit)  and key in s.inst_ref and key not in self.reswb:
                    print(s.recordLimits[i][1], " -> ",key, " -> ", s.recordLimits[i+1][0], "key is ", key)
                    self.reswb.append([key, s.recordLimits[i+1][0]])
                    break;
                i += 1

        sort = sorted(self.reswb, key=lambda x: int(x[0], 16)) 
        unique_data = list(set(tuple(row) for row in sort))   
        self.reswb = [list(row) for row in unique_data]
        # sort = sorted(int(x, 16) for x in self.reswb)
        # self.reswb = [hex(x)[2:].upper() for x in sorted_data]

            
    def save_objectCodes(self, s, f):
    
        i = 1
        j = 0
        counter = 0
        while i < len(f.lines)-1:
            objcodes = f.lines[i][9:-1]
            j = 0
            while j < len(objcodes):
            # print(opCode, ' ->', i, '->', )
                opCode = objcodes[j:j+2]
                if s.check_Format1():
                    s.objectCodes.append(objcodes[j:j+2])
                    j = j+2
                else:
                    s.objectCodes.append(objcodes[j:j+6])
                    j = j+6
                
                counter += 1
 
            i += 1
        # print(objectCodes)
        return   counter  
    
    def get_assembly_code(self, s,f):
        pointerLC = hex(int(s.hRecord["start"], 16) +3)
        pointerLC = pointerLC[2:]
        end = s.hRecord["end"]
        self.locationCounter.append(pointerLC)

        counter = self.save_objectCodes(s, f)
        self.get_resw(s)

        i = 0
        # pointerLC != end
        while i < counter:
            # if self.get_diff(self.start_t_record):
            #     # self.get_res(locationCounter)
            #     print(1)
            # print(pointerLC)   
            if pointerLC not in s.symbolTable :
                pointerLC = hex(int(pointerLC, 16) +3)
                pointerLC = pointerLC[2:].upper()
                # print("1")


            elif pointerLC in s.symbolTable and s.inst_ref[pointerLC] in d.opCode_j:
                pointerLC = hex(int(pointerLC, 16) +3)
                pointerLC = pointerLC[2:].upper()
                # print("2")

            elif pointerLC in s.symbolTable and s.inst_ref[pointerLC] in d.opcode_3:
                self.wb.append(pointerLC)
                pointerLC = hex(int(pointerLC, 16) + int(len(s.objectCodes[i]) / 2))
                pointerLC = pointerLC[2:].upper()
                # print("3")
            
            
            self.locationCounter.append(pointerLC)
            i += 1 
        # print(self.locationCounter)



        


