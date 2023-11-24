<h1 align="center"> modi-sic Disassembler </h1> 

###### The primary objective of this project is to disassemble High-Level Assembler (HTE) records, extracting information to populate a SYMBOL table and generate corresponding ASSEMBLY code. By dissecting the HTE records, the system aims to provide a comprehensive disassembly of the code, enhancing the understanding and usability of the SYMBOL table and ASSEMBLY code components.

## Symbol Table Functionality (symbolTable.py)

To observe the functionality of the `symbolTable.py` script, follow these step-by-step instructions:

1. **Open Terminal/Command Prompt:**
   - Open a terminal or command prompt on your system.

2. **Run the Script:**
   - Execute the script using the Python interpreter.
     ```bash
     python symbolTable.py
     ```

### Design Issues:

- **Objective:**
  - To establish references to memory addresses, the initial approach involves placing object codes in the symbol table. This ensures that all object codes, including those associated with words and bytes, can be referenced using their respective addresses.

- **Challenge:**
  - A critical consideration arises in the removal of these entries from the symbol table. The deletion of entries, necessary for maintaining an accurate symbol table, is contingent upon the successful execution of the assembly's functionality.


## Assembly Code Execution (assembly.py)

To observe the functionality of the `assembly.py` script, follow these step-by-step instructions:

1. **Open Terminal/Command Prompt:**
   - Open a terminal or command prompt on your system.

2. **Run the Script:**
   - Execute the script using the Python interpreter.
     ```bash
     python assembly.py
     ```

### Design Issues:

- **Objective:**
  - The assembly code's seamless execution relies significantly on the availability of references to memory addresses, which are meticulously managed within the symbol table.

- **Challenge:**
  - A pivotal design consideration revolves around the interdependence of the assembly code and the symbol table. The assembly code's effective functioning necessitates accurate references to memory addresses, all orchestrated through the symbol table.


## Main Program Execution (main.py)

To observe the functionality of the `main.py` script, follow these step-by-step instructions:

1. **Open Terminal/Command Prompt:**
   - Open a terminal or command prompt on your system.

2. **Run the Script:**
   - Execute the script using the Python interpreter.
     ```bash
     python main.py
     ```

### Design Issues:

- **Object Code Handling in Symbol Table:**
  - Initial placement of object codes in the symbol table.
  - Delayed removal of entries, impacting the accuracy of the symbol table.

- **Address Reference Dependency:**
  - Assembly code's dependency on the symbol table for address references.
  - Synchronization challenges with changes in the symbol table during execution.



