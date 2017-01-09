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
# this example assumes that a bucket named "books" and the following objects exist on the server (these are the same objects as are on the server if they are not deleted at the end of the bulk put example)
fileList = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

bucketContents = client.get_bucket(ds3.GetBucketRequest(bucketName))

objectList = ds3.FileObjectList(map(lambda obj: ds3.FileObject(obj['Key']), bucketContents.result['ContentsList']))
bulkGetResult = client.get_bulk_job_spectra_s3(ds3.GetBulkJobSpectraS3Request(bucketName, objectList))

# create a set of the chunk ids which will be used to track
# what chunks have not been retrieved
chunkIds = set(map(lambda x: x['ChunkId'], bulkGetResult.result['ObjectsList']))

# create a dictionary to map our retrieved objects to temporary files
# if you want to keep the retreived files on disk, this is not necessary
tempFiles={}

# while we still have chunks to retrieve
while len(chunkIds) > 0:
    # get a list of the available chunks that we can get
    availableChunks = client.get_job_chunks_ready_for_client_processing_spectra_s3(
                             ds3.GetJobChunksReadyForClientProcessingSpectraS3Request(bulkGetResult.result['JobId']))

    chunks = availableChunks.result['ObjectsList']

    # check to make sure we got some chunks, if we did not
    # sleep and retry.  This could mean that the cache is full
    if len(chunks) == 0:
        time.sleep(availableChunks.retryAfter)
        continue

    # for each chunk that is available, check to make sure
    # we have not gotten it, and if not, get that object
    for chunk in chunks:
        if not chunk['ChunkId'] in chunkIds:
            continue
        chunkIds.remove(chunk['ChunkId'])
        for obj in chunk['ObjectList']:
            # if we haven't create a temporary file for this object yet, create one
            if obj['Name'] not in tempFiles.keys():
                tempFiles[obj['Name']]=tempfile.mkstemp()
    
        # get the object
        objectStream = open(tempFiles[obj['Name']][1], "wb")
        client.get_object(ds3.GetObjectRequest(bucketName, 
                                               obj['Name'],
                                               objectStream,                                               
                                               offset = int(obj['Offset']), 
                                               job = bulkGetResult.result['JobId']))

# iterate over the temporary files, printing out their names, then closing and and removing them
for objName in tempFiles.keys():
    print(objName)
    os.close(tempFiles[objName][0])
    os.remove(tempFiles[objName][1])
