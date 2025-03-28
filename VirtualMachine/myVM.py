# This is my Virtual Machine class
class VIRTUALMACHINE:
    # The initialization function
    def __init__(self, MAX_MEMORY_SIZE = 500, PROGRAMCOUNTER = 0):
        self.MAX_MEMORY_SIZE = MAX_MEMORY_SIZE
        self.PROGRAMCOUNTER = PROGRAMCOUNTER
        self.MEMORY = [""] * MAX_MEMORY_SIZE  # This initializes the memory list to a max size of MAX_MEMORY_SIZE
        self.DESCRIPTOR = {} # The descriptor is what holds the variables and labels
        self.CURRENTLINE = 0 # This is a ProgramCounter holder
        self.WRITTENTOLINE = 0 # This keeps track of what line the executor needs to write to. 
        self.PASTJUMP = False  # This helps the program know if it needs to break out of the line by line for loop to go back to previously visited memory.
        self.ISHALTED = False # This boolean value helps the program detemrine if the program has been halted from HALT
        
    def LOADPHASE(self):  
        # This phase loads the text into memory
        
        # Clears the output file
        open('myVM_Output.txt', 'w').close()
        
        # Reset the line on loop
        self.CURRENTLINE = 0
        self.PROGRAMCOUNTER = 0 

        while (not self.ISHALTED): # while the program has not been halted
            
            # Open the file in read mode
            with open('myVM_Prog.txt', 'r') as FILE:
            
                
            # Read the file line by line
                LINES = FILE.readlines() 
                for LINE in LINES[self.CURRENTLINE:]: # keeps track of the line currently being worked with
                    self.CURRENTLINE += 1

                    # skip the lines when jumping to other lines and do not load the skipped lines into memory
                    if(self.CURRENTLINE < self.PROGRAMCOUNTER):
                        continue
                
                    # Skip comments and do not load them into memory
                    if LINE.strip().startswith(";"):
                      continue 
            
                    if self.PROGRAMCOUNTER < self.MAX_MEMORY_SIZE: # if the program counter exceeds memory size then that means the memory is full
                        self.MEMORY[self.PROGRAMCOUNTER] = LINE.strip("\n") #fetch
                        self.PROGRAMCOUNTER += 1 #increment program counter
                        self.DECODEPHASE()  # Decode
                        
                    else:
                        print("Memory is full")
                        break
                    
                    # If the program needs to go to memory in an earlier visited line
                    # it will break out of looping through the lines and go back
                    if (self.PASTJUMP):
                        self.PASTJUMP = False
                        break
                        
                self.CURRENTLINE = 0

    def DECODEPHASE(self):
        
        # This phase decodes the instructions in memory
        INSTRUCTION = self.MEMORY[self.PROGRAMCOUNTER - 1]

        WORDS = INSTRUCTION.split() # Splits the intruction into individual words
        
        # This word will decide what the program will do
        COMMANDWORD = WORDS[0] 
        
        ## Initial post save requirement 
        self.STOREINOUTPUTFILE("myVM_Output.txt", 0, "Noah Sylvester, CSCI 4200, Spring 2025")
        self.STOREINOUTPUTFILE("myVM_Output.txt", 1, "**********************************************")

        # This command word halts the program
        if COMMANDWORD != "HALT": 
            
            # This word will decide what the program will do with the command
            VARSANDNUMS = WORDS[1:]
            
            # The following if else if tree decodes the instruction's command word
            if COMMANDWORD == "ADD":
                SUM = VARSANDNUMS[0] # sum is a reference to the variable that is being stored
                VALUE1 = VARSANDNUMS[1] # value 1 is the second word in VarsAndNums, this is the first number
                VALUE2 = VARSANDNUMS[2] # value 2 is the third word in VarsAndNums, this is the second number
                RESULT = self.ADD(SUM, VALUE1, VALUE2) # assigns result to the result of value 1 and value2
                return 
            
            elif COMMANDWORD == "SUB": # This handles when the command word is SUB for subtraction
                RESULT = VARSANDNUMS[0] 
                VALUE1 = VARSANDNUMS[1]
                VALUE2 = VARSANDNUMS[2]
                RESULT = self.SUB(RESULT, VALUE1, VALUE2) # calls Sub to subtract 
                return
            
            elif COMMANDWORD == "MUL": # This handles when the command word is MUL for multiplication
                PRODUCT = VARSANDNUMS[0]
                VALUE1 = VARSANDNUMS[1]
                VALUE2 = VARSANDNUMS[2]
                RESULT = self.MUL(PRODUCT, VALUE1, VALUE2) # Calls Mul to multiply value 1 and value 2 together
                return
            
            elif COMMANDWORD == "DIV": # This handles when the command word is DIV for division
                QUOTIENT = VARSANDNUMS[0]
                VALUE1 = VARSANDNUMS[1]
                VALUE2 = VARSANDNUMS[2]
                RESULT = self.DIV(QUOTIENT, VALUE1, VALUE2) # Calls Div to divide value 1 and value2, store in quotient
                return
            
            elif COMMANDWORD == "STO": # This handles when the command word is STO for store
                STORE = VARSANDNUMS[0]
                VALUE = VARSANDNUMS[1]
                self.STORE(STORE,VALUE) # Calls Store to store a value in the variable 
                return
            
            elif COMMANDWORD == "OUT": # This handles when the command word is OUT for printing
                OUTWORD = ' '.join(WORDS[1:]) # I convert the word or varibal entered into a string with spaces, rather than being connected
                RESULT = self.OUT(OUTWORD) # call Out function with the OutWord and keep track of the result
                self.WRITTENTOLINE += 1 # increment the line number that has been written to
                self.STOREINOUTPUTFILE("myVM_Output.txt", self.WRITTENTOLINE + 1, RESULT) # This stores the output in the output file.
                return
            
            elif COMMANDWORD == "IN": # This handles when the command word is IN for a variable
                RESULT = self.IN(VARSANDNUMS[0])
                return
            
            elif COMMANDWORD == "JMP": # This handles when the command word is JMP for jumping to different lines
                LABEL = VARSANDNUMS[0] # keep track of the label
                LINENUMBER = self.GOTOLABELS(LABEL) # This keeps track of the LineNumber that JMP needs to go to   
                self.PROGRAMCOUNTER = LINENUMBER # Set the program counter to the Line Number

                # Mark that we need to restart if we are jumping backward
                if LINENUMBER < self.CURRENTLINE:
                    self.CURRENTLINE = LINENUMBER
                    self.PASTJUMP = True
                    
                return
                            
            elif COMMANDWORD == "BRn": # This handles when the command word is BRn
                VARIABLE = VARSANDNUMS[0] 
                LABEL = VARSANDNUMS[1] # Keep track of the label we would need to jmp to.
                RESULT = self.BRN(VARIABLE)
                if (RESULT == True): # If the result is true we need to jmp to the line number
                    LINENUMBER = self.GOTOLABELS(LABEL)
                    self.PROGRAMCOUNTER = LINENUMBER # set the program counter to the line we need to go to
                    return
                else:
                    return # return if we need to do nothing if the result is false.
                
            elif COMMANDWORD == "BRp": # This handles when the command word is BRp
                VARIABLE = VARSANDNUMS[0]
                LABEL = VARSANDNUMS[1]
                RESULT = self.BRP(VARIABLE)
                if (RESULT == True):
                    LINENUMBER = self.GOTOLABELS(LABEL) # This has the same output logic as BRn
                    self.PROGRAMCOUNTER = LINENUMBER
                    return
                else:
                    return
            
            elif COMMANDWORD == "BRz": # This handles when the command word is BRz
                VARIABLE = VARSANDNUMS[0]
                LABEL = VARSANDNUMS[1]
                RESULT = self.BRZ(VARIABLE)
                if (RESULT == True):
                    LINENUMBER = self.GOTOLABELS(LABEL)
                    self.PROGRAMCOUNTER = LINENUMBER
                    return
                else:
                    return
             
            elif COMMANDWORD == "BRzn": # This handles when the command word is BRzn
                VARIABLE = VARSANDNUMS[0]
                LABEL = VARSANDNUMS[1]
                RESULT = self.BRZN(VARIABLE)
                if (RESULT == True):
                    LINENUMBER = self.GOTOLABELS(LABEL)
                    self.PROGRAMCOUNTER = LINENUMBER
                    return
                else:
                    return
                
            elif COMMANDWORD == "BRzp": # This handles when the command word is BRzp
                VARIABLE = VARSANDNUMS[0]
                LABEL = VARSANDNUMS[1]
                RESULT = self.BRZP(VARIABLE)
                if (RESULT == True):
                    LINENUMBER = self.GOTOLABELS(LABEL)
                    self.PROGRAMCOUNTER = LINENUMBER
                    return
                else:
                    return
            
            # If the CommandWord is not an Identifier, it must be a label then.
            else:
                # This will store the label in the dictionary if the first character is a letter, as the requirements for this assignment
                # specified that it must be a letter followed by 0 or more letters, numbers, or underscores.
                if (COMMANDWORD[0].isalpha()):
                    self.STORE(COMMANDWORD) # Store the label

                else:
                    print (f"Not valid command word: {COMMANDWORD}") # Logic for when the label is not following the rules.
            
        else:
            self.ISHALTED = True # Setting this to true will halt the program's while not halted loop.
            return

    def STOREINOUTPUTFILE(self, FILENAME, LINE_NUMBER, RESULT):
        # Read the file
        with open(FILENAME, 'r') as FILE:
            LINES = FILE.readlines()

        #  Makes sure the file has enough lines
        while len(LINES) <= LINE_NUMBER:
            LINES.append("\n")  # Add another line after the previous

        # This updates the line with the content
        LINES[LINE_NUMBER] = f"{RESULT}\n"

        # Writes the updated content back to the file
        with open(FILENAME, 'w') as FILE:
            FILE.writelines(LINES)

    # This is the add function 
    def ADD(self, SUM, VALUE1, VALUE2):
        if(SUM.isalpha or SUM in self.DESCRIPTOR): # If sum is a variable or it is in the Descriptor
            if ((VALUE1 in self.DESCRIPTOR) and not (VALUE2 in self.DESCRIPTOR)):   # If value1 is in the descriptor but not value 2.
                self.DESCRIPTOR[SUM] = int(self.DESCRIPTOR[VALUE1]) + int(VALUE2) # adds the values and stores result in descriptor
                return self.DESCRIPTOR[SUM]
            
            elif ((VALUE2 in self.DESCRIPTOR) and not( VALUE1 in self.DESCRIPTOR)):# If value2 is in the descriptor but not value 1.
                self.DESCRIPTOR[SUM] = int(VALUE1) + int(self.DESCRIPTOR[VALUE2])# adds the values and stores result in descriptor
                return self.DESCRIPTOR[SUM]
            
            elif ((VALUE1 in self.DESCRIPTOR) and (VALUE2 in self.DESCRIPTOR)): # If both values are in the descriptor
                self.DESCRIPTOR[SUM] = int(self.DESCRIPTOR[VALUE1]) + int(self.DESCRIPTOR[VALUE2])# adds the values and stores result in descriptor
                return self.DESCRIPTOR[SUM]
            
            else:
                self.DESCRIPTOR[SUM] = int(VALUE1) + int(VALUE2) # adds the values and stores result in descriptor
                return self.DESCRIPTOR[SUM]

        else:
            RESULT = int(VALUE1) + int(VALUE2)     # adds the values and stores result in descriptor   
            return RESULT
        
    # This is the subtract function
    # The if statements are the same as the addition function above. See Add for comment details.
    def SUB(self, RESULT, VALUE1, VALUE2):
        if(RESULT.isalpha or RESULT in self.DESCRIPTOR):
            if ((VALUE1 in self.DESCRIPTOR) and not (VALUE2 in self.DESCRIPTOR)):
                self.DESCRIPTOR[RESULT] = int(self.DESCRIPTOR[VALUE1]) - int(VALUE2) # subtracts the values and stores result in descriptor
                return self.DESCRIPTOR[RESULT]
            
            elif ((VALUE2 in self.DESCRIPTOR) and not( VALUE1 in self.DESCRIPTOR)):
                self.DESCRIPTOR[RESULT] = int(VALUE1) - int(self.DESCRIPTOR[VALUE2])# subtracts the values and stores result in descriptor
                return self.DESCRIPTOR[RESULT]
            
            elif ((VALUE1 in self.DESCRIPTOR) and (VALUE2 in self.DESCRIPTOR)):
                self.DESCRIPTOR[RESULT] = int(self.DESCRIPTOR[VALUE1]) - int(self.DESCRIPTOR[VALUE2])# subtracts the values and stores result in descriptor
                return self.DESCRIPTOR[RESULT]
            
            else:
                self.DESCRIPTOR[RESULT] = int(VALUE1) - int(VALUE2)# subtracts the values and stores result in descriptor
                return self.DESCRIPTOR[RESULT]

        else:
            RESULT = int(VALUE1) - int(VALUE2)       # subtracts the values and stores result in descriptor
            return RESULT
        
    # This is the multiply function
    # If statement explanation same as Add function above
    def MUL(self, RESULT, VALUE1, VALUE2):
        if(RESULT in self.DESCRIPTOR):
            if (VALUE1 in self.DESCRIPTOR and not VALUE2 in self.DESCRIPTOR):
                self.DESCRIPTOR[RESULT] = int(self.DESCRIPTOR[VALUE1]) * int(VALUE2) # Multiplies the values and stores result in descriptor
                return self.DESCRIPTOR[RESULT]
            
            elif (VALUE2 in self.DESCRIPTOR and not VALUE1 in self.DESCRIPTOR):
                self.DESCRIPTOR[RESULT] = int(VALUE1) * int(self.DESCRIPTOR[VALUE2]) # Multiplies the values and stores result in descriptor
                return self.DESCRIPTOR[RESULT]
            
            elif (VALUE1 in self.DESCRIPTOR and VALUE2 in self.DESCRIPTOR):
                self.DESCRIPTOR[RESULT] = int(self.DESCRIPTOR[VALUE1]) * self.DESCRIPTOR[VALUE2] # Multiplies the values and stores result in descriptor
                return self.DESCRIPTOR[RESULT]
            
            else:
                self.DESCRIPTOR[RESULT] = int(VALUE1) * int(VALUE2) # Multiplies the values and stores result in descriptor
                return self.DESCRIPTOR[RESULT]
        else: 
            RESULT = int(VALUE1) * int(VALUE2) # Multiplies the values and stores result in descriptor
            return RESULT

    # This is the divide function
    # If statement explanation same as Add function above
    def DIV(self, QUOTIENT, VALUE1, VALUE2):
        if(QUOTIENT in self.DESCRIPTOR):
            if (VALUE1 in self.DESCRIPTOR and not VALUE2 in self.DESCRIPTOR):
                self.DESCRIPTOR[QUOTIENT] = int(self.DESCRIPTOR[VALUE1]) / int(VALUE2) # Multiplies the values and stores quotient in descriptor
                return self.DESCRIPTOR[QUOTIENT]
            
            elif (VALUE2 in self.DESCRIPTOR and not VALUE1 in self.DESCRIPTOR):
                self.DESCRIPTOR[QUOTIENT] = int(VALUE1) / int(self.DESCRIPTOR[VALUE2]) # Multiplies the values and stores quotient in descriptor
                return self.DESCRIPTOR[QUOTIENT]
            
            elif (VALUE1 in self.DESCRIPTOR and VALUE2 in self.DESCRIPTOR):
                self.DESCRIPTOR[QUOTIENT] = int(self.DESCRIPTOR[VALUE1]) / int(self.DESCRIPTOR[VALUE2]) # Multiplies the values and stores quotient in descriptor
                return self.DESCRIPTOR[QUOTIENT]
            
            else:
                self.DESCRIPTOR[QUOTIENT] = int(VALUE1) / int(VALUE2) # Multiplies the values and stores quotient in descriptor
                return self.DESCRIPTOR[QUOTIENT]
        else:
            QUOTIENT = int(VALUE1) / int(VALUE2) # Multiplies the values and stores quotient in descriptor
            return QUOTIENT

    # The In function will store a variable into a descriptor with a user inputted integer value; Ex: IN sum        User Input: 5
    def IN(self, VARIABLE):
        USER_INPUT = int(input()) # Retrieves the integer input from the user for what the value will be.
        self.DESCRIPTOR[VARIABLE] = USER_INPUT # Stores the variable and value into the descriptor.
        return self.DESCRIPTOR[VARIABLE]

    # This is the out function, this function will print and return the string or numbers that are stored in a variable or what needs to be printed
    def OUT(self, OUTWORD):
        if(OUTWORD in self.DESCRIPTOR): # If the word is a variable
            print(self.DESCRIPTOR[OUTWORD]) # Print it
            return self.DESCRIPTOR[OUTWORD] # return it
        else:
            OUTWORD = OUTWORD.strip('"') # If it is a string, remove the quotations around the word like professor's example
            print (OUTWORD) # Print it
            return OUTWORD # return it
    
    # This is the store function which will store the var name as the key in the dictionary to its value
    def STORE(self, VARIABLE, VALUE = None):
        if(VALUE in self.DESCRIPTOR):
            self.DESCRIPTOR[VARIABLE] = self.DESCRIPTOR[VALUE]

        elif(VALUE is not None): 
            self.DESCRIPTOR[VARIABLE] = VALUE # stores the value and var into Descriptor
        # This below will store the label name and the location in the Descriptor
        else:
            self.DESCRIPTOR[VARIABLE] = self.CURRENTLINE

    # This function handles all jumping, which is what the BRx's call when they need to jump or when JMP jumps.
    def GOTOLABELS(self, LABEL):
        if(LABEL in self.DESCRIPTOR): # If the label is already stored in the descriptor
            JUMPPOINT = self.DESCRIPTOR[LABEL] # jump to the lineNumber that was stored
            return JUMPPOINT
        else:
            # Loop through the input file
            with open('myVM_Prog.txt', 'r') as FILE:
            # Read the file line by line
                for LINE_NUMBER, LINE in enumerate(FILE, start=1):  
                    if LINE.strip().startswith(LABEL):  # If it finds the label, return the line number it is on so it knows where to jump to.
                        return LINE_NUMBER
                    
        # If the label is not found in the memory, print a message and return None
        print(f"Label '{LABEL}' not found")
        return None
    
    # This is the BRn function which returns true if the variable is less than 0, false otherwise
    def BRN(self, VARIABLE):
        if (VARIABLE in self.DESCRIPTOR and self.DESCRIPTOR[VARIABLE] < 0):
            return True
        else:
            return False
        
    # This is the BRz function which returns true if the variable is 0, false otherwise
    def BRZ(self, VARIABLE):
        if (VARIABLE in self.DESCRIPTOR and self.DESCRIPTOR[VARIABLE] == 0):
            return True
        else:
            return False
    
    # This is the BRp function which returns true if the variable is greater than 0, false otherwise
    def BRP(self, VARIABLE):
        if (VARIABLE in self.DESCRIPTOR and self.DESCRIPTOR[VARIABLE] > 0):
            return True
        else:
            return False
        
    # This is the BRzp function which returns true if the variable is 0 or positive, false otherwise
    def BRZP(self, VARIABLE):
        if (VARIABLE in self.DESCRIPTOR and self.DESCRIPTOR[VARIABLE] == 0 or self.DESCRIPTOR[VARIABLE] > 0):
            return True
        else:
            return False
    
    # This is the BRzn function which returns true if the variable is 0 or negative, false otherwise
    def BRZN(self, VARIABLE):
        if (VARIABLE in self.DESCRIPTOR and self.DESCRIPTOR[VARIABLE] < 0 or self.DESCRIPTOR[VARIABLE] == 0):
            return True
        else:
            return False
        
# Instance of the virtual machine
VM = VIRTUALMACHINE()

# Initialize the Sequence of Load -> Decode -> Execute
VM.LOADPHASE()