
from Location_Counter import get_format
from SICXE_Instructions import sicxe_instructions

registers_num = {
    "a":'0000', 
    "x":'0001',
    "l":'0010',
    "b":'0011', 
    "s":'0100', 
    "t":'0101', 
    "f":['0110', '0111'],
    "pc": '1000',
    "sw": '1001'
}


## !THIS GETS THE OPCODE
def get_opcode(instruction):
    clean_inst = instruction.lstrip('+')
    
    # Search all instruction formats
    for format_dict in sicxe_instructions.values():
        if clean_inst in format_dict:
            return format_dict[clean_inst]
    
    return None


# !THIS GETS THE SYMBOL TABLE AND UPDATES IT INTO A DICTIONARY
data_dict = {}
def update_symbol_table():

    with open("outputs/symbol_table.txt", "r") as file:
        for line in file:
            key, value = line.strip().split()
            data_dict[key] = value  # convert hex string to integer

    print(data_dict)

#! PASS 2
def Pass_2(input_array):
    
    update_symbol_table() ## so it updates the symbol table each time

    Object_Codes = []
    Modifaction_Records = []
    base_location = ""

    for line in input_array:
        
        ## gets the PC for format 3
        index_of_next = input_array.index(line) + 1 if line[1] != "END" else 0x0000
        PC = input_array[index_of_next][0]


       
        op = ''
        symbol = ''
        label = '' ## most like will not need this
        location = ''
       

        ## get the base for format 3
        if "BASE" in line: 
            base_location = line[2] ## cuz location + BASE + base_loc
            if base_location in data_dict:
                base_location = hex(int(data_dict[base_location], 16))
            # print(base_location)

        if len(line) == 2: ## Location + Instruction
            #? feh eh law galy msln 0x0034 TABLE RSUB?
            location = line[0]
            op = line[1]
        elif len(line) == 3: ## Location + Instruction + Symbol
            location, op, symbol = line
        elif len(line) == 4: ## Location + Label + Instruction + Symbol
            location, label, op, symbol = line
        else: 
            print("THERE IS SOMETHING FISHY GOING ON")


        opcode = get_opcode(op) ## returns opcode of the instruction so it can be usable
        format = get_format(op) ## this is the format of the line at hand

        # ModCode = ""
        # objectCode = ""
        
        if format == 1:
            objectCode = format1(opcode)
        elif format == 2:
            objectCode = format2(opcode, symbol)
        elif format == 3:
            objectCode = format3(PC, base_location, opcode, symbol)
        elif format == 4:
            objectCode, ModCode  = format4(location, opcode, symbol) 
            Modifaction_Records.append(ModCode)
        else:
            ## if format is None
            objectCode = memory_handling(line)
        
        Object_Codes.append(objectCode)
    
    return Object_Codes, Modifaction_Records


        
#! FORMATS

