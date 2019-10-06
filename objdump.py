#! python3

from pykd import *
import enum
from common import *
import traceback

class OBJ_TYPE(enum.Enum):
	# Documentation indicates that both NonPagedPool
	# and NonPagedPoolExecute are both 0.
	# Could be some legacy hold over.
	NonPagedPool = 0
	NonPagedPoolExecute = 0
	PagedPool = 1
	NonPagedPoolMustSucceed = 2
	DontUseThisType = 3
	NonPagedPoolCacheAligned = 4
	PagedPoolCacheAligned = 5
	NonPagedPoolCacheAlignedMustS = 6
	MaxPoolType = 7
	NonPagedPoolBase = 0
	NonPagedPoolBaseMustSucceed = 2
	NonPagedPoolBaseCacheAligned = 4
	NonPagedPoolBaseCacheAlignedMustS = 6
	NonPagedPoolSession = 32
	PagedPoolSession = 33
	NonPagedPoolMustSucceedSession = 34
	DontUseThisTypeSession = 35
	NonPagedPoolCacheAlignedSession = 36
	PagedPoolCacheAlignedSession = 37
	NonPagedPoolCacheAlignedMustSSession = 38
	NonPagedPoolNx = 512
	NonPagedPoolNxCacheAligned = 516
	NonPagedPoolSessionNx = 544

class Object(): 
	def __init__(self, raw_object, index):
		self.parse(raw_object, index)

	def parse(self, raw_object, index):
		try:
			self.index = index
			self.name = loadUnicodeString(raw_object.Name)
			self.total_number = ptrByte(raw_object.TotalNumberOfObjects.getAddress())
			self.high_water_objects = ptrByte(raw_object.HighWaterNumberOfObjects.getAddress())
			self.total_handles = ptrByte(raw_object.TotalNumberOfHandles.getAddress())
			self.high_water_handles = ptrByte(raw_object.HighWaterNumberOfHandles.getAddress())
			# Work around for getting the enum key as a string. 
			# There's probably a better way.
			self.pooltype = str(OBJ_TYPE(raw_object.TypeInfo.PoolType)).split(".")[1]
			self.allocation_tag = loadChars(raw_object.Key.getAddress(), 4)
		except Exception as e:
			print("Failed to parse object.")
			print(e)

	def __str__(self):
		output = ""
		output += "\n----------------------------------------\n\n"
		output += "Object Name:\t{0}\n".format(self.name)
		output += "Object Index:\t{0}\n".format(self.index)
		output += "Object Count:\t{0}\n".format(self.total_number)
		output += "Object Highest:\t{0}\n".format(self.high_water_objects)
		output += "Handle Count:\t{0}\n".format(self.total_handles)
		output += "Handle Highest:\t{0}\n".format(self.high_water_handles)
		output += "Pool Type:\t\t{0}\n".format(self.pooltype)
		output += "Alloc Tag:\t\t{0}".format(self.allocation_tag)
		return output


def getObjectType(object_table_addr, object_index):
	return ptrPtr(object_table_addr + (object_index * ptrSize()))

def getObjectTableAddr():
	objtable_addr = None
	nt = getNt()
	if nt:
		objtable_addr = nt.ObTypeIndexTable
	return objtable_addr

def dumpObjectTable(object_table_addr):
	if object_table_addr is None:
		print("Invalid object table address.")
		return 

	# ObTypeIndexTable points to a blank address.
	# Actual objects start two pointer sizes after the base address.
	object_table_addr_offset = object_table_addr + ptrSize() * 2

	object_count = 0

	try:
		object_type = getNt().type("_OBJECT_TYPE")

		while getObjectType(object_table_addr_offset, object_count) != 0x0:
			raw_object = typedVar(object_type, getObjectType(object_table_addr_offset, object_count))
			print(Object(raw_object, object_count))
			object_count += 1

	except Exception as e:
		print("Failed to fully dump the object table.")
		print(e)

	print("\n----------------------------------------\n")
	print("Found {0} objects in the object table [{1}]\n\n".format(object_count, hex(object_table_addr)))

def run():
	objtable_addr = getObjectTableAddr()
	if objtable_addr is not None:
		dumpObjectTable(objtable_addr)

def options():
	if len(sys.argv) == 2 
		if sys.argv[1] == '?':
			useage()
			return False
	return True

def useage():
	print("Prints all objects contained in the object table, along with the object statistics,"\
		"including how many objects are currently in use across the machine.\n")

def init():
	try:
		if options():
			run()
	except Exception as e: 
		print("Exception: %s" % e)
		print(traceback.format_exc())

if __name__ == "__main__":
    init()
