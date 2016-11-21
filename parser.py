class Parser:

	def __init__(self, input_file):
		self.input_file = input_file
		self.current_command = ""

	def has_more_commands(self):
		"""Check that we haven't reached the end of the file"""

		self.current_command = self.input_file.readline()
		if self.current_command:
			return True;
		else:
			return False;

	def advance(self):
		"""Remove all comments and whitespace"""
		self.current_command = self.remove_comments(self.current_command)
		self.current_command = self.remove_whitespace(self.current_command)

	def command_type(self):
		"""Return command type

		A_Command for @Xxx where Xxx is a symbol or decimal number
		C_Command for dest=comp;jump
		L_Command for Xxx where Xxx is a symbol
		"""

		if self.current_command[0] == '@':
			return 'A_Command'
		elif self.current_command[0] == '(':
			return 'L_Command'
		else:
			return 'C_Command'

	def symbol(self):
		"""Return symbol or decimal value of current A_Command or L_Command"""
		
		sym = self.current_command.split('@')[-1]
		if sym[0] == '(':
			sym = sym[1:-1]
		return sym

	def dest(self):
		"""Return dest Mnemonic of current C-Command"""

		if "=" in self.current_command:
			command_list = self.current_command.split("=")
			return command_list[0]
		else:
			return ""

	def comp(self):
		"""Return comp Mnemonic of current C-Command"""

		command_without_dest = self.current_command.split("=")[-1]
		comp_command = command_without_dest.split(";")[0]
		return comp_command

	def jump(self):
		"""Return Jump Mnemonic of current C-Command"""

		if ";" in self.current_command:
			command_list = self.current_command.split(";")
			return command_list[-1]
		else:
			return ""

	def remove_whitespace(self, string_to_parse):
		"""remove spaces and tabs"""

		string_list = string_to_parse.split()
		return "".join(string_list)

	def remove_comments(self, string_to_parse):
		"""Remove comments following //"""

		string_list = string_to_parse.split("//")
		return string_list[0]