def format1(opcode):
    op = format(opcode, '08b')
    op = hex(int(op, 2))[2:].upper().zfill(len(op) // 4)
    print(op)
    return op



def format2(opcode, registers):
    ## this will return object code of a format 2
    # ?print(opcode)
    # ?print(registers.lower())
    opcode = format(opcode, '08b')
    ## X,S

    if(len(registers) == 3):
        first_register = registers_num[registers[0].lower()]
        second_register = registers_num[registers[2].lower()]
        object_code = opcode + first_register + second_register

        
    else:
        first_register = registers_num[registers[0].lower()]
        second_register = "0000"
    object_code = opcode + first_register + second_register

    
    print(hex(int(object_code, 2))[2:].upper().zfill(len(object_code) // 4))
    return hex(int(object_code, 2))[2:].upper().zfill(len(object_code) // 4)



def format3(PC, base, opcode, symbol):
    ## this will return object code of a format 3

    # symbol w/o "#" or "@"
    processed_symbol = symbol.replace('@', '').replace('#', '').replace(',x', '').replace(',X', '')
    
    op = format(opcode, '08b')[:-2]  # Get first 6 bits of opcode

    # flags
    n = '1' if not symbol.startswith('#') else '0'  # n=1 unless immediate 
    i = '1' if not symbol.startswith('@') else '0'  # i=1 unless indirect
    x = '1' if ',x' in symbol.lower() else '0'
    e = '0'  # Format 3 always has e=0
    b ='0'
    p ='0'

    # Handle displacement calculation
    if processed_symbol.isdigit():
        p = "0"
        b = "0"
        disp = int(processed_symbol)
    elif symbol == "":
        disp = 0  # Changed from string to integer
    else:
        TA = data_dict[processed_symbol]
        TA_int = int(TA, 16)
        PC_int = int(PC, 16)

        disp = TA_int - PC_int
        if -2048 <= disp <= 2047:
            p = "1"
            b = "0"
        else:
            base_int = int(base, 16)
            disp = TA_int - base_int
            if 0 <= disp <= 4095:
                p = "0"
                b = "1"
            else:
                raise ValueError(f"Displacement out of range for format 3: {disp}")

    # Ensure disp is integer and apply bitmask
    disp_int = int(disp)  # Convert to integer if not already
    disp_bin = format(disp_int & 0xFFF, "012b")  # Now works with integers

    ni = n + i
    xbpe = x + b + p + e
    final_bin = op + ni + xbpe + disp_bin
    final_hex = format(int(final_bin, 2), '06X')
    print(final_hex)
    return final_hex


#! FORMAT 4 --> returns object code and modification record
def format4(location, opcode, symbol):
    ## this will return object code of a format 4


    # symbol w/o "#" or "@"
    processed_symbol = symbol.replace('@', '').replace('#', '').replace(',x', '').replace(',X', '') 
    #? print("processed_symbol: "+ processed_symbol)
    ## 72 --> 48 --> 010010
    op = format(opcode, '08b')[:-2]
    # op = op[:-2]

    # flags
    n = '1' if not symbol.startswith('#') else '0'  # n=1 unless immediate 
    i = '1' if not symbol.startswith('@') else '0'  # i=1 unless indirect
    x = '1' if ',x' in symbol.lower() else '0'
    b = '0'  # Format 4 always uses absolute addressing
    p = '0'  # Format 4 doesn't use PC-relative
    e = '1'  # Format 4 always has e=1

    #? print("flags are: " + n + i + x + b + p + e)
    temp = op + n + i + x + b + p + e # 010010111001
    #? print(temp)
    

    ## turns the symbol into binary [20 bits]
    if symbol == "": ## e.g +RSUB
        disp = format(int("00000", 16), '020b') ## 20 bits of 0
    elif processed_symbol.isdigit():  # Immediate constant like #4096
        disp = format(int(processed_symbol), '020b') 
    else: 
        disp = format(int(data_dict[processed_symbol], 16), '020b')

    objectcode = temp + disp ## final object code --> 6 bits + 6 bits + 20 bits

    ## Make the modification record
    if processed_symbol.isdigit():
        mod_loc = ""
    else:
        mod_loc = f"{int(location, 16) + 1:06X}.05"

    #? print(mod_loc)
    #? print(objectcode)
    hex_string = hex(int(objectcode, 2))[2:].upper().zfill(len(objectcode) // 4)
    print(hex_string)


    return hex_string, mod_loc





def memory_handling(line):

    # print(line)
    if "RESW" in line or "RESB" in line:
        print("X")
        return "X"
    

    elif "END" in line or "START" in line or "BASE" in line:
        return '.'
    
    elif "WORD" in line:
        obj_code = int(line[-1])
        # print(obj_code)
        obj_code = f"{obj_code:06X}"
        # print("incoming word")
        print(obj_code)
        return obj_code

    elif "BYTE" in line:
        word = line[-1]
        if word[0] == 'C': #1char= 1 byte 
            word = word[2:-1]
            ans= ''.join(f"{ord(c):02X}" for c in word)
            print(ans)
            return ans

        elif word[0] == 'X':  #2Hex values = 1byte 
            word = word[2:-1]
            print(word)
            return word






