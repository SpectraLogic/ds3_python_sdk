import os
import stat
import sys
import tempfile
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
        return (fileName, size)
    resources = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

    client.putBucket(bucketName)

    fileList = map(getSize, resources)

    bulkResult = client.putBulk(bucketName, fileList)

    for chunk in bulkResult.chunks:
        allocateChunk = client.allocateChunk(chunk.chunkId)
        for obj in allocateChunk.chunk.objects:
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
        self.client.putBucket(bucketName)

        bucketSet = frozenset(map(lambda service: service.name, self.client.getService()))

        self.assertTrue(bucketName in bucketSet)

        clearBucket(self.client, bucketName)

    def test_bulk_put(self):
        popluateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(len(bucketContents.objects), 4)

        clearBucket(self.client, bucketName)

    def test_bulk_get(self):
        popluateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(len(bucketContents.objects), 4)

        bulkGetResult = self.client.getBulk(bucketName, map(lambda obj: obj.name, bucketContents.objects))

        self.assertEqual(len(bulkGetResult.chunks), 1)
        self.assertEqual(len(bulkGetResult.chunks[0].objects), 4)

        tempFiles = []

        availableChunks = self.client.getAvailableChunks(bulkGetResult.jobId)

        self.assertTrue(availableChunks != None)
        self.assertEqual(len(availableChunks.bulkPlan.chunks), 1)

        for obj in availableChunks.bulkPlan.chunks[0].objects:
            newFile = tempfile.mkstemp()
            tempFiles.append(newFile)
            self.client.getObject(bucketName, obj.name, bulkGetResult.jobId, newFile[1])


        for tempFile in tempFiles:
            os.close(tempFile[0])
            os.remove(tempFile[1])

        clearBucket(self.client, bucketName)

    def prefix(self):
        populateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName, prefix = "beo")

        self.assertEqual(len(bucketContents.objects), 1)

        clearBucket(self.client, bucketName)
