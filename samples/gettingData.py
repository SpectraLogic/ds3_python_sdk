import os
import tempfile

from ds3 import ds3

client = ds3.createClientFromEnv()

bucketName = "books"
# this example assumes that a bucket named "books" and the following objects exist on the server (these are the same objects as are on the server if they are not deleted at the end of the bulk put example)
fileList = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

bucketContents = client.getBucket(bucketName)

bulkGetResult = client.getBulk(bucketName, map(lambda obj: obj.name, bucketContents.objects))

# create a set of the chunk ids which will be used to track
# what chunks have not been retrieved
chunkIds = set(map(lambda x: x.chunkId, bulkGetResult.chunks))

# create a dictionary to map our retrieved objects to temporary files
# if you want to keep the retreived files on disk, this is not necessary
tempFiles={}

# while we still have chunks to retrieve
while len(chunkIds) > 0:
    # get a list of the available chunks that we can get
    availableChunks = client.getAvailableChunks(bulkGetResult.jobId)

    chunks = availableChunks.bulkPlan.chunks

    # check to make sure we got some chunks, if we did not
    # sleep and retry.  This could mean that the cache is full
    if len(chunks) == 0:
        time.sleep(availableChunks.retryAfter)
        continue

    # for each chunk that is available, check to make sure
    # we have not gotten it, and if not, get that object
    for chunk in chunks:
        if not chunk.chunkId in chunkIds:
            continue
        chunkIds.remove(chunk.chunkId)
        for obj in chunk.objects:
            # if we haven't create a temporary file for this object yet, create one
            if obj.name not in tempFiles.keys():
                tempFiles[obj.name]=tempfile.mkstemp()
	    # get the object
	    client.getObject(bucketName, obj.name, obj.offset, bulkGetResult.jobId, realFileName=tempFiles[obj.name][1])

# iterate over the temporary files, printing out their names, then closing and and removing them
for objName in tempFiles.keys():
    print(objName)
    os.close(tempFiles[objName][0])
    os.remove(tempFiles[objName][1])
