#! python3.7

from pykd import *
from common import *

registers = ['rcx', 'rdx', 'r8', 'r9']
stack_length = 20

def getRegValue(value):
	if isValid(value):
		return dbgCommand("db {0}".format(hex(value)))
	else:
		return hex(value)

def run():
	print()

	for register in registers:
		try:
			print("{0}\n{1}\n".format(
				register.upper(),
				getRegValue(reg(register))))
		except:
			print("Failed to dump register {0}.".format(register))

	try:
		print("STACK:")
		for offset in range(0, stack_length):
			address = reg("rsp") + offset * ptrSize()
			value = ptrPtr(address)
			type_ = 'PTR' if isValid(value) else 'VAL'
			
			print("{0}: [{1}] {2}".format(
				hex(address), 
				type_, 
				hex(value)))
	except:
		print("Failed to dump stack.")

	print()

def useage():
	print("\nDumps all prominent register values.\n")

def init():
	if is64bitSystem() == False:
		print("This is only an x64 script.")
		return
	run()

if __name__ == "__main__":
	init()