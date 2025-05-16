Introduction

This project implements a two-pass assembler for the SIC/XE architecture. It takes a SIC/XE assembly
program and generates the corresponding object code in the HTME format, as well as intermediate
and symbol table files. The assembler is written entirely in Python and utilizes only built-in libraries.

How to Use the Program

To run the assembler, execute the following command in the terminal:
python3 File.py
or
python File.py
You will be prompted to enter the filename of the input SIC/XE assembly code. This file should
be placed in the files directory.
The assembler’s outputs, including the HTME object code and symbol table, will be saved in the
output directory.
