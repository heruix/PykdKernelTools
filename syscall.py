#! python3.7

from pykd import *
from common import *

syscall_number = 0

def run():
	print("\n{0}\n".format(findSymbol(getSyscallAddress(syscall_number), True)))

def options():
	global syscall_number

	if (len(sys.argv) is 2 and sys.argv[1] is '?') or \
		(len(sys.argv) > 3 or len(sys.argv) < 2):
		useage()
		return False

	if len(sys.argv) is 2:
		try:
			syscall_number = int(sys.argv[1], 16)
		except Exception as e:
			print("syscall number invalid.")
			return False
	else:
		syscall_number = reg("ax")

	return True

def useage():
	print("\nGives you the resulting kernel function called to by a syscall.")
	print("\nOptional Parameters:")
	print("\tA syscall number, otherwise, the value of the ax register will be used.")

def init():
	if options():
		run()

if __name__ == "__main__":
	init()