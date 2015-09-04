import os
import stat
import sys
import tempfile
import unittest

from ds3.ds3 import *
from ds3.libds3 import LibDs3JobStatus

bucketName = "python_test_bucket"

def pathForResource(resourceName):
    encoding = sys.getfilesystemencoding()
    currentPath = os.path.dirname(unicode(__file__, encoding))
    return os.path.join(currentPath, "resources", resourceName)

def populateTestData(client, bucketName, resourceList = None, prefix = "", metadata = None):
    if not resourceList:
        resourceList = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

    def getSize(fileName):
        size = os.stat(pathForResource(fileName)).st_size
        return (prefix + fileName, size)

    client.putBucket(bucketName)

    pathes={prefix + fileName: pathForResource(fileName) for fileName in resourceList}

    fileList = map(getSize, resourceList)

    bulkResult = client.putBulk(bucketName, fileList)

    for chunk in bulkResult.chunks:
        allocateChunk = client.allocateChunk(chunk.chunkId)
        for obj in allocateChunk.chunk.objects:
            client.putObject(bucketName, obj.name, obj.offset, obj.length, bulkResult.jobId, pathes[obj.name], metadata)

def clearBucket(client, bucketName):
    bucketContents = client.getBucket(bucketName)
    for obj in bucketContents.objects:
        client.deleteObject(bucketName, obj.name)
    client.deleteBucket(bucketName)

class BasicClientFunctionTestCase(unittest.TestCase):

    def setUp(self):
        self.client = createClientFromEnv()

    def tearDown(self):
        try:
            clearBucket(self.client, bucketName)
        except Ds3Error as e:
            pass

    def testCreateBucket(self):
        self.client.putBucket(bucketName)

        bucketSet = frozenset(map(lambda service: service.name, self.client.getService()))

        self.assertTrue(bucketName in bucketSet)
        
    def testCreateBucketTypeChecking(self):
        some_inputs=[1234, None]
        for an_input in some_inputs:
            try:
                self.client.putBucket(an_input)
            except TypeError as e:
                self.assertEqual(str(e), "expected instance of type basestring, got instance of type "+type(an_input).__name__)

    def testDeleteEmptyBucket(self):
        self.client.putBucket(bucketName)

        self.client.deleteBucket(bucketName)

        bucketSet = frozenset(map(lambda service: service.name, self.client.getService()))
        self.assertFalse(bucketName in bucketSet)

    def testGetPhysicalPlacement(self):
        populateTestData(self.client, bucketName)

        bogus=["bogus.txt"]
        
        self.assertEqual(len(self.client.getPhysicalPlacement(bucketName, bogus)), 0)

    def testDeleteObjects(self):
        populateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName)

        fileNameList = map(lambda obj: obj.name, bucketContents.objects)

        self.client.deleteObjects(bucketName, fileNameList)
        
        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(len(bucketContents.objects), 0)
        
    def testDeleteFolder(self):
        populateTestData(self.client, bucketName, prefix = "folder/")

        self.client.deleteFolder(bucketName, "folder")
        
        bucketResult = self.client.getBucket(bucketName)
        
        self.assertEqual(len(bucketResult.objects), 0)

    def testHeadObject(self):
        metadata={"name1":["value1"], "name2":"value2", "name3":("value3")}
        metadata_check={"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, resourceList=["beowulf.txt"], metadata=metadata)

        metadata_resp = self.client.headObject(bucketName, "beowulf.txt")
        
        self.assertEqual(metadata_check, metadata_resp)

    def testGetObjectWithMetadata(self):
        metadata={"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, resourceList=["beowulf.txt"], metadata=metadata)

        bucketContents = self.client.getBucket(bucketName)
        
        bulkGetResult = self.client.getBulk(bucketName, map(lambda obj: obj.name, bucketContents.objects))
        
        tempFiles = []
        
        availableChunks = self.client.getAvailableChunks(bulkGetResult.jobId)

        for obj in availableChunks.bulkPlan.chunks[0].objects:
            newFile = tempfile.mkstemp()
            tempFiles.append(newFile)

            metadata_resp=self.client.getObject(bucketName, obj.name, obj.offset, bulkGetResult.jobId, newFile[1])
        
        for tempFile in tempFiles:
            os.close(tempFile[0])
            os.remove(tempFile[1])

        jobStatusResponse = self.client.getJob(bulkGetResult.jobId)

        self.assertEqual(metadata, metadata_resp)
        self.assertEqual(jobStatusResponse.status, LibDs3JobStatus.COMPLETED)

    def testBulkPut(self):
        populateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(len(bucketContents.objects), 4)

    def testBulkGet(self):
        populateTestData(self.client, bucketName)

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

            self.client.getObject(bucketName, obj.name, obj.offset, bulkGetResult.jobId, newFile[1])

        for tempFile in tempFiles:
            os.close(tempFile[0])
            os.remove(tempFile[1])

        jobStatusResponse = self.client.getJob(bulkGetResult.jobId)
        self.assertEqual(jobStatusResponse.status, LibDs3JobStatus.COMPLETED)

    def testPrefix(self):
        populateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName, prefix = "beo")

        self.assertEqual(len(bucketContents.objects), 1)

    def testPagination(self):
        fileList = []
        for i in xrange(0, 15):
            fileList.append(("file" + str(i), 0))

        self.client.putBucket(bucketName)
        self.client.putBulk(bucketName, fileList)

        bucketResult = self.client.getBucket(bucketName, maxKeys = 5)

        self.assertEqual(len(bucketResult.objects), 5)
        self.assertTrue(bucketResult.nextMarker != None)
        self.assertEqual(bucketResult.objects[4].name[4:6], "12")

        bucketResult = self.client.getBucket(bucketName, maxKeys = 5, nextMarker = bucketResult.nextMarker)

        self.assertEqual(len(bucketResult.objects), 5)
        self.assertTrue(bucketResult.nextMarker != None)
        self.assertEqual(bucketResult.objects[4].name[4], "4")

        bucketResult = self.client.getBucket(bucketName, maxKeys = 5, nextMarker = bucketResult.nextMarker)

        self.assertEqual(len(bucketResult.objects), 5)
        self.assertTrue(bucketResult.nextMarker == None)
        self.assertEqual(bucketResult.objects[4].name[4], "9")

    def testDeleteBadKey(self):
        self.client.putBucket(bucketName)
        try:
            self.client.deleteObject(bucketName, "badFile")
        except Ds3Error as e:
            self.assertEqual(e.statusCode, 404)

    def testDelimiter(self):
        fileList = []

        for i in xrange(0, 10):
            fileList.append(("dir/file" + str(i), 0))

        for i in xrange(0, 10):
            fileList.append(("file" + str(i), 0))

        self.client.putBucket(bucketName)

        self.client.putBulk(bucketName, fileList)

        bucketResult = self.client.getBucket(bucketName, delimiter = "/")

        self.assertEqual(len(bucketResult.objects), 10)

        self.assertEqual(len(bucketResult.commonPrefixes), 1)
        self.assertEqual(bucketResult.commonPrefixes[0], "dir/")
