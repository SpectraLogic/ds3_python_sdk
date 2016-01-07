import os
import tempfile

from ds3 import ds3

client = ds3.createClientFromEnv()

# create a dictionary to map bucket names to object names
object_dict={}

# get a list of all the buckets on the server we have access to
bucketObjects = client.getService()
# the call to getService will return a list bucket objects, which have more information about the bucket, but in this case we only care about the name of the buckets
bucketNames = map(lambda bucket: bucket.name, bucketObjects)

# iterate over every bucket and get details about each of them
for bucketName in bucketNames:
    object_dict[bucketName]=[]
    bucketContents = client.getBucket(bucketName)

    # like getService, getBucket returns more information about the bucket than the contents, so we'll extract those
    objectNames = map(lambda bucket: bucket.name, bucketContents.objects)
    for name in objectNames:
    	object_dict[bucketName].append(name)

print(object_dict)
