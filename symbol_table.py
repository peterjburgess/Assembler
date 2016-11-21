class SymbolTable:

	def __init__(self):
		self.table = self.default_table

	default_table = {
			"SP": 0,
			"LCL": 1,
			"ARG": 2,
			"THIS": 3,
			"THAT": 4,
			"R0": 0,
			"R1": 1,
			"R2": 2,
			"R3": 3,
			"R4": 4,
			"R5": 5,
			"R6": 6,
			"R7": 7,
			"R8": 8,
			"R9": 9,
			"R10": 10,
			"R11": 11,
			"R12": 12,
			"R13": 13,
			"R14": 14,
			"R15": 15,
			"SCREEN": 16384,
			"KBD": 24576
			}

	def add_entry(self, symbol, address):
		"""Add dictionary entry to self.table with key=symbol and address=address"""

		self.table[symbol] = address

	def contains(self, symbol):
		"""Determine whether symbol exists in self.table"""

		if symbol in self.table:
			return True
		else:
			return False

	def get_address(self, symbol):
		"""Get the address of a given symbol"""

		return self.table[symbol]
