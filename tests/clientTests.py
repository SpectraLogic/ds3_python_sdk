import os
import stat
import sys
import tempfile
import unittest

from ds3.ds3 import *
from ds3.libds3 import LibDs3JobStatus

bucketName = "python_test_bucket"
resources = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

def pathForResource(resourceName):
    encoding = sys.getfilesystemencoding()
    currentPath = os.path.dirname(unicode(__file__, encoding))
    return os.path.join(currentPath, "resources", resourceName)

def populateTestData(client, bucketName, resourceList = None, prefix = "", metadata = None):
    if not resourceList:
        resourceList = resources

    def getSize(fileName):
        size = os.stat(pathForResource(fileName)).st_size
        return (prefix + fileName, size)

    client.putBucket(bucketName)

    pathes = {prefix + fileName: pathForResource(fileName) for fileName in resourceList}

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

def statusCodeList(status):
    return [Ds3Error, lambda obj: obj.statusCode, status]

def typeErrorList(badType):
    return [TypeError, str, "expected instance of type basestring, got instance of type " + type(badType).__name__]

class Ds3TestCase(unittest.TestCase):
    def setUp(self):
        self.client = createClientFromEnv()

    def tearDown(self):
        try:
            clearBucket(self.client, bucketName)
        except Ds3Error as e:
            pass
        
    def checkBadInputs(self, testFunction, inputs, second_arg_dict = None):
        for test_input, status in inputs.items():
            if second_arg_dict:
                for arg, second_status in second_arg_dict.items():
                    if second_status:
                        try:
                            testFunction(test_input, arg)
                        except second_status[0] as e:
                            self.assertEqual(second_status[1](e), second_status[2])
                    else:
                        try:
                            testFunction(test_input, arg)
                        except status[0] as e:
                            self.assertEqual(status[1](e), status[2])
            else:
                try:
                    testFunction(test_input)
                except status[0] as e:
                    self.assertEqual(status[1](e), status[2])
                    
class BucketTestCase(Ds3TestCase):
    def testPutBucket(self):
        """tests putBucket"""
        self.client.putBucket(bucketName)

        bucketSet = frozenset(map(lambda service: service.name, self.client.getService()))

        self.assertTrue(bucketName in bucketSet)
        
    def testPutBucketBadInput(self):
        """tests putBucket: bad input to function"""
        self.client.putBucket(bucketName)
        badBuckets = {"": statusCodeList(400), bucketName: statusCodeList(409), 1234: typeErrorList(1234), None:typeErrorList(None)}
        self.checkBadInputs(self.client.putBucket, badBuckets)

    def testDeleteEmptyBucket(self):
        """tests deleteBucket: deleting an empty bucket"""
        self.client.putBucket(bucketName)

        self.client.deleteBucket(bucketName)

        bucketSet = frozenset(map(lambda service: service.name, self.client.getService()))
        self.assertFalse(bucketName in bucketSet)
        
    def testDeleteBucketBadInput(self):
        """tests deleteBucket: bad input to function"""
        populateTestData(self.client, bucketName)
        
        badBuckets = {"": statusCodeList(400), bucketName: statusCodeList(409), "not-here": statusCodeList(404), 1234: typeErrorList(1234), None:typeErrorList(None)}
        self.checkBadInputs(self.client.deleteBucket, badBuckets)
            
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
        fileList = populateTestData(self.client, bucketName)

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
            
    def testGetBucketBadInput(self):
        """tests getBucket: bad input to function"""
        badBuckets = {"": statusCodeList(400), "not-here": statusCodeList(404), 1234: typeErrorList(1234), None:typeErrorList(None)}
        self.checkBadInputs(self.client.getBucket, badBuckets)

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
        servicesBefore = map(lambda service: service.name, frozenset(self.client.getService()))
        self.assertFalse(bucketName in servicesBefore)
        
        self.client.putBucket(bucketName)
        
        servicesAfter = map(lambda service: service.name, frozenset(self.client.getService()))
        self.assertTrue(bucketName in servicesAfter)
        
    def testHeadBucket(self):
        self.client.putBucket(bucketName)
        self.client.headBucket(bucketName)
        
    def testHeadBucketBadInput(self):
        badBuckets = {"": statusCodeList(400), "not-here": statusCodeList(404), 1234: typeErrorList(1234), None:typeErrorList(None)}
        self.checkBadInputs(self.client.headBucket, badBuckets)

class JobTestCase(Ds3TestCase):
    def testGetJobs(self):
        populateTestData(self.client, bucketName)
        bucketContents = self.client.getBucket(bucketName)
        bulkGetResult = self.client.getBulk(bucketName, map(lambda obj: obj.name, bucketContents.objects))
        
        result = map(lambda obj: obj.jobId, self.client.getJobs())
        self.assertTrue(bulkGetResult.jobId in result)

        self.client.deleteJob(bulkGetResult.jobId)
        
        result = map(lambda obj: obj.jobId, self.client.getJobs())
        self.assertFalse(bulkGetResult.jobId in result)

class ObjectTestCase(Ds3TestCase):
    def validateSearchObjects(self, objects, resourceList = resources, objType = "DATA"):
        self.assertEqual(len(objects), len(resourceList))

        def getSize(fileName):
            size = os.stat(pathForResource(fileName)).st_size
            return (fileName, size)
        fileList = map(getSize, resourceList)

        self.assertEqual(len(set(map(lambda obj: obj.bucketId, objects))), 1)
        
        for index in xrange(0, len(objects)):
            self.assertEqual(objects[index].name, fileList[index][0])
            # charlesh: in BP 1.2, size returns 0 (will be fixed in 2.4)
            # self.assertEqual(objects[index].size, fileList[index][1])
            self.assertEqual(objects[index].type, objType)
            self.assertEqual(objects[index].version, "1")

    def testDeleteObject(self):
        """tests deleteObject: when object exists"""
        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"])

        self.client.deleteObject(bucketName, "beowulf.txt")
        
        bucketContents = self.client.getBucket(bucketName)

        self.assertEqual(len(bucketContents.objects), 0)
        
    def testDeleteObjectBadInput(self):
        """tests deleteObject: bad input to function"""
        self.client.putBucket(bucketName)
        badBuckets = {1234:typeErrorList(1234), None:typeErrorList(None)}
        self.checkBadInputs(self.client.deleteObject, badBuckets, second_arg_dict = {"":None, "badFile":None, 1234: None, None:None})
        badBuckets = {bucketName: statusCodeList(404), "not-here": statusCodeList(404)}
        self.checkBadInputs(self.client.deleteObject, badBuckets, second_arg_dict = {"":None, "badFile":None, 1234: typeErrorList(1234), None:typeErrorList(None)})
        badBuckets = {"": statusCodeList(400)}
        self.checkBadInputs(self.client.deleteObject, badBuckets, second_arg_dict = {"badFile":None})

    def testDeleteObjects(self):
        """tests deleteObjects"""
        fileList = populateTestData(self.client, bucketName)

        deletedResponse = self.client.deleteObjects(bucketName, map(lambda obj: obj[0], fileList))

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
        try:
            self.client.getPhysicalPlacement(bucketName, ["bogus.txt"])
        except Ds3Error as e:
            self.assertEqual(e.statusCode, 404)
            
    def testGetPhysicalPlacementFull(self):
        """tests getPhysicalPlacement: with an empty file"""
        populateTestData(self.client, bucketName)
        self.assertEqual(len(self.client.getPhysicalPlacement(bucketName, ["bogus.txt"], fullDetails = True)), 0)

    def testGetPhysicalPlacementFullBadInput(self):
        """tests getPhysicalPlacement: with non-existent bucket"""
        try:
            self.client.getPhysicalPlacement(bucketName, ["bogus.txt"], fullDetails = True)
        except Ds3Error as e:
            self.assertEqual(e.statusCode, 404)
        
    def testDeleteFolder(self):
        """tests deleteFolder"""
        populateTestData(self.client, bucketName, prefix = "folder/")

        self.client.deleteFolder(bucketName, "folder")
        
        bucketResult = self.client.getBucket(bucketName)
        
        self.assertEqual(len(bucketResult.objects), 0)
        
    def testDeleteFolderBadInput(self):
        """tests deleteFolder"""
        self.client.putBucket(bucketName)
        badBuckets = {"": statusCodeList(400), "fakeBucket": statusCodeList(400), bucketName: statusCodeList(400)}
        self.checkBadInputs(self.client.deleteFolder, badBuckets, second_arg_dict = {"folder":None})

    def testGetObjects(self):
        # charlesh: the C SDK currently always expects a bucket name even though the specification says it's optional.
        # the Python call is written so the bucket name is optional, but will still error (because of the C SDK) when it is not given
        populateTestData(self.client, bucketName)

        objects = self.client.getObjects()

        self.validateSearchObjects(objects, resources)
            
    def testGetObjectsBucketName(self):
        populateTestData(self.client, bucketName)

        objects = self.client.getObjects(bucketName = bucketName)

        self.validateSearchObjects(objects, resources)
            
    def testGetObjectsObjectName(self):
        populateTestData(self.client, bucketName)

        objects = self.client.getObjects(bucketName = bucketName, name = "beowulf.txt")
        
        self.validateSearchObjects(objects, ["beowulf.txt"])
            
    def testGetObjectsPageParameters(self):
        populateTestData(self.client, bucketName)

        first_half = self.client.getObjects(bucketName = bucketName, pageLength = 2)
        self.assertEqual(len(first_half), 2)
        second_half = self.client.getObjects(bucketName = bucketName, pageLength = 2, pageOffset = 2)
        self.assertEqual(len(second_half), 2)
        
        self.validateSearchObjects(first_half+second_half, resources)
            
    def testGetObjectsType(self):
        populateTestData(self.client, bucketName)

        objects = self.client.getObjects(bucketName = bucketName, objType = "DATA")
        
        self.validateSearchObjects(objects, resources)

        objects = self.client.getObjects(bucketName = bucketName, objType = "FOLDER")
        
        self.validateSearchObjects(objects, [], objType = "FOLDER")
            
    def testGetObjectsVersion(self):
        populateTestData(self.client, bucketName)

        objects = self.client.getObjects(bucketName = bucketName, version = 1)
        
        self.validateSearchObjects(objects, resources)

    
class ObjectMetadataTestCase(Ds3TestCase):
    def testHeadObject(self):
        """tests headObject"""
        metadata = {"name1":["value1"], "name2":"value2", "name3":("value3")}
        metadata_check = {"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"], metadata = metadata)

        metadata_resp = self.client.headObject(bucketName, "beowulf.txt")
        
        self.assertEqual(metadata_check, metadata_resp)

    def testHeadObjectBadInput(self):
        """tests headObject: bad input to function"""
        metadata = {"name1":["value1"], "name2":"value2", "name3":("value3")}

        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"], metadata = metadata)

        badBuckets = {"fakeBucket": statusCodeList(404), bucketName: statusCodeList(404)}
        self.checkBadInputs(self.client.headObject, badBuckets, second_arg_dict = {"":None, "badFile":None, None:typeErrorList(None), 1234:typeErrorList(1234)})
        badBuckets = {None:typeErrorList(None), 1234:typeErrorList(1234)}
        self.checkBadInputs(self.client.headObject, badBuckets, second_arg_dict = {"":None, "badFile":None, None:None, 1234:None})
        badBuckets = {"": statusCodeList(400)}
        self.checkBadInputs(self.client.headObject, badBuckets, second_arg_dict = {"badFile":None, None:typeErrorList(None), 1234:typeErrorList(1234)})
                
    def testGetBulkWithMetadata(self):
        """tests getObject: metadata parameter, putObject:metadata parameter"""
        metadata = {"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"], metadata = metadata)

        bucketContents = self.client.getBucket(bucketName)
        
        bulkGetResult = self.client.getBulk(bucketName, map(lambda obj: obj.name, bucketContents.objects))
        
        tempFiles = []
        
        availableChunks = self.client.getAvailableChunks(bulkGetResult.jobId)

        for obj in availableChunks.bulkPlan.chunks[0].objects:
            newFile = tempfile.mkstemp()
            tempFiles.append(newFile)

            metadata_resp = self.client.getObject(bucketName, obj.name, obj.offset, bulkGetResult.jobId, newFile[1])
        
        for tempFile in tempFiles:
            os.close(tempFile[0])
            os.remove(tempFile[1])

        jobStatusResponse = self.client.getJob(bulkGetResult.jobId)

        self.assertEqual(metadata, metadata_resp)
        self.assertEqual(jobStatusResponse.status, LibDs3JobStatus.COMPLETED)
        
class BasicClientTestCase(Ds3TestCase):
    def testGetSystemInformation(self):
        result = self.client.getSystemInformation()

        self.assertNotEqual(result.apiVersion, None)
        self.assertNotEqual(result.serialNumber, None)

    def testVerifySystemHealth(self):
        result = self.client.verifySystemHealth()

        self.assertTrue(result.msRequiredToVerifyDataPlannerHealth >= 0)
