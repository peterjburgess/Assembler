#Program to parse a .asm machine language file and produce a .hack binary translation
#Produced for Chapter 6 of the Nand2Tetris course
import parser
import symbol_table
import code
import sys

#Get the filename supplied by command line argument
#Rework to allow for multiple asm files to be processed at the same time
file_name = sys.argv[1]

#Check that the file provided is a .asm file. Raise exception if not
extension = file_name.split('.')[-1]
if extension != 'asm':
	raise ValueError("Wrong filetype. Supply a .asm file")

asm_file = open(file_name, 'r')
parse = parser.Parser(asm_file)
symbol_table = symbol_table.SymbolTable()
program_counter = 0

#Go through file once, find the loops and store them in the symbol table
while parse.has_more_commands():
	parse.advance()
	if parse.current_command:
		if parse.command_type() == 'L_Command':
			loop_symbol = parse.symbol()
			symbol_table.add_entry(loop_symbol, program_counter)

		else:
			program_counter += 1

asm_file.close()
asm_file = open(file_name, 'r')
parse = parser.Parser(asm_file)

#Create a list of commands to be later exported to a .hack file
command_list = []
#first address for symbol memory
address = 16
while parse.has_more_commands():
	parse.advance()
	if parse.current_command:
		if parse.command_type() == 'C_Command':
			dest = parse.dest()
			comp = parse.comp()
			jump = parse.jump()
			coder = code.Code(dest, comp, jump)
			binary_repr = coder.binary_repr_of_command()
			command_list.append(binary_repr)
		elif parse.command_type() == 'A_Command':
			symbol = parse.symbol()
			#if symbol doesn't begin with a numeric value, check symbol table for
			#correct value. Add new symbol if necessary
			try:
				int_symbol = int(symbol)
			except ValueError:
				if not symbol_table.contains(symbol):
					symbol_table.add_entry(symbol, address)
					address += 1

				symbol = symbol_table.get_address(symbol)

			#convert decimal symbol to binary and add to command_list
			binary_symbol = "{0:016b}".format(int(symbol))
			command_list.append(binary_symbol)

asm_file.close()
#strip .asm and add .hack to the filename open .hack file for writing
hack_file_name = file_name[:-4] + ".hack"
hack_file = open(hack_file_name, 'w')

#write binary codes into file.hack one line at a time
for item in command_list:
	hack_file.write(item + '\n')
	
hack_file.close()
