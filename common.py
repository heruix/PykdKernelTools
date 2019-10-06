#! python3
from pykd import *

nt = None
ntdll = None

def getNt():
	global nt
	if nt is not None:
		return nt

	try: # Could fail if the symbols for nt haven't been loaded yet.
		nt = module("nt")
	except:
		print("Failed to find symbols for the kernel (ntkrnlmp).")
		print("Try doing '.reload'.")
	return nt

def getNtDll():
	global ntdll
	if ntdll is not None:
		return ntdll

	try: # Could fail if the symbols for ntdll haven't been loaded yet.
		ntdll = module("ntdll")
	except:
		print("Failed to find symbols for the kernel (ntkrnlmp).")
		print("Try doing '.reload'.")
	return ntdll

def isValidAddress(addr):
	try:
		if isValid(int(addr, 16)) is True:
			return True
	except:
		pass
	return False


def formatFlags(valueList):
	# The layout that the flag converted bitmask will come
	# through as after being converted to a string is
	# FLAG_NAME.FlagValue1|FlagValue2
	# Here there are two values seperated by a pipe and
	# starting with the name of the enum.flag.

	output = ""
	try:
		# Remove the enum.flag name and split each value.
		list_ = str(valueList).rsplit('.')[1].rsplit('|')
		
		# Join the values back together with a comma.
		output = ', '.join(list_)
	except Exception as e:
		print(e)
		
	return output
	