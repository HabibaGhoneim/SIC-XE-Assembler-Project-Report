from Location_Counter import Location_Counter
from Pass2 import Pass_2
import re
from HTME import HTME


Sentences = []
file_name = input("Enter the file name: ")
with open("files/" + file_name , 'r',  encoding='latin-1') as file:
    for line in file:
        lines = line.strip()
        array = lines.split()
        Sentences.append(array)


## Remove the lines, check if there are even lines or not.
def remove_lines(Sentences):
    for tokens in Sentences:
        if tokens and re.fullmatch(r"-?\d+\.?|0*\d+", tokens[0]):  # Matches numbers like "41.", "0092", or "-123"
            tokens.pop(0)
remove_lines(Sentences)




## ? What if it is ".Comment"
## remove the Comments [Habiba]
def remove_comments(Sentences):
    for tokens in Sentences:    # If there are more than 3 fields
        if len(tokens) > 3:
            del tokens[3:]
    for tokens in Sentences:
        for i, token in enumerate(tokens):
            if token.startswith(".") and (token == "." or token[1:].isalpha()):  # Matches ".comment" or ". comment"
                del tokens[i:]
                break
    Sentences[:] = [t for t in Sentences if t]  # Remove any empty lists
remove_comments(Sentences)



## Generate an intermediate File
with open("outputs/Intermediate.txt", "w") as intermediate:
    for list in Sentences:
        sentence = ' '.join(list)
        intermediate.write(sentence + "\n")




## Pass 1: Location Counter and Symbol Table


## Initializing the array
Int_Array = []
with open("outputs/Intermediate.txt", 'r') as file:
    for line in file:
        lines = line.strip()
        array = lines.split()
        Int_Array.append(array)

## Call the location counter function
Locations = Location_Counter(Int_Array)


## insert the locations that we got from Locations

for i in range(0, len(Locations)):
    if i < len(Int_Array):
        Int_Array[i].insert(0, Locations[i])



## !GENERATES OUT_PASS1.TXT 

with open("outputs/out_pass1.txt", "w") as file:
    for line in Int_Array:
        sentence = ' '.join(line)
        file.write(sentence + "\n")


## !GENERATES SYMBOL_TABLE.TXT


symbol_table = {}
for entry in Int_Array:
    if len(entry) == 4:
        loc, label = entry[0], entry[1]
        symbol_table[label] = loc

with open("outputs/symbol_table.txt", "w") as file:
    for label in sorted(symbol_table):
        address = symbol_table[label]
        file.write(f"{label} {address}\n")







##! Pass 2: Object code and HTME Records

Object_Codes, Modification_Records = Pass_2(Int_Array)

# generate the pass2 file

Pass2_Array = []
for i in range(0, len(Int_Array)):
    if i < len(Object_Codes):
        # Keep the original Int_Array intact
        temp_line = Int_Array[i][:]  # Create a copy of the current line
        temp_line.append(Object_Codes[i])

        # Remove "X" and "." from the copy only
        if Object_Codes[i] == "X" or Object_Codes[i] == ".":
            temp_line.pop()  # Remove the last element (Object_Codes[i])

        Pass2_Array.append(temp_line)

# !GENERATES OUT_PASS2.TXT
with open("outputs/out_pass2.txt", "w") as file:
    for line in Pass2_Array:
        sentence = ' '.join(line)
        file.write(sentence + "\n")


HTME(Int_Array, Locations,Object_Codes, Modification_Records)
print("HTME file generated successfully.")
