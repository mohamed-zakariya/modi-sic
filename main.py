import dic as d
import assembly as a
import symbolTable as st


def mainfun(f,s, assem):
   
    f.open_file()
    s.get_H_record(f)
    st.call_objectcode(f,s)
    s.get_trecord_symbolTable()
    #s.create_symbol_table()
    assem.get_assembly_code(s, f)
    #assem.save_objectCodes(s)
    assem.create_first_assembly_line(s)
    
    # print(assem.res_index)
    assem.create_assembly_lines(s)
    # print(assem.assembly_lines)
    print(s.objectCodes)
    # print(s.objectCodes_all)
    # print( s.inst_ref)
if __name__ == '__main__':
   
        f=st.File()
        s=st.Symbol()
        assem = a.assembly()

        mainfun(f, s, assem)