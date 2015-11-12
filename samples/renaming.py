import os
import tempfile

from ds3 import ds3

client = ds3.createClientFromEnv()


bucketName = "books"

# make sure the bucket that we will be sending objects to exists
client.putBucket(bucketName)

# create your list of objects that will be sent to DS3
# the key to the dictionary is the name the object will have on the server, and the values are the files to be transferred
# this example assumes that these files exist on the file system
fileListMapping = {
    "beowulf.txt":"resources/beowulf.txt",
    "sherlock_holmes.txt":"resources/sherlock_holmes.txt",
    "tale_of_two_cities.txt":"resources/tale_of_two_cities.txt",
    "ulysses.txt":"resources/ulysses.txt",
    "folder/beowulf.txt":"resources/beowulf.txt",
    "folder/sherlock_holmes.txt":"resources/sherlock_holmes.txt",
    "folder/folder2/tale_of_two_cities.txt":"resources/tale_of_two_cities.txt",
    "folder/folder2/ulysses.txt":"resources/ulysses.txt"
}

# this method is used to get the size of the files
# we need two parameters because the S3 API wants the name that the object will take on the server, but the size obviously needs to come from the file on the current file system
def getSize(fileName, realFileName):
    size = os.stat(realFileName).st_size
    return (fileName, size)

# get the sizes for each file
fileList = map(lambda key:getSize(key, fileListMapping[key]), fileListMapping.keys())

# submit the put bulk request to DS3
bulkResult = client.putBulk(bucketName, fileList)

# the bulk request will split the files over several chunks if it needs to.
# we then need to ask what chunks we can send, and then send them making
# sure we don't resend the same chunks

# create a set of the chunk ids which will be used to track
# what chunks have not been sent
chunkIds = set(map(lambda x: x.chunkId, bulkResult.chunks))

# while we still have chunks to send
while len(chunkIds) > 0:
    # get a list of the available chunks that we can send
    availableChunks = client.getAvailableChunks(bulkResult.jobId)

    chunks = availableChunks.bulkPlan.chunks

    # check to make sure we got some chunks, if we did not
    # sleep and retry.  This could mean that the cache is full
    if len(chunks) == 0:
        time.sleep(availableChunks.retryAfter)
        continue

    # for each chunk that is available, check to make sure
    # we have not sent it, and if not, send that object
    for chunk in chunks:
        if not chunk.chunkId in chunkIds:
            continue
        chunkIds.remove(chunk.chunkId)
        for obj in chunk.objects:
            # it is possible that if we start resending a chunk, due to the program crashing, that 
            # some objects will already be in cache.  Check to make sure that they are not, and then
            # send the object to Spectra S3
            if not obj.inCache:
                client.putObject(bucketName, obj.name, obj.offset, obj.length, bulkResult.jobId, realFileName = fileListMapping[obj.name])

# we now verify that all our objects have been sent to DS3
bucketResponse = client.getBucket(bucketName)

for obj in bucketResponse.objects:
    print obj.name

# objects on the server are arranged in a flat structure, but filepath-like names can be simulated using prefixes.
# deleteFolder will delete any object with "prefix/", in this case "folder/"

client.deleteFolder(bucketName, "folder/folder2")

print("\nAfter deletion number 1:")
bucketResponse = client.getBucket(bucketName)

for obj in bucketResponse.objects:
    print obj.name

client.deleteFolder(bucketName, "folder")

print("\nAfter deletion number 2:")
bucketResponse = client.getBucket(bucketName)

for obj in bucketResponse.objects:
    print obj.name

# delete everything else
for obj in bucketResponse.objects:
    client.deleteObject(bucketName, obj.name)

client.deleteBucket(bucketName)
