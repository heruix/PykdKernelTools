#! python3.7

from pykd import *
from common import *

process_name = None
break_addr = None


def callback():
	process_name = getCurrentProcessName()
	process_path = getCurrentProcessPath()

	print(name.lower())
	print(process_name)

	if name.lower() is process_name:
		return True

def run():
	global process_name
	global break_addr

	if getNtDll() is None:
		return

	break_addr_hex = int(break_addr, 16)
	setBp(break_addr_hex, callback)

	print("\nBreaking now will cancel the script.\n\
		Waiting for {0} to hit {1}...\n".format(process_name, break_addr))
	
	go()

	symbol = None
	try:
		symbol = findSymbol(break_addr_hex, True)
	except:
		pass

	print("\n{0} has hit {1} [0x{2}]\n".format(
		process_name, 
		symbol if symbol is not None else '???',
		break_addr))

def useage():
	print("\nAllows you to set a breakpoint that only gets triggered " \
		"when the process matches the given process name.")
	print("\nRequired Parameters:")
	print("\tprocess_name\tRequires a process name to be provided.")
	print("\tbreak_addr\t\tRequires a memory address which will be broken into.")

def options():
	global process_name
	global break_addr

	if len(sys.argv) != 3:
		return False

	try:
		process_name = sys.argv[1]
		break_addr = sys.argv[2]

		if isValidAddress(break_addr) is False:
			print("Invalid address '{0}'".format(break_addr))
			return False

	except:
		print("Failed to parse parameters.")
		return False

	return True

def init():
	if options():
		run()
	else:
		useage()

if __name__ == "__main__":
	init()