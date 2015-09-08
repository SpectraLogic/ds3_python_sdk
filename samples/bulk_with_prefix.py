from ds3 import ds3
import os

client = ds3.createClientFromEnv()

bucketName = "put_test_bucket"

client.putBucket(bucketName)

fileList = ["resources/beowulf.txt", "resources/sherlock_holmes.txt", "resources/tale_of_two_cities.txt", "resources/ulysses.txt"]

fileMap = {}

# this method is used to get the size of the files
def createDs3Obj(fileName):
    size = os.stat(fileName).st_size
    ds3ObjName = "prefix/" + fileName
    fileMap[ds3ObjName] = fileName
    return (ds3ObjName, size)

# get the sizes for each file
fileList = map(createDs3Obj, fileList)

# submit the put bulk request to DS3
bulkResult = client.putBulk(bucketName, fileList)

# the bulk request will split the files over several chunks if it needs to
# we need have to iterate over the chunks, ask the server for spacd to send
# the chunk, then send all the objects returned in the chunk
for chunk in bulkResult.chunks:
    allocateChunk = client.allocateChunk(chunk.chunkId)
    for obj in allocateChunk.chunk.objects:
        client.putObject(bucketName, obj.name, obj.offset, obj.length, bulkResult.jobId, fileMap[obj.name])

# we now verify that all our objects have been sent to DS3
bucketResponse = client.getBucket(bucketName)

for obj in bucketResponse.objects:
    print obj.name
