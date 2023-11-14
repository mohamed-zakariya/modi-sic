import dic as d
import assembly as a
import symbolTable as st


def mainfun(f,s, ass):
   
    f.open_file()
    s.get_H_record(f)
    st.call_objectcode(f,s)
    s.get_trecord_symbolTable()
    s.create_symbol_table()
    # print(f.lines)
    # s.get_H_record(f.lines)
    # print(s.objcode_3)
    # print(s.objcode_3_imm)
    # print(ass.var)
    # print(s.objectCodes)
    # print(s.inst_ref)
    print("hhhhhh")
    # print(s.hRecord)
    print(s.inst_ref)
    ass.get_assembly_code(s, f)
    # print(ass.wb)
    ass.get_resw(s)
    print(ass.locationCounter)
    print(ass.reswb)
    # print (int("1000", 16) < int("101F", 16) < int("101E", 16))

if __name__ == '__main__':
   
        f=st.File()
        s=st.Symbol()
        ass = a.assembly()

        mainfun(f, s, ass)