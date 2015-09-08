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
    return fileList

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

    def testPutBucket(self):
        """tests putBucket"""
        self.client.putBucket(bucketName)

        bucketSet = frozenset(map(lambda service: service.name, self.client.getService()))

        self.assertTrue(bucketName in bucketSet)
        
    def testPutBucketBadInput(self):
        """tests putBucket: bad input to function"""
        self.client.putBucket(bucketName)
        badBuckets={None: 400, "": 400, bucketName: 409} # should include an integer
        for bucket, status in badBuckets.items():
            try:
                self.client.putBucket(bucket)
            except Ds3Error as e:
                self.assertEqual(e.statusCode, status)
        
    def testCreateBucketTypeChecking(self):
        some_inputs=[1234, None]
        for an_input in some_inputs:
            try:
                self.client.putBucket(an_input)
            except TypeError as e:
                self.assertEqual(str(e), "expected instance of type basestring, got instance of type "+type(an_input).__name__)

    def testDeleteEmptyBucket(self):
        """tests deleteBucket: deleting an empty bucket"""
        self.client.putBucket(bucketName)

        self.client.deleteBucket(bucketName)

        bucketSet = frozenset(map(lambda service: service.name, self.client.getService()))
        self.assertFalse(bucketName in bucketSet)
        
    def testDeleteBucketBadInput(self):
        """tests deleteBucket: bad input to function"""
        populateTestData(self.client, bucketName)
        badBuckets={None: 400, "": 400, bucketName: 409, "not-here":404} # should include an integer
        for bucket, status in badBuckets.items():
            try:
                self.client.deleteBucket(bucket)
            except Ds3Error as e:
                self.assertEqual(e.statusCode, status)
            
    def testGetEmptyBucket(self):
        """tests getBucket: when bucket is empty"""
        self.client.putBucket(bucketName)

        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(bucketContents.isTruncated, False)

        self.assertEqual(bucketContents.marker, None)

        self.assertEqual(bucketContents.delimiter, None)
        
        self.assertEqual(bucketContents.maxKeys, 1000)
        
        self.assertEqual(bucketContents.nextMarker, None)
        
        self.assertEqual(bucketContents.prefix, None)
        
        self.assertEqual(len(bucketContents.commonPrefixes), 0)
                         
        self.assertEqual(len(bucketContents.objects), 0)
        
    def testGetFilledBucket(self):
        """tests getBucket: when bucket has contents"""
        fileList=populateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(bucketContents.isTruncated, False)

        self.assertEqual(bucketContents.marker, None)

        self.assertEqual(bucketContents.delimiter, None)
        
        self.assertEqual(bucketContents.maxKeys, 1000)
        
        self.assertEqual(bucketContents.nextMarker, None)
        
        self.assertEqual(bucketContents.prefix, None)
        
        self.assertEqual(len(bucketContents.commonPrefixes), 0)
                         
        self.assertEqual(len(bucketContents.objects), 4)
        
        returnedFileList = map(lambda obj: (obj.name, obj.size), bucketContents.objects)
        self.assertEqual(returnedFileList, fileList)
        
    def testGetBadBucket(self):
        """tests getBucket: when the bucket does not exist"""
        try:
            self.client.getBucket(bucketName)
        except Ds3Error as e:
            self.assertEqual(e.statusCode, 404)
            
    def testGetBucketBadInput(self):
        """tests getBucket: bad input to function"""
        populateTestData(self.client, bucketName)
        badBuckets={None: 400, "": 400, bucketName: 404} # should include an integer
        for bucket, status in badBuckets.items():
            try:
                self.client.deleteBucket(bucket)
            except Ds3Error as e:
                self.assertEqual(e.statusCode, status)

    def testPrefix(self):
        """tests getBucket: prefix parameter"""
        populateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName, prefix = "beo")

        self.assertEqual(len(bucketContents.objects), 1)

    def testPagination(self):
        """tests getBucket: maxKeys parameter, getBucket: nextMarker parameter"""
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

    def testDelimiter(self):
        """tests getBucket: delimiter parameter"""
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

    def testGetService(self):
        """tests getService"""
        servicesBefore=map(lambda service: service.name, frozenset(self.client.getService()))
        self.assertFalse(bucketName in servicesBefore)
        
        self.client.putBucket(bucketName)
        
        servicesAfter=map(lambda service: service.name, frozenset(self.client.getService()))
        self.assertTrue(bucketName in servicesAfter)

    def testDeleteObject(self):
        """tests deleteObject: when object exists"""
        populateTestData(self.client, bucketName, resourceList=["beowulf.txt"])

        self.client.deleteObject(bucketName, "beowulf.txt")
        
        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(len(bucketContents.objects), 0)
        
    def testDeleteObjectBadInput(self):
        """tests deleteObject: bad input to function"""
        badBuckets={None: 400, bucketName: 404, "": 400, "badBucket":404} # an integer should be included as well
        badObjects=["", None, "badFile"] # an integer should be in here as well

        self.client.putBucket(bucketName)
        
        for badBucket, status in badBuckets.items():
            for badObject in badObjects:
                try:
                    self.client.deleteObject(badBucket, badObject)
                except Ds3Error as e:
                    self.assertEqual(e.statusCode, status)

    def testDeleteObjects(self):
        """tests deleteObjects"""
        fileList=populateTestData(self.client, bucketName)

        deletedResponse=self.client.deleteObjects(bucketName, map(lambda obj: obj[0], fileList))

        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(len(bucketContents.objects), 0)
        
    def testDeleteObjectsEmpty(self):
        """tests deleteObjects: when list passed is empty"""
        self.client.putBucket(bucketName)
        try:
            self.client.deleteObjects(bucketName, [])
        except Ds3Error as e:
            self.assertEqual(e.reason, "The bulk command requires a list of objects to process")
        
    def testDeleteBadObjects(self):
        """tests deleteObjects: when bucket is empty"""
        self.client.putBucket(bucketName)

        self.client.deleteObjects(bucketName, ["not-here", "also-not-here"])
        
    def testDeleteObjectsBadBucket(self):
        """tests deleteObjects: when bucket doesn't exist"""
        try:
            self.client.deleteObjects(bucketName, ["not-here", "also-not-here"])
        except Ds3Error as e:
            self.assertEqual(e.statusCode, 404)

    def testGetPhysicalPlacement(self):
        """tests getPhysicalPlacement: with an empty file"""
        populateTestData(self.client, bucketName)
        self.assertEqual(len(self.client.getPhysicalPlacement(bucketName, ["bogus.txt"])), 0)

    def testGetPhysicalPlacementBadInput(self):
        """tests getPhysicalPlacement: with non-existent bucket"""
        self.assertEqual(len(self.client.getPhysicalPlacement(bucketName, ["bogus.txt"])), 0)
        
    def testDeleteFolder(self):
        """tests deleteFolder"""
        populateTestData(self.client, bucketName, prefix = "folder/")

        self.client.deleteFolder(bucketName, "folder")
        
        bucketResult = self.client.getBucket(bucketName)
        
        self.assertEqual(len(bucketResult.objects), 0)
        
    def testDeleteFolderBadInput(self):
        """tests deleteFolder"""
        buckets=[bucketName, "fakebucket"]
        self.client.putBucket(bucketName)
        for bucket in buckets:
            try:
                self.client.deleteFolder(bucket, "folder")
            except Ds3Error as e:
                self.assertEqual(e.statusCode, 400)

    def testHeadObject(self):
        """tests headObject"""
        metadata={"name1":["value1"], "name2":"value2", "name3":("value3")}
        metadata_check={"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, resourceList=["beowulf.txt"], metadata=metadata)

        metadata_resp = self.client.headObject(bucketName, "beowulf.txt")
        
        self.assertEqual(metadata_check, metadata_resp)

    def testHeadObjectBadInput(self):
        """tests headObject: bad input to function"""
        metadata={"name1":["value1"], "name2":"value2", "name3":("value3")}

        populateTestData(self.client, bucketName, resourceList=["beowulf.txt"], metadata=metadata)
        
        badBuckets={None: 400, "badBucket": 404, bucketName:409, "": 400} # an integer should be included as well
        badObjects=["", None, "badFile"] # an integer should be in here as well

        # TODO (charlesh): code isn't finished here
        for badBucket, status in badBuckets.items():
            for badObject in badObjects:
                try:
                    self.client.deleteObject(badBucket, badObject)
                except Ds3Error as e:
                    if e.statusCode==403:
                        print 403, badBucket, badObject
                    elif badBucket==bucketName and badObject=="badFile":
                        self.assertEqual(e.statusCode, 404)
                    else:
                        self.assertEqual(e.statusCode, status)
                
    def testGetBulkWithMetadata(self):
        """tests getObject: metadata parameter, putObject:metadata parameter"""
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

    def testPutBulk(self):
        """ tests putBulk, allocateChunk, putObject"""
        fileList=populateTestData(self.client, bucketName)

        bucketContents = self.client.getBucket(bucketName)

        returnedFileList = map(lambda obj: (obj.name, obj.size), bucketContents.objects)
        self.assertEqual(returnedFileList, fileList)

    def testGetBulk(self):
        """tests getBulk, getAvailableChunks, getObject, getJob"""
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
            # TODO (charlesh): the result from getObject probably should be tested here

        for tempFile in tempFiles:
            os.close(tempFile[0])
            os.remove(tempFile[1])

        jobStatusResponse = self.client.getJob(bulkGetResult.jobId)
        self.assertEqual(jobStatusResponse.status, LibDs3JobStatus.COMPLETED)
