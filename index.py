import dic as d
def get_H_record(Hline):
    title = Hline[0][1:7]
    # print(title)
    programName = ""
    flag = 1;
    first = 1;
    for letter in reversed(title):
        # print(programName)
        if letter != 'X' and first == 1:
            first = 0
            flag = 0
            programName += letter

        elif letter == 'X' and flag == 1:
            continue

        elif letter != 'X' or (letter == 'X' and first == 0): 
            flag = 0
            programName += letter
            

    programName = programName[::-1]
    
    start = Hline[0][7:13]
    length = Hline[0][13:19]
    end = int(start, 16) + int(length, 16)
    end = hex(end).upper()
    end = end[2:]
    start = int(start, 16)
    start = hex(start).upper()
    start = start[2:]
    # print(start)
    # print(end)
    return [programName, start, end]
    
def check_Format1(opCode):
    return opCode in d.opcode_1

def check_dic(opCode):
    return opCode in d.opcode_3

def check_imd(opCode):
  bit8 = bin(int(opCode, 16)).upper()
  bit8 = bit8[-1]
#   print(bit8)
  return bit8 == '1'


def save_objectCodes(tline):
    
    i = 1
    j = 0
    counter = 0
    while i < len(tline)-1:
        objcodes = tline[i][9:-1]
        j = 0
        while j < len(objcodes):
        # print(opCode, ' ->', i, '->', )
            opCode = objcodes[j:j+2]
            if check_Format1(opCode):
                objectCodes.append(objcodes[j:j+2])
                j = j+2
            else:
                objectCodes.append(objcodes[j:j+6])
                j = j+6
            
            counter += 1

        i += 1
    print(objectCodes) 
    return   counter     
    


def get_trecord_objectCode3(tline, j):
    objcodes = tline[j][9:-1]
    
    i = 0
    while i < len(objcodes):
        opCode = objcodes[i:i+2]
        # print(opCode, ' ->', i, '->', )

        if check_Format1(opCode):
            objcode_1.append(opCode)
            i = i+2
        elif check_dic(opCode) and check_imd(opCode):
            objcode_3_imm.append(objcodes[i:i+6])
            i = i+6
        elif check_dic(opCode):
            objcode_3.append(objcodes[i:i+6])
            i = i+6
        else:
            i = i+6
    # print(objcode_3)        
    return objcode_3
    # print(objcode_1, '@', objcode_3)

def get_trecord_symbolTable(tline, symbolTable, j, m):
    address = get_trecord_objectCode3(tline, j)
    # print(objCode)
    symbolTable2 = []
    for i in range(0, len(address)):
        symbolTable2.append(address[i][2:])
        inst_ref[address[i][2:]] = address[i][:2]


    ref = "ref"
    for symbol in symbolTable2:
        if symbol not in symbolTable:
            symbolTable[symbol] = ref+ str(m)
            m = m + 1 

    return m                



hte_path = 'HTE.txt'

#assembly table
def get_assembly_code(hrecord):
    locationCounter = []
    pointerLC = hex(int(hrecord[1], 16) +3)
    pointerLC = pointerLC[2:]
    end = hrecord[2]
    locationCounter.append(pointerLC)
    print(pointerLC)
    # pointerLC = hex(int(pointerLC, 16) +3)
    # pointerLC = pointerLC[2:]
    print(end)


    counter = save_objectCodes(lines)

    i = 0
    # pointerLC != end
    while i < counter:
        if pointerLC not in symbolTable:
            pointerLC = hex(int(pointerLC, 16) +3)
            pointerLC = pointerLC[2:]
            locationCounter.append(pointerLC)


        elif pointerLC in symbolTable and pointerLC in d.opCode_j:
            pointerLC = hex(int(pointerLC, 16) +3)
            pointerLC = pointerLC[2:]
            locationCounter.append(pointerLC)

        else:
            pointerLC = hex(int(pointerLC, 16) + int(len(objectCodes[i]) / 2))
            pointerLC = pointerLC[2:]
            locationCounter.append(pointerLC)
            

        print(pointerLC)
        i += 1  
    print(i)
    # print(locationCounter)




with open(hte_path, 'r') as file:
    content = file.read()
    # print(content[0])
    file.seek(0)
    lines = file.readlines()
    
    # print(lines[0][0])
    # for line in lines:
    #     print(line)
    hRecord =  get_H_record(lines)
    # print(hRecord)
    j = 1
    i = 1
    k = 1
    m = 0

    objectCodes = []
    objcode_1 = []
    objcode_3 = []
    objcode_3_imm = []

    symbolTable = {}
    inst_ref = {}
    # get_trecord_symbolTable(lines, symbolTable, 1)

    while k < len(lines)-1:
        m = get_trecord_symbolTable(lines, symbolTable, k, m)
        k = k+1;
    
    # print(objcode_1)
    # print(objcode_3_imm)
    print(symbolTable)
    # print(inst_ref)

    print(hRecord)

    get_assembly_code(hRecord)



symbolTable_path = "symbolTable.txt"
with open(symbolTable_path, 'w') as file2:
    file2.write("SYMBOLTABLE \t REFERNCES \n")
    for key, value in symbolTable.items():
        file2.write(f"{key} \t\t\t {value} \n")

    # print(get_H_record(lines))



    
        