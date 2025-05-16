


def HTME(Int_Array, Locations, Object_Code ,Modification_Records):

    start_loc = Locations[0] 
    end_loc   = Locations[-1]  

    #removed 0x
    start_addr = start_loc[2:].zfill(6)
    end_addr   = end_loc[2:].zfill(6)

    #H
    first = Int_Array[0]
    prog_name  = first[1][:6]
    start_addr = first[0][2:].zfill(6)

    #prog size
    prog_len   = int(end_addr, 16) - int(start_addr, 16)
    prog_len_hex = f"{prog_len:06X}"


    T_Record = T_records(Locations, Object_Code)

    with open("outputs/HTME.txt", "w") as f:

        f.write(f"H{prog_name}{start_addr}{prog_len_hex}\n")

        for t in T_Record:
            f.write(f"{t}\n")

        for m in Modification_Records:
            if m:
                f.write(f"M{m}\n")
        # E
        f.write(f"E{start_addr}\n")





def T_records(Locations, Object_Codes):

    ## TODO: Map each object code to its location
    Mapped_Object_Codes = {}
    for i in range(0, len(Object_Codes)):
        if i < len(Locations):
            Mapped_Object_Codes[Locations[i]] = Object_Codes[i]


    current_length = 0
    T_records = []
    current_record_codes = ""
    start_address = ""

    for location, code in Mapped_Object_Codes.items():


        if code == ".":
            continue  # Skip START, BASE, and END records

        if code == "X":  # Skip RESW/RESB or uninitialized memory
            if current_record_codes:
                length_hex = f"{current_length:02X}"
                start_address = start_address[2:].zfill(6)
                record = f"T{start_address}^{length_hex}{current_record_codes}"
                T_records.append(record)
                current_record_codes = ""
                current_length = 0
            continue

        if current_length == 0:
            start_address = location
            start_address = start_address[2:].zfill(6)
            current_record_codes = "^" +  code
            current_length = len(code) // 2
        elif current_length + len(code) // 2 <= 30:
            current_record_codes += "^" +  code
            current_length += len(code) // 2
        else:
            length_hex = f"{current_length:02X}"
            record = f"T{start_address}^{length_hex}{current_record_codes}"
            T_records.append(record)

            # Start new record
            start_address = location
            start_address = start_address[2:].zfill(6)
            current_record_codes = "^" +  code
            current_length = len(code) // 2

    # Final record
    if current_record_codes:
        length_hex = f"{current_length:02X}"
        record = f"T{start_address}^{length_hex}{current_record_codes}"
        T_records.append(record)


    return T_records

