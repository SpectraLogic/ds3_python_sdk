#   Copyright 2014-2016 Spectra Logic Corporation. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License"). You may not use
#   this file except in compliance with the License. A copy of the License is located at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   or in the "license" file accompanying this file.
#   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied. See the License for the
#   specific language governing permissions and limitations under the License.

import os
import tempfile

from ds3 import ds3

client = ds3.createClientFromEnv()


bucketName = "books"

# make sure the bucket that we will be sending objects to exists
client.put_bucket(ds3.PutBucketRequest(bucketName))

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
    return ds3.FileObject(fileName, size)

# get the sizes for each file
fileList = ds3.FileObjectList(map(lambda key:getSize(key, fileListMapping[key]), fileListMapping.keys()))

# submit the put bulk request to DS3
bulkResult = client.put_bulk_job_spectra_s3(ds3.PutBulkJobSpectraS3Request(bucketName, fileList))

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
            if not obj['InCache']:
                client.put_object(PutObjectRequest(bucketName, 
                                                   obj['Name'], 
                                                   obj['Offset'], 
                                                   obj['Length'], 
                                                   bulkResult.result['JobId'], 
                                                   real_file_name = fileListMapping[obj.name]))

# we now verify that all our objects have been sent to DS3
bucketResponse = client.get_bucket(ds3.GetBucketRequest(bucketName))

for obj in bucketResponse.result['ContentsList']:
    print obj['Key']

# objects on the server are arranged in a flat structure, but filepath-like names can be simulated using prefixes.
# deleteFolder will delete any object with "prefix/", in this case "folder/"

client.delete_folder_recursively_spectra_s3(ds3.DeleteFolderRecursivelySpectraS3Request(bucketName, "folder/folder2"))

print("\nAfter deletion number 1:")
bucketResponse = client.get_bucket(ds3.GetBucketRequest(bucketName))

for obj in bucketResponse.result['ContentsList']:
    print obj['Key']

client.delete_folder_recursively_spectra_s3(ds3.DeleteFolderRecursivelySpectraS3Request(bucketName, "folder"))

print("\nAfter deletion number 2:")
bucketResponse = client.get_bucket(ds3.GetBucketRequest(bucketName))

for obj in bucketResponse.result['ContentsList']:
    print obj['Key']

# delete everything else
for obj in bucketResponse.result['ContentsList']:
    client.delete_object(ds3.DeleteObjectRequest(bucketName, obj['Key']))

client.delete_bucket(ds3.DeleteBucketRequest(bucketName))
