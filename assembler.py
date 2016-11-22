#Program to parse a .asm machine language file and produce a .hack binary translation
#Produced for Chapter 6 of the Nand2Tetris course
import parser
import symbol_table
import code
import sys

def main():
	#Get the filename supplied by command line argument
	#Rework to allow for multiple asm files to be processed at the same time
	file_name = sys.argv[1]

	#Check that the file provided is a .asm file. Raise exception if not
	extension = file_name.split('.')[-1]
	if extension != 'asm':
		raise ValueError("Wrong filetype. Supply a .asm file")

	sym_table = symbol_table.SymbolTable()

	pass1(file_name, sym_table)
	#Create a list of commands to be later exported to a .hack file
	command_list = pass2(file_name)
	write_to_hack_file(command_list, file_name)

def pass1(file_name, sym_table):
	with open(file_name, 'r') as asm_file:
		program_counter = 0

		#Go through file once, find the loops and store them in the symbol table
		for command in asm_file:
			current_command = parser.clean(command)
			#skip further processing if line made up of only spaces and/or comments
			if current_command:
				if parser.command_type(current_command) == 'L_Command':
					loop_symbol = parser.symbol(current_command)
					sym_table.add_entry(loop_symbol, program_counter)

				else:
					program_counter += 1

def pass2(file_name):
	#first address for symbol memory
	with open(file_name, 'r') as asm_file:
		address = 16
		command_list = []
		for command in asm_file:
			current_command = parser.clean(command)
			#skip further processing if line made up of only spaces and/or comments
			if current_command:
				if parser.command_type(current_command) == 'C_Command':
					dest = parser.dest(current_command)
					comp = parser.comp(current_command)
					jump = parser.jump(current_command)
					binary_repr = code.binary_code(dest, comp, jump)
					command_list.append(binary_repr)
				elif parser.command_type(current_command) == 'A_Command':
					symbol = parser.symbol(current_command)
					#if symbol doesn't begin with a numeric value, check symbol table for
					#correct value. Add new symbol if necessary
					try:
						int_symbol = int(symbol)
					except ValueError:
						if not sym_table.contains(symbol):
							sym_table.add_entry(symbol, address)
							address += 1

						symbol = sym_table.get_address(symbol)

					#convert decimal symbol to binary and add to command_list
					binary_symbol = "{0:016b}".format(int(symbol))
					command_list.append(binary_symbol)

	return command_list

def write_to_hack_file(command_list, file_name):
	#strip .asm and add .hack to the filename open .hack file for writing
	hack_file_name = file_name[:-4] + ".hack"

	with open(hack_file_name, 'w') as hack_file:

		#write binary codes into file.hack one line at a time
		for item in command_list:
			hack_file.write(item + '\n')
		
if __name__ == "__main__":
	main()
