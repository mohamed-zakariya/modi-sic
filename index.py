def get_H_record(Hline):
    title = Hline[0][1:7]
    print(title)
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
    print(start)
    print(end)
    return [programName, start, end]

file_path = 'HTE.txt'
with open(file_path, 'r') as file:
    content = file.read()
    # print(content[0])
    file.seek(0)
    lines = file.readlines()
    # print(lines[0][0])
    # for line in lines:
    #     print(line)
    hRecord =  get_H_record(lines)
    print(hRecord)
    
    # print(get_H_record(lines))



    
        