import os
import tempfile

from ds3 import ds3
from ds3 import libds3

client = ds3.createClientFromEnv()

bucket = "sdkexamples"
objname = "123456795.txt"
objlist = [1] 
objlist[0] = objname
objlist.append("beowulf.txt")
tapes = client.getPhysicalPlacement(bucket, objlist, False)

for tape in tapes.tapes:
    print(tape)
