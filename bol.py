#! python3.7

import re
from pykd import *
from common import *

target_process_name = None
target_dll_name = None
output_all = None
 
exe_str = ".exe"

def callback():
	global target_process_name, target_dll_name, output_all

	process_name = getCurrentProcessName().lower()

	# The name of the image is stored in the eax/rax register (depending on CPU architecture)
	image_name = loadUnicodeString(reg("rcx") if is64bitSystem() else reg("ecx"))
	image_name = os.path.basename(image_name)
	
	process_match = process_name == target_process_name

	if output_all is True or process_match:
		print("[{0}] {1} loaded {2}".format(getCurrentPid(), process_name, image_name))

	if process_match and image_name == target_dll_name:
		return True

def run():
	image_notify_routine = None

	# Try and get the image notify virtual address.
	try:
		image_notify_routine = getNt().offset("PsCallImageNotifyRoutines")
	except Exception as e:
		print(e)
		return

	bp = setBp(image_notify_routine, callback)

	go()

def useage():
	print("Allows you to break into a process at the point that it loads an image.")
	print("\nRequired Parameters:")
	print("process_name\tSpecifies the process name to look for.")
	print("image_name\tSpecifies the image name to look for.")
	print("Optional Parameters:")
	print("-a\tOutput all image loads across the system.")

def options():
	global target_dll_name, target_process_name, output_all

	if len(sys.argv) == 2 and sys.argv[1] == '?':
		return False

	if len(sys.argv) < 3:
		return False

	try:
		target_process_name = sys.argv[1]
		target_dll_name = sys.argv[2]
		target_process_name = removeExeFromPath(target_process_name).lower()
	except Exception as e:
		print(e)
		return False

	try:
		for option in sys.argv:
			if option == '-a':
				output_all = True
	except Exception as e:
		print(e)

	return True

def init():
	if options():
		run()
	else:
		useage()

if __name__ == "__main__":
	init()