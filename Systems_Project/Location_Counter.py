import SICXE_Instructions 

def extended_hex(hex_value):
    return f"0x{int(hex_value, 16):04X}"
## this gets the format number of the operations



def get_format(op):
    op_base = op.lstrip('+')
    for fmt_key, instr_dict in SICXE_Instructions.sicxe_instructions.items():

        if op_base in instr_dict:
            format_number = 4 if fmt_key == "Format 3/4" and op.startswith('+') else (
                3 if fmt_key == "Format 3/4" else int(fmt_key[-1])
            )
            return format_number
    
    return None

def calc_memory(op, operand):
    op = op.upper()
    if op == "WORD":
        return 3
    elif op == "RESW":
        return 3 * int(operand)
    elif op == "RESB":
        return int(operand)
    elif op == "BYTE":
        if operand.startswith("C'"):
            return len(operand[2:-1])
        elif operand.startswith("X'"):
            return (len(operand[2:-1]) + 1) // 2 # +1 if odd number 
    return 0

def Location_Counter(Int_Array):
    
    starting_address = hex(int(Int_Array[0][-1], 16))  # Ensure it's an integer before hex conversion
    Locations = [starting_address]
    LOCCTR = int(starting_address, 16)
    # print(starting_address)

    for instruction in Int_Array:
        op_index = 0
        if len(instruction) > 3:
            print("there is something fishy about this code.")
            break


        if len(instruction) == 3:
            ## then this has a symbol definition
            op_index = 1


        op = instruction[op_index].upper()
        operand = instruction[op_index + 1] if len(instruction) > op_index + 1 else None ## incase of RSUB or smth
        instr_format = get_format(op)

        if instr_format:
            LOCCTR += instr_format
        elif op in ["WORD", "RESW", "RESB", "BYTE"]:
            LOCCTR += calc_memory(op, operand)
        elif op == "START":
            LOCCTR = int(operand, 16)
        else:
            print(f"Unknown operation: {op}")



        LOCCTR_hex = hex(LOCCTR)  # Convert back to hexadecimal after calculation
        Locations.append(extended_hex(LOCCTR_hex))  # Append the formatted hex

    return Locations
    