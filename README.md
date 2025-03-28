# Virtual Machine Interpreter

This Virtual Machine (VM) is a lightweight computing environment implemented in Python that follows the fundamental fetch-decode-execute cycle of computer architecture. The VM processes assembly-like instructions from a text source file (`myVM_Prog.txt`) and generates output in a separate file (`myVM_Output.txt`).

## Features

### Core Functionality
- **Instruction Processing Pipeline**:
  - **Load Phase**: Reads instructions sequentially from the input file
  - **Decode Phase**: Parses each instruction into operation and operands
  - **Execute Phase**: Performs the specified operation
  - **Program Counter**: Automatically increments after each operation (with exceptions for jump commands)

### Supported Operations
| Category        | Commands                          |
|-----------------|-----------------------------------|
| Arithmetic      | `ADD`, `SUB`, `MUL`, `DIV`       |
| Memory          | `STO` (store), `IN` (user input) |
| Control Flow    | `JMP`, `BRn`, `BRp`, `BRz`       |
| I/O             | `OUT` (output to file)           |

### Memory Management
- Fixed-size memory (default 500 addressable locations)
- Symbol table for variable and label storage
- Automatic memory bounds checking

## Getting Started

### Prerequisites
- Python 3.x

### Usage
1. Create your program in `myVM_Prog.txt`:
   ```plaintext
   STO X 5
   STO Y 10
   ADD Z X Y
   OUT Z
   HALT

2. Run/execute the file `myVM.py`
   
3. View the Results inside `myVM_Output.txt`
