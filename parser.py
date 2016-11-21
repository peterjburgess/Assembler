def clean(current_command):
	"""Remove all comments and whitespace"""
	current_command = remove_comments(current_command)
	current_command = remove_whitespace(current_command)
	return current_command

def command_type(current_command):
	"""Return command type

	A_Command for @Xxx where Xxx is a symbol or decimal number
	C_Command for dest=comp;jump
	L_Command for Xxx where Xxx is a symbol
	"""

	if current_command[0] == '@':
		return 'A_Command'
	elif current_command[0] == '(':
		return 'L_Command'
	else:
		return 'C_Command'

def symbol(current_command):
	"""Return symbol or decimal value of current A_Command or L_Command"""
	
	#will return everything after the @ for an A_command
	sym = current_command.split('@')[-1]
	#if an L_Command, will return what's inside the parenthises
	if sym[0] == '(':
		sym = sym[1:-1]
	return sym

def dest(current_command):
	"""Return dest Mnemonic of current C-Command"""

	if "=" in current_command:
		#split string at = and return everything before the = (if = in string)
		command_list = current_command.split("=")
		return command_list[0]
	else:
		return ""

def comp(current_command):
	"""Return comp Mnemonic of current C-Command"""

	#remove the dest part of command if exists (part before =)
	command_without_dest = current_command.split("=")[-1]
	#remove jump part of command if exists (part after ;)
	comp_command = command_without_dest.split(";")[0]
	return comp_command

def jump(current_command):
	"""Return Jump Mnemonic of current C-Command"""

	#jump exists after ; if ; in string. Always the last part of the command
	if ";" in current_command:
		command_list = current_command.split(";")
		return command_list[-1]
	else:
		return ""

def remove_whitespace(string_to_parse):
	"""remove spaces and tabs"""

	string_list = string_to_parse.split()
	return "".join(string_list)

def remove_comments(string_to_parse):
	"""Remove comments following //"""

	string_list = string_to_parse.split("//")
	return string_list[0]
