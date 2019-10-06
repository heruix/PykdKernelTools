#! python3
from pykd import *
import os

nt = None
ntdll = None

def getNt():
	global nt
	if nt is not None:
		return nt

	try: # Could fail if the symbols for nt haven't been loaded yet.
		nt = module("nt")
	except:
		print("\nFailed to find symbols for the kernel (ntkrnlmp).")
		print("Try doing '.reload'.\n")
	return nt

def getNtDll():
	global ntdll
	if ntdll is not None:
		return ntdll

	try: # Could fail if the symbols for ntdll haven't been loaded yet.
		ntdll = module("ntdll")
	except:
		print("\nFailed to find symbols for ntdll.")
		print("Try doing '.reload'.\n")
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
	
def getCurrentProcessName():
	path = getProcessName(getCurrentProcess())
	if path is None:
		return None
	return os.path.basename(path)

def getAllActiveProcessAddresses():
	eprocess_type = getNtDll().type("_EPROCESS")
	eprocess = typedVar(eprocess_type, getCurrentProcess())
	process_list_offset = eprocess.fieldOffset("ActiveProcessLinks")
	
	activeprocesslinks = typedVarList(eprocess.ActiveProcessLinks, "nt!_LIST_ENTRY", "Flink")
	
	return [process - process_list_offset for process in activeprocesslinks]

def getProcessFromName(name):
	for eprocess in getAllActiveProcessAddresses():
		process_name = getProcessName(eprocess)

		if process_name == None:
			continue

		if process_name.replace('.exe', '').lower() == name.lower():
			return eprocess
	return None

def getProcessName(process_addr):
	path = getProcessPathFromProcess(process_addr)
	if path == None:
		return path
	return os.path.basename(path)

def getProcessPathFromProcess(process_addr):
	try:
		eprocess = typedVar(getNtDll().type("_EPROCESS"), process_addr)

		# Some processes, like SYSTEM, don't have an ImageFilePointer.
		# Make sure this isn't one of them.
		if int(eprocess.ImageFilePointer) is 0:
			return getImageFileName(eprocess)
		else:
			return getImageFilePointer(eprocess)

	except: pass
	return None

def getImageFileName(eprocess):
	try:
		# Fallback on pulling the ImageFileName, which has a max of 15 chars.
		processName = loadChars(eprocess.ImageFileName, 15)
		return ''.join([char if ord(char) != 0 else '' for char in processName])
	except: pass
	return None
	
def getImageFilePointer(eprocess):
	try:
		imagefile = typedVar(getNtDll().type("_FILE_OBJECT"), eprocess.ImageFilePointer)

		if eprocess.ImageFilePointer.getAddress() != 0:
			unicode_filename = typedVar(getNtDll().type("_UNICODE_STRING"), 
				imagefile.FileName)
			return loadUnicodeString(unicode_filename)
	except: pass
	return None