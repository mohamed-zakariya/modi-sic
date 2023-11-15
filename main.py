import dic as d
import assembly as a
import symbolTable as st


def mainfun(f,s, ass):
   
    f.open_file()
    s.get_H_record(f)
    st.call_objectcode(f,s)
    s.get_trecord_symbolTable()
    s.create_symbol_table()
    
    print(s.inst_ref)
    ass.get_assembly_code(s, f)
    print(ass.locationCounter)

if __name__ == '__main__':
   
        f=st.File()
        s=st.Symbol()
        ass = a.assembly()

        mainfun(f, s, ass)