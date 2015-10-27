Spectra S3 Python SDK
--------------

An SDK conforming to the Spectra S3 [specification](https://developer.spectralogic.com/doc/ds3api/1.2/wwhelp/wwhimpl/js/html/wwhelp.htm).

Contact Us
----------

Join us at our [Google Groups](https://groups.google.com/d/forum/spectralogicds3-sdks) forum to ask questions, or see frequently asked questions.

Installing
----------

Follow the instructions for installing the [ds3_c_sdk](https://github.com/SpectraLogic/ds3_c_sdk) first.  The ds3_python_sdk uses the ds3_c_sdk to communicate with a Spectra S3 endpoint, and will not function without it.

To install the ds3_python_sdk, either clone the latest code, or download a release bundle from [Releases](http://github.com/SpectraLogic/ds3_python_sdk/releases).  Once the code has been download, cd into the bundle, and install it with `sudo python setup.py install`

Once `setup.py` completes the ds3_python_sdk should be installed and available to be imported into python scripts.

Documentation
-------------
The documentation for the SDK can be found at [http://spectralogic.github.io/ds3_python_sdk/sphinx/v1.0-0/](http://spectralogic.github.io/ds3_python_sdk/sphinx/v1.0-0/)

SDK
---

The SDK provides an interface for a user to add Spectra S3 functionality to their existing or new python application.  In order to take advantage of the SDK you need to import the `ds3` python package and module.  The following is an example that creates a Spectra S3 client from environment variables, creates a bucket, and lists all the buckets that are visible to the user.

```python

from ds3 import ds3

client = ds3.createClientFromEnv()

client.putBucket("testBucket")

for bucket in client.getService():
        print bucket.name
```

Ds3Client
---------
In the ds3_python_sdk there are two ways that you can create a `Ds3Client` instance: environment variables, or manually.  `ds3.createClientFromEnv` will create a `Ds3Client` using the following environment variables:

* `DS3_ENDPOINT` - The URL to the DS3 Endpoint
* `DS3_ACCESS_KEY` - The DS3 access key
* `DS3_SECRET_KEY` - The DS3 secret key
* `http_proxy` - If set, the `Ds3Client` instance will proxy through this URL

The `Ds3Client` instance can also be created manually in code with:

```python

from ds3 import ds3

client = ds3.Ds3Client("endpoint", ds3.Credentials("access_key", "secret_key"))

```

The proxy URL can be passed in as the named parameter `proxy` to `Ds3Client()`.

Putting Data
------------

To put data to a Spectra S3 appliance you have to do it inside of the context of what is called a Bulk Job.  Bulk Jobs allow the Spectra S3 appliance to plan how data should land to cache, and subsequently get written/read to/from tape.  The basic flow of every job is:

* Generate the list of objects that will either be sent to or retrieved from Spectra S3
* Send a bulk put/get to Spectra S3 to plan the job
* The job will be split into multiple chunks.  An application must then get the available list of chunks that can be processed
* For each chunk that can be processed, sent the object (this step can be done in parallel)
* Repeat getting the list of available chunks until all chunks have been processed

Here is an example of the above using the Python SDK for putting data:

```python

from ds3 import ds3
import os
import time

client = ds3.createClientFromEnv()

bucketName = "books"

# make sure the bucket that we will be sending objects to exists
client.putBucket(bucketName)

# create your list of objects that will be sent to DS3
# this example assumes that these files exist on the file system

fileList = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

# this method is used to get the size of the files
def getSize(fileName):
    size = os.stat(fileName).st_size
    return (fileName, size)

# get the sizes for each file
fileList = map(getSize, fileList)

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
                client.putObject(bucketName, obj.name, obj.offset, obj.length, bulkResult.jobId)

# we now verify that all our objects have been sent to DS3
bucketResponse = client.getBucket(bucketName)

for obj in bucketResponse.objects:
    print obj.name

# delete the bucket by first deleting all the objects, and then deleting the bucket
for obj in bucketResponse.objects:
    client.deleteObject(bucketName, obj.name)

client.deleteBucket(bucketName)

```

Here is an example of getting data with the Python SDK:

```python
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
            # it is possible that if we start resending a chunk, due to the program crashing, that 
            # some objects will already be in cache.  Check to make sure that they are not, and then
            # send the object to Spectra S3
            if not obj.inCache:
                client.putObject(bucketName, obj.name, obj.offset, obj.length, bulkResult.jobId)
                client.getObject(bucketName, obj.name, obj.offset, bulkGetResult.jobId, tempFiles[obj.name][1])

# iterate over the temporary files, printing out their names, then closing and and removing them
for objName in tempFiles.keys():
    print(objName)
    os.close(tempFiles[objName][0])
    os.remove(tempFiles[objName][1])
```

Here's an example of using getService and getBucket to list all accessible buckets and the names of their objects

```python
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


Suppose we didn't want to get the contents of a bucket all at once, but in sections; to do that, we can use the maxKeys and nextMarker parameters
For instance, if we wanted to look at objects in the 'books' bucket, two at a time:

```python
import os
import tempfile

from ds3 import ds3

client = ds3.createClientFromEnv()

bucketName = 'books'

# use the maxKeys parameter to specify we only want 2 objects to come back
bucketResult = client.getBucket(bucketName, maxKeys = 2)

# the first two objects
print(map(lambda bucket: bucket.name, bucketResult.objects))

# nextMarker indicates where to start the next section of objects
# it will be None when there are no more objects left
while(bucketResult.nextMarker != None):
	# we use maxKeys parameter to say we still want 2 objects, and the nextMarker parameter to say we want the section after the one we just got
	bucketResult = client.getBucket(bucketName, maxKeys = 2, nextMarker = bucketResult.nextMarker)
	print(map(lambda bucket: bucket.name, bucketResult.objects))
```

Here's an example of how to give objects on the server a different name than what is on the filesystem, and how to delete the renamed objects as though they were organized by folder

```python
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
```