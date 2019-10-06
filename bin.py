#! python3

from pykd import *
from common import *

process_name = None
str_exe = ".exe"

def run():
	global process_name
	process_name = process_name.lower()

	# We need ntdll to enumerate the processes.
	if getNtDll() is None: return
	
	# Remove .exe from given process name.
	if process_name.endswith(str_exe):
		process_name = process_name.replace(str_exe, '')

	# Ensure the input doesn't end in 'exe'.
	current_process_name = getCurrentProcessName().lower().replace(str_exe, '')

	# Check if we're already in that process.
	if process_name == current_process_name:
		print("Current process is already {0}".format(getCurrentProcessName()))
		return

	eprocess = getProcessFromName(process_name)
	if eprocess is not None:
		# Issue the context switch command.
		dbgCommand(".process -i {0};g".format(hex(eprocess)))

		print("\nSwitched to {0} with PID {1}".format(
			process_name,
			int(typedVar(getNtDll().type("_EPROCESS"), eprocess).UniqueProcessId)))
	else:
		print("\nFailed to find process matching '{0}'".format(process_name))

def options():
	global process_name

	try:
		if len(sys.argv) == 2:
			if sys.argv[1] is '?':
				return False
			process_name = sys.argv[1]
			return True
	except: pass
	
	return False

def useage():
	print("\nAllows you to break into a process without having to use the .process command.")
	print("If there are multiple matches, this will just switch to the first process found to match.")
	print("\nRequired Arguments:")
	print("\tprocess_name\tRequires a process name be provided. No need to append exe.")

def init():
	if options():
		print()
		run()
		print()
	else:
		useage()

if __name__ == "__main__":
	init()