DS3 Python SDK
--------------

An SDK conforming to the DS3 specification.

Contact Us
----------

Join us at our [Google Groups](https://groups.google.com/d/forum/spectralogicds3-sdks) forum to ask questions, or see frequently asked questions.

Installing
----------

Follow the instructions for installing the [ds3_c_sdk](https://github.com/SpectraLogic/ds3_c_sdk) first.  The ds3_python_sdk uses the ds3_c_sdk to communicate with a DS3 endpoint, and will not function without it.

To install the ds3_python_sdk, either clone the latest code, or download a release bundle from [Releases](http://github.com/SpectraLogic/ds3_python_sdk/releases).  Once the code has been download, cd into the bundle, and install it with `sudo python setup.py install`

Once `setup.py` completes the ds3_python_sdk should be installed and available to be imported into python scripts.

SDK
---

The SDK provides an interface for a user to add DS3 functionality to their existing or new python code.  In order to take advantage of the SDK you need to import the `ds3` python package and module.  The following is an example that creates a ds3 client from environment variables, creates a bucket, and lists all the buckets that are visible to the user.

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

To put data to a DS3 appliance you have to do it inside of the context of what is called a Bulk Job.  Bulk Jobs allow the DS3 application to plan how data should land to cache, and subsequently get written/read to/from tape.  The basic flow of every job is:

* Generate the list of objects that will either be sent to DS3 or retrieved from DS3
* Send a bulk put/get to DS3 to plan the job
* The job will be split into multiple chunks.  An application must then get the available list of chunks that can be processed
* For each chunk that can be processed, sent the object (this step can be done in parallel)
* Repeat getting the list of available chunks until all chunks have been processed

Here is an example of the above using the Python SDK for putting data:

```python

from ds3 import ds3
import os

client = ds3.createClientFromEnv()

bucketName = "testBucket"

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

# the bulk request will split the files over several chunks if it needs to
# we need have to iterate over the chunks, ask the server for spacd to send
# the chunk, then send all the objects returned in the chunk
for chunk in bulkResult.chunks:
    allocateChunk = client.allocateChunk(chunk.chunkId)
    for obj in allocateChunk.chunk.objects:
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
