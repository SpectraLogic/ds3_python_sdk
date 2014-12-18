import os
import stat
import sys
import unittest

from ds3.ds3 import *

bucketName = "python_test_bucket"

def pathForResource(resourceName):
    encoding = sys.getfilesystemencoding()
    currentPath = os.path.dirname(unicode(__file__, encoding))
    return os.path.join(currentPath, "resources", resourceName)

def popluateTestData(client, bucketName):
    def getSize(fileName):
        size = os.stat(pathForResource(fileName)).st_size
        print "Size of " + fileName + " is " + str(size)
        return (fileName, size)
    resources = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

    client.putBucket(bucketName)

    fileList = map(getSize, resources)

    bulkResult = client.putBulk(bucketName, fileList)

    print "Processing result: " + str(bulkResult)
    for chunk in bulkResult.chunks:
        print "Processing chunk: " + str(chunk)
        allocateChunk = client.allocateChunk(chunk.chunkId)
        for obj in allocateChunk.chunk.objects:
            print "putting obj: " + obj.name
            client.putObject(bucketName, obj.name, obj.length, bulkResult.jobId, pathForResource(obj.name))

def clearBucket(client, bucketName):
    bucketContents = client.getBucket(bucketName)
    for obj in bucketContents.objects:
        client.deleteObject(bucketName, obj.name)
    client.deleteBucket(bucketName)

class BasicClientFunctionTestCase(unittest.TestCase):

    def setUp(self):
        self.client = createClientFromEnv()

    def test_create_bucket(self):
        def name(service):
            return service.name

        self.client.putBucket(bucketName)

        bucketSet = frozenset(map(name, self.client.getService()))

        self.assertTrue(bucketName in bucketSet)

        clearBucket(self.client, bucketName)

    def test_bulk_put(self):
        popluateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(len(bucketContents.objects), 4)

        sys.exit(1)

        clearBucket(self.client, bucketName)
