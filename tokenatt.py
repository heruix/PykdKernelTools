#! python3

from pykd import *
from common import *
import traceback
from enum import Flag

token_addr = None
token_attributes = None

VALUE_TYPE = {
	0x0001:"INT64",
	0x0002:"UINT64",
	0x0003:"STRING",
	0x0004:"FQBN",
	0x0005:"SID",
	0x0006:"BOOLEAN",
	0x0010:"OCTET_STRING"
}

class VALUE_FLAG(Flag): 
	NON_INHERITABLE	= 0x0001
	VALUE_CASE_SENSITIVE = 0x0002
	USE_FOR_DENY_ONLY = 0x0004
	DISABLED_BY_DEFAULT	= 0x0008
	DISABLED = 0x0010
	MANDATORY = 0x0020

class SecurityAttribute():
	counter = 0

	def __init__(self, raw_security_attribute):
		self.parse(raw_security_attribute)

	def parse(self, raw_security_attribute):
		self.count = SecurityAttribute.counter
		self.name = loadUnicodeString(raw_security_attribute.name)
		self.type_ = VALUE_TYPE[int(raw_security_attribute.type_)]
		self.reserved = hex(raw_security_attribute.reserved)
		test = VALUE_FLAG(0x00003)
		formatFlags(test)
		
		self.flags = formatFlags(VALUE_FLAG(raw_security_attribute.flags))
		self.values = []
		for value_item in typedVarList(raw_security_attribute.values, "nt!_LIST_ENTRY", "Flink"):
			offset = 5 if is64bitSystem() else 6
			if int(raw_security_attribute.type_) == 1 or int(raw_security_attribute.type_) == 2:
				self.values.append(hex(ptrPtr(value_item + ptrSize() * offset)))
			if int(raw_security_attribute.type_) == 3:
				self.values.append(loadUnicodeString(value_item + ptrSize() * offset))

	def __str__(self):
		output = "\n"
		output += "[{0}]".format(self.count)
		output += " '{0}'".format(self.name)
		output += "\n\tType:\t\t{0}".format(self.type_)
		output += "\n\tReserved:\t{0}".format(self.reserved)
		output += "\n\tFlags:\t\t{0}".format(self.flags)
		output += "\n\tCount:\t\t{0}".format(len(self.values))
		output += "\n\tValues:\t\t["
		for value in self.values:
			output += str(value) + ", "
		output = output[:-2] + "]\n\n"
		return output

def initTokenAttributeStruct():
	global token_attributes

	alignment = 8 if is64bitSystem() else 4

	# The token attributes structure is aligned differently depending on
	# CPU architecture (x86 / x64).
	# Relying on pykd's createStruct() here to properly layout structure,
	# otherwise you get into all sorts of process architecture difference
	# issues.
	token_attributes = createStruct(name="token_attributes", align=alignment)
	token_attributes.append("name", getNtDll().type("_UNICODE_STRING"))
	token_attributes.append("type_", baseTypes.UInt4B)
	token_attributes.append("reserved", baseTypes.UInt4B)
	token_attributes.append("flags", baseTypes.UInt4B)
	token_attributes.append("value_count", baseTypes.UInt4B)
	token_attributes.append("emptyptr", baseTypes.UInt4B)
	token_attributes.append("values", getNtDll().type("_LIST_ENTRY"))

def getCurrProcTokenAddress():
	try:
		eprocess = typedVar(getNtDll().type("_EPROCESS"), getCurrentProcess())
		token_base_addr = typedVar(getNtDll().type("_EX_FAST_REF"), eprocess.Token)

		# The actual token address has nothing to do with the least
		# significant bit, so just mask that off.
		# Again, the amount to mask is processor architecture dependant.
		return token_base_addr.Object & (0xfffffffffffffff0 if is64bitSystem() else 0xfffffffffffffff8)
	except:
		print("Failed to get current process' token address.")
		print("Please supply token address.")
	return False

def parseRawSecurityAttributes(security_attributes):
	secatt_list = []
	for attribute in security_attributes:
		# The bit we want is four pointer sizes away
		# from the base security attribute address.
		offset = attribute + ptrSize() * 4
		secatt_list.append(typedVar(token_attributes, offset))
	return [SecurityAttribute(security_attribute) for security_attribute in secatt_list]

def getRawSecurityAttributes(token):
	raw_security_attributes = typedVar(getNt().type("_AUTHZBASEP_SECURITY_ATTRIBUTES_INFORMATION"), token.pSecurityAttributes)
	raw_security_attribute_list = typedVarList( \
			raw_security_attributes.SecurityAttributesList, \
			getNtDll().type("_LIST_ENTRY"), \
			"Flink")
	return raw_security_attributes, raw_security_attribute_list

def printSecurityAttributes(token_addr, security_attributes):
	raw_security_attributes = getRawSecurityAttributes(getTokenObject(token_addr))[0]
	try:
		print("\nProcess Token Address:      {0}".format(hex(token_addr)))
		print("Security Attribute List:    {0}".format(hex(ptrPtr(raw_security_attributes.SecurityAttributesList))))
		print("Security Attribute Count:   {0}".format(int(raw_security_attributes.SecurityAttributeCount)))
		print(*security_attributes)
	except:
		print("Failed to print security attributes.")

def getTokenObject(token_addr):
	return typedVar(getNt().type("_TOKEN"), token_addr)

def getSecurityAttributes(token_addr):
	return parseRawSecurityAttributes(getRawSecurityAttributes(getTokenObject(token_addr))[1])

def run():
	global token_addr

	try:
		token_addr = getCurrProcTokenAddress() if token_addr is None else False
		if token_addr is None: return
	
		# Create the token attribute structure at runtime 
		# due to differences in processor architecture.
		initTokenAttributeStruct()
		printSecurityAttributes(token_addr, getSecurityAttributes(token_addr))
	except:
		print("Failed to retrieve token attributes.")

def options():
	try:
		if len(sys.argv) == 1: 
			return True

		if len(sys.argv) == 2: 
		
			if sys.argv[1] == '?':
				return False
	
			if isValidAddress(sys.argv[1]):
				global token_addr
				token_addr = int(sys.argv[1], 16)
				return True
	except: pass
	return False

def useage():
	print("\nPrints the token attributes that are currently " \
		"missing from the !token command.\n")

	print("Optional Arguments:")
	print("\ttoken_address\tAllows a token address to be supplied.\n \
		\t\t\tIf none is supplied, the current process' access token will be used.\n")

def init():
	try:
		if options():
			run()
		else:
			useage()
	except Exception as e: 
		print("Exception: %s" % e)
		print(traceback.format_exc())

if __name__ == "__main__":
	init()
