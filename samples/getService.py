from ds3 import ds3
import pdb

client = ds3.createClientFromEnv()

pdb.set_trace()
for bucket in client.getService():
    print bucket.name
