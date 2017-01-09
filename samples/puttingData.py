from ds3 import ds3
import os
import time
import sys

client = ds3.createClientFromEnv()

bucketName = "books"

# make sure the bucket that we will be sending objects to exists
client.put_bucket(ds3.PutBucketRequest(bucketName))

# create your list of objects that will be sent to DS3
# this example assumes that these files exist on the file system

fileList = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

# this method is used to get the size of the files
def getSize(fileName, prefix=""):
    size = os.stat(pathForResource(fileName)).st_size
    return ds3.FileObject(prefix + fileName, size)
    
# this method is used to get the os specific path for an object located in the resources folder
def pathForResource(resourceName):
    encoding = sys.getfilesystemencoding()
    currentPath = os.path.dirname(unicode(__file__, encoding))
    return os.path.join(currentPath, "resources", resourceName)

# get the sizes for each file
fileList = map(getSize, fileList)
fileObjectList = ds3.FileObjectList(fileList)

# submit the put bulk request to DS3
bulkResult = client.put_bulk_job_spectra_s3(ds3.PutBulkJobSpectraS3Request(bucketName, fileObjectList))

# the bulk request will split the files over several chunks if it needs to.
# we then need to ask what chunks we can send, and then send them making
# sure we don't resend the same chunks

# create a set of the chunk ids which will be used to track
# what chunks have not been sent
chunkIds = set(map(lambda x: x['ChunkId'], bulkResult.result['ObjectsList']))

# while we still have chunks to send
while len(chunkIds) > 0:
    # get a list of the available chunks that we can send
    availableChunks = client.get_job_chunks_ready_for_client_processing_spectra_s3(
                             ds3.GetJobChunksReadyForClientProcessingSpectraS3Request(bulkResult.result['JobId']))

    chunks = availableChunks.result['ObjectsList']

    # check to make sure we got some chunks, if we did not
    # sleep and retry.  This could mean that the cache is full
    if len(chunks) == 0:
        time.sleep(availableChunks.retryAfter)
        continue

    # for each chunk that is available, check to make sure
    # we have not sent it, and if not, send that object
    for chunk in chunks:
        if not chunk['ChunkId'] in chunkIds:
            continue
        
        chunkIds.remove(chunk['ChunkId'])
        for obj in chunk['ObjectList']:
            # it is possible that if we start resending a chunk, due to the program crashing, that 
            # some objects will already be in cache.  Check to make sure that they are not, and then
            # send the object to Spectra S3
            if obj['InCache'] == 'false':
                localFileName = "resources/" + obj['Name']
                objectDataStream = open(localFileName, "rb")
                client.put_object(ds3.PutObjectRequest(bucketName, 
                                                       obj['Name'], 
                                                       obj['Length'],
                                                       objectDataStream,
                                                       offset=int(obj['Offset']),
                                                       job=bulkResult.result['JobId']))

# we now verify that all our objects have been sent to DS3
bucketResponse = client.get_bucket(ds3.GetBucketRequest(bucketName))

for obj in bucketResponse.result['ContentsList']:
    print obj['Key']

# delete the bucket by first deleting all the objects, and then deleting the bucket
for obj in bucketResponse.result['ContentsList']:
    client.delete_object(ds3.DeleteObjectRequest(bucketName, obj['Key']))

client.delete_bucket(ds3.DeleteBucketRequest(bucketName))
