#   Copyright 2014-2015 Spectra Logic Corporation. All Rights Reserved.
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
import stat
import sys
import tempfile
import unittest

from ds3.ds3 import *

bucketName = "python_test_bucket"
resources = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]
unicodeResources = [unicode(filename) for filename in resources]

def pathForResource(resourceName):
    return pathForFileName(resourceName, "resources")
    
def pathForFileName(resourceName, fileName):
    encoding = sys.getfilesystemencoding()
    currentPath = os.path.dirname(unicode(__file__, encoding))
    return os.path.join(currentPath, fileName, resourceName)

def populateTestData(client, bucketName, dataPolicyId, resourceList = None, prefix = "", metadata = None, createBucket=True):
    if not resourceList:
        resourceList = resources

    def getSize(fileName):
        size = os.stat(pathForResource(fileName)).st_size
        return FileObject(prefix + fileName, size)

    if createBucket:
        client.put_bucket_spectra_s3(PutBucketSpectraS3Request(bucketName, data_policy_id=dataPolicyId))

    pathes = {prefix + fileName: pathForResource(fileName) for fileName in resourceList}
    #pathes = {prefix + key: pathForResource(key) for keyin resources}

    fileList = map(getSize, resourceList)
    fileObjectList = FileObjectList(fileList)

    bulkResult = client.put_bulk_job_spectra_s3(PutBulkJobSpectraS3Request(bucketName, fileObjectList))

    for chunk in bulkResult.result['ObjectsList']:
        allocateChunk = client.allocate_job_chunk_spectra_s3(AllocateJobChunkSpectraS3Request(chunk['ChunkId']))
        for obj in allocateChunk.result['ObjectList']:
            filePath = pathes[obj['Name']]
            fileSize = obj['Length'] #?
            localFileStream = open(filePath, "rb")
            client.put_object(PutObjectRequest(bucketName, obj['Name'], fileSize, localFileStream, offset=int(obj['Offset']), job=bulkResult.result['JobId'], headers=metadata))
            localFileStream.close()
            
    return fileList

def clearBucket(client, bucketName):
    bucketContents = client.get_bucket(GetBucketRequest(bucketName))
    if bucketContents.response.status == 404:
        #There is no bucket to delete
        return
    for obj in bucketContents.result['ContentsList']:
        client.delete_object(DeleteObjectRequest(bucketName, obj['Key']))
    client.delete_bucket(DeleteBucketRequest(bucketName))

def statusCodeList(status):
    return [RequestFailed, lambda obj: obj.http_error_code, status]

def typeErrorList(badType):
    return [RequestFailed, str, "expected instance of type basestring, got instance of type " + type(badType).__name__]

def reasonErrorList(reason):
    return [RequestFailed, str, reason]
    
def setupStorageDomainMember(client, storageDomainName, poolPartitionName):
    '''Creates a storage domain, pool partition, and links the two via a storage domain member'''
    storageResponse = client.put_storage_domain_spectra_s3(
                PutStorageDomainSpectraS3Request(storageDomainName))
    poolResponse = client.put_pool_partition_spectra_s3(
                PutPoolPartitionSpectraS3Request(poolPartitionName, "ONLINE"))
    memberResponse = client.put_pool_storage_domain_member_spectra_s3(
                PutPoolStorageDomainMemberSpectraS3Request(poolPartitionName, storageDomainName))
    ids = {}
    ids["StorageId"] = storageResponse.result['Id']
    ids["PoolId"] = poolResponse.result['Id']
    ids["MemberId"] = memberResponse.result['Id']
    return ids
    
def teardownStorageDomainMember(client, ids):
    '''Deletes the storage domain member, the storage domain, and the pool partition'''
    client.delete_storage_domain_member_spectra_s3(
                DeleteStorageDomainMemberSpectraS3Request(ids["MemberId"]))
    
    client.delete_pool_partition_spectra_s3(
                DeletePoolPartitionSpectraS3Request(ids["PoolId"]))
    
    client.delete_storage_domain_spectra_s3(
                DeleteStorageDomainSpectraS3Request(ids["StorageId"]))

def setupTestEnvironment(client):
    # Set up test storage domain
    ids = setupStorageDomainMember(client, "PythonTestEnvDomain", "PythonTestEnvPoolPartition")
    
    # Create data policy
    dataPolicyResponse = client.put_data_policy_spectra_s3(
                PutDataPolicySpectraS3Request("PythonTestEnvDataPolicy"))
    
    ids['DataPolicyId'] = dataPolicyResponse.result['Id']
    
    # Create data persistence rule
    persistenceRuleResponse = client.put_data_persistence_rule_spectra_s3(
                PutDataPersistenceRuleSpectraS3Request(ids['DataPolicyId'], 
                                                       'STANDARD', 
                                                       ids['StorageId'], 
                                                       'PERMANENT'))
    
    ids['PersistenceRuleId'] = persistenceRuleResponse.result['Id']
    return ids
    
def teardownTestEnvironment(client, ids):
    # Delete data persistence rule
    client.delete_data_persistence_rule_spectra_s3(
                DeleteDataPersistenceRuleSpectraS3Request(ids['PersistenceRuleId']))
    
    # Delete data policy
    client.delete_data_policy_spectra_s3(DeleteDataPolicySpectraS3Request(ids['DataPolicyId']))
    
    # Tear down test storage domain
    teardownStorageDomainMember(client, ids)
    
class Ds3TestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Ds3TestCase, self).__init__(*args, **kwargs)
        self.envStorageIds = []
        
    def setUp(self):
        self.client = createClientFromEnv()
        self.envStorageIds = setupTestEnvironment(self.client)

    def tearDown(self):
        try:
            clearBucket(self.client, bucketName)
        except RequestFailed as e:
            pass
        teardownTestEnvironment(self.client, self.envStorageIds)
        
    def checkBadInputs(self, testFunction, inputs):
        for test_input, status in inputs.items():
            try:
                testFunction(test_input)
            except status[0] as e:
                self.assertEqual(status[1](e), status[2])
    
    def getDataPolicyId(self):
        return self.envStorageIds['DataPolicyId']
    
    def createBucket(self, myBucketName):
        self.client.put_bucket_spectra_s3(PutBucketSpectraS3Request(myBucketName, data_policy_id=self.getDataPolicyId()))
                    
class BucketTestCase(Ds3TestCase):
    def testPutBucket(self):
        """tests putBucket"""
        self.createBucket(unicode(bucketName))

        getService = self.client.get_service(GetServiceRequest())
        self.assertEqual(getService.response.status, 200)
        bucketSet = frozenset(map(lambda service: service['Name'], getService.result['BucketList']))

        self.assertTrue(bucketName in bucketSet)
        
    def testPutBucketUnicode(self):
        """tests putBucket"""
        self.createBucket(unicode(bucketName))

        getService = self.client.get_service(GetServiceRequest())
        self.assertEqual(getService.response.status, 200)
        bucketSet = frozenset(map(lambda service: service['Name'], getService.result['BucketList']))

        self.assertTrue(bucketName in bucketSet)
        
    def testPutBucketBadInput(self):
        """tests putBucket: bad input to function"""
        self.createBucket(bucketName)
        badBuckets = {PutBucketRequest(""): statusCodeList(400), PutBucketRequest(bucketName): statusCodeList(409)}
        self.checkBadInputs(self.client.put_bucket, badBuckets)

    def testDeleteEmptyBucket(self):
        """tests deleteBucket: deleting an empty bucket"""
        self.createBucket(bucketName)

        self.client.delete_bucket(DeleteBucketRequest(bucketName))

        getService = self.client.get_service(GetServiceRequest())
        bucketSet = frozenset(map(lambda service: service['Name'], getService.result['BucketList']))
        self.assertFalse(bucketName in bucketSet)
        
    def testDeleteBucketBadInput(self):
        """tests deleteBucket: bad input to function"""
        populateTestData(self.client, bucketName, self.getDataPolicyId())
        
        badBuckets = {DeleteBucketRequest(""): statusCodeList(400), DeleteBucketRequest(bucketName): statusCodeList(409), DeleteBucketRequest("not-here"): statusCodeList(404)}
        self.checkBadInputs(self.client.delete_bucket, badBuckets)
            
    def testGetEmptyBucket(self):
        """tests getBucket: when bucket is empty"""
        self.createBucket(bucketName)

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(bucketContents.result['IsTruncated'], 'false')

        self.assertEqual(bucketContents.result['Marker'], None)

        self.assertEqual(bucketContents.result['Delimiter'], None)
        
        self.assertEqual(bucketContents.result['MaxKeys'], '1000')
        
        self.assertEqual(bucketContents.result['NextMarker'], None)
        
        self.assertEqual(bucketContents.result['Prefix'], None)
        
        self.assertEqual(len(bucketContents.result['CommonPrefixesList']), 0)
                         
        self.assertEqual(len(bucketContents.result['ContentsList']), 0)
        
    def testPutBulkUnicode(self):
        """tests getBucket: when bucket has contents"""
        fileList = populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = unicodeResources)

    def testGetFilledBucket(self):
        """tests getBucket: when bucket has contents"""
        fileList = populateTestData(self.client, bucketName, self.getDataPolicyId())

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(bucketContents.result['IsTruncated'], 'false')

        self.assertEqual(bucketContents.result['Marker'], None)

        self.assertEqual(bucketContents.result['Delimiter'], None)
        
        self.assertEqual(bucketContents.result['MaxKeys'], '1000')
        
        self.assertEqual(bucketContents.result['NextMarker'], None)
        
        self.assertEqual(bucketContents.result['Prefix'], None)
        
        self.assertEqual(len(bucketContents.result['CommonPrefixesList']), 0)
                         
        self.assertEqual(len(bucketContents.result['ContentsList']), 4)
        
        returnedFileList = map(lambda obj: (obj['Key'], obj['Size']), bucketContents.result['ContentsList'])
        
        simpleFileList = []
        for file in fileList:
          simpleFileList.append((file.name, str(file.size)))
        self.assertEqual(returnedFileList, simpleFileList)
            
    def testGetBucketBadInput(self):
        """tests getBucket: bad input to function"""
        badBuckets = {GetBucketRequest(""): reasonErrorList("Reason: The bucket name parameter is required.")}
        self.checkBadInputs(self.client.get_bucket, badBuckets)

    def testPrefix(self):
        """tests getBucket: prefix parameter"""
        populateTestData(self.client, bucketName, self.getDataPolicyId())

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName, prefix = "beo"))

        self.assertEqual(len(bucketContents.result['ContentsList']), 1)

    def testPagination(self):
        """tests getBucket: maxKeys parameter, getBucket: nextMarker parameter"""
        fileList = []
        for i in xrange(0, 15):
            fileList.append(FileObject("file" + str(i), 0))

        self.createBucket(bucketName)
        self.client.put_bulk_job_spectra_s3(PutBulkJobSpectraS3Request(bucketName, FileObjectList(fileList)))

        bucketResult = self.client.get_bucket(GetBucketRequest(bucketName, max_keys = 5))

        self.assertEqual(len(bucketResult.result['ContentsList']), 5)
        self.assertTrue(bucketResult.result['NextMarker'] != None)
        self.assertEqual(bucketResult.result['ContentsList'][4]['Key'][4:6], "12")

        bucketResult = self.client.get_bucket(GetBucketRequest(bucketName, max_keys = 5, marker = bucketResult.result['NextMarker']))

        self.assertEqual(len(bucketResult.result['ContentsList']), 5)
        self.assertTrue(bucketResult.result['NextMarker'] != None)
        self.assertEqual(bucketResult.result['ContentsList'][4]['Key'][4], "4")

        bucketResult = self.client.get_bucket(GetBucketRequest(bucketName, max_keys = 5, marker = bucketResult.result['NextMarker']))

        self.assertEqual(len(bucketResult.result['ContentsList']), 5)
        self.assertTrue(bucketResult.result['NextMarker'] == None)
        self.assertEqual(bucketResult.result['ContentsList'][4]['Key'][4], "9")

    def testDelimiter(self):
        """tests getBucket: delimiter parameter"""
        fileList = []

        for i in xrange(0, 10):
            fileList.append(FileObject("dir/file" + str(i), 0))

        for i in xrange(0, 10):
            fileList.append(FileObject("file" + str(i), 0))

        self.createBucket(bucketName)

        self.client.put_bulk_job_spectra_s3(PutBulkJobSpectraS3Request(bucketName, FileObjectList(fileList)))

        bucketResult = self.client.get_bucket(GetBucketRequest(bucketName, delimiter = "/"))

        self.assertEqual(len(bucketResult.result['ContentsList']), 10)

        self.assertEqual(len(bucketResult.result['CommonPrefixesList']), 1)
        self.assertEqual(bucketResult.result['CommonPrefixesList'][0]['Prefix'], "dir/")

    def testGetService(self):
        """tests getService"""
        beforeResponse = self.client.get_service(GetServiceRequest())
        servicesBefore = map(lambda service: service['Name'], beforeResponse.result['BucketList'])
        self.assertFalse(bucketName in servicesBefore)
        
        self.createBucket(bucketName)
        
        afterResponse = self.client.get_service(GetServiceRequest())
        servicesAfter = map(lambda service: service['Name'], afterResponse.result['BucketList'])
        self.assertTrue(bucketName in servicesAfter)
        
    def testHeadBucket(self):
        self.createBucket(bucketName)
        self.client.head_bucket(HeadBucketRequest(bucketName))
        
    def testHeadBucketBadInput(self):
        badBuckets = {HeadBucketRequest(""): statusCodeList(400), HeadBucketRequest("not-here"): statusCodeList(404)}
        self.checkBadInputs(self.client.head_bucket, badBuckets)

class JobTestCase(Ds3TestCase):
    def testGetJobs(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())
        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))
        
        fileObjects = FileObjectList(map(lambda obj: FileObject(obj['Key']), bucketContents.result['ContentsList']))
        bulkGetResult = self.client.get_bulk_job_spectra_s3(GetBulkJobSpectraS3Request(bucketName, fileObjects))
        bulkId = bulkGetResult.result['JobId']
        
        jobsBefore = self.client.get_jobs_spectra_s3(GetJobsSpectraS3Request())
        result = map(lambda obj: obj['JobId'], jobsBefore.result['JobList'])
        self.assertTrue(bulkId in result)

        self.client.cancel_job_spectra_s3(CancelJobSpectraS3Request(bulkId))
        
        jobsAfter = self.client.get_jobs_spectra_s3(GetJobsSpectraS3Request())
        result = map(lambda obj: obj['JobId'], jobsAfter.result['JobList'])
        self.assertFalse(bulkId in result)

class ObjectTestCase(Ds3TestCase):
    def validateSearchObjects(self, objects, resourceList = resources, objType = "DATA"):
        self.assertEqual(len(objects), len(resourceList))

        def getSize(fileName):
            size = os.stat(pathForResource(fileName)).st_size
            return (fileName, size)
        fileList = map(getSize, resourceList)

        if len(objects)>0:
            self.assertEqual(len(set(map(lambda obj: obj['BucketId'], objects))), 1)
        
        for index in xrange(0, len(objects)):
            self.assertEqual(objects[index]['Name'], fileList[index][0])
            # charlesh: in BP 1.2, size returns 0 (will be fixed in 2.4)
            # self.assertEqual(objects[index].size, fileList[index][1])
            self.assertEqual(objects[index]['Type'], objType)
            self.assertEqual(objects[index]['Version'], "1")

    def testGetObject(self):
        fileName = "beowulf.txt"
        fileList = populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = [fileName])
        
        self.assertEqual(len(fileList), 1)
        self.assertEqual(fileList[0].name, fileName)
        self.assertEqual(fileList[0].size, 294059L)
        
        fd, tempname = tempfile.mkstemp()
        f = open(tempname, "wb")
        
        getObjectResult = self.client.get_object(GetObjectRequest(bucketName, fileName, f))
        self.assertEqual(getObjectResult.response.status, 200)
        self.assertEqual(os.stat(tempname).st_size, 294059L)
        
        f.close()
        os.close(fd)
        os.remove(tempname)
        
    def testGetObjectDetails(self):
        fileName = "beowulf.txt"
        populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = [fileName])
        
        response = self.client.get_object_details_spectra_s3(
                    GetObjectDetailsSpectraS3Request(fileName, bucketName))
        
        self.assertEqual(response.result['Name'], fileName)
        self.assertEqual(response.result['Type'], 'DATA')
        
    def testGetAndPutObjectStream(self):
        self.createBucket(bucketName)
        
        fileName = "beowulf.txt"
        localFileStream = open(pathForResource(fileName), "rb")
        self.client.put_object(PutObjectRequest(bucketName, fileName, 294059L, localFileStream))
        localFileStream.close()
        
        fd, tempname = tempfile.mkstemp()
        f = open(tempname, "wb")
        
        getObjectResult = self.client.get_object(GetObjectRequest(bucketName, fileName, f))
        self.assertEqual(getObjectResult.response.status, 200)
        self.assertEqual(os.stat(tempname).st_size, 294059L)
        
        f.close()
        os.close(fd)
        os.remove(tempname)
    
    def testDeleteObject(self):
        """tests deleteObject: when object exists"""
        populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = ["beowulf.txt"])

        self.client.delete_object(DeleteObjectRequest(bucketName, "beowulf.txt"))
        
        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(len(bucketContents.result['ContentsList']), 0)

    def testDeleteObjectUnicode(self):
        """tests deleteObject: unicode parameter"""
        populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = ["beowulf.txt"])

        self.client.delete_object(DeleteObjectRequest(bucketName, unicode("beowulf.txt")))
        
        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(len(bucketContents.result['ContentsList']), 0)
        
    def testDeleteObjectBadInput(self):
        """tests deleteObject: bad input to function"""
        self.createBucket(bucketName)
        
        noNameBucket = ""
        notHereBucket = "not-here"
        badBuckets = {DeleteObjectRequest(noNameBucket, ""):statusCodeList(400),
                      DeleteObjectRequest(noNameBucket, "badFile"):statusCodeList(404),
                      DeleteObjectRequest(notHereBucket, ""): statusCodeList(404),
                      DeleteObjectRequest(notHereBucket, "badFile"): statusCodeList(404),
                      DeleteObjectRequest(bucketName, ""): statusCodeList(400),
                      DeleteObjectRequest(bucketName, "badFile"): statusCodeList(404)}
        self.checkBadInputs(self.client.delete_object, badBuckets)

    def testDeleteObjects(self):
        """tests deleteObjects"""
        fileList = populateTestData(self.client, bucketName, self.getDataPolicyId())

        deleteFiles = DeleteObjectList(map(lambda obj: DeleteObject(obj.name), fileList))
        
        deletedResponse = self.client.delete_objects(DeleteObjectsRequest(bucketName, deleteFiles))

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(len(bucketContents.result['ContentsList']), 0)

    def testDeleteObjectsUnicode(self):
        """tests deleteObjects: unicode parameter"""
        fileList = populateTestData(self.client, bucketName, self.getDataPolicyId())

        deleteList = DeleteObjectList(map(lambda obj: DeleteObject(obj.name), fileList))
        deletedResponse = self.client.delete_objects(DeleteObjectsRequest(bucketName, deleteList))

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(len(bucketContents.result['ContentsList']), 0)
        
    def testDeleteObjectsEmpty(self):
        """tests deleteObjects: when list passed is empty"""
        self.createBucket(bucketName)
        try:
            self.client.delete_objects(DeleteObjectsRequest(bucketName, DeleteObjectList([])))
        except RequestFailed as e:
            self.assertEqual(e.message, "The bulk command requires a list of objects to process")
        
    def testDeleteBadObjects(self):
        """tests deleteObjects: when bucket is empty"""
        self.createBucket(bucketName)

        objects = DeleteObjectList([DeleteObject("not-here"), DeleteObject("also-not-here")])
        self.client.delete_objects(DeleteObjectsRequest(bucketName, objects))
        
    def testDeleteObjectsBadBucket(self):
        """tests deleteObjects: when bucket doesn't exist"""
        try:
            objects = DeleteObjectList([DeleteObject("not-here"), DeleteObject("also-not-here")])
            self.client.delete_objects(DeleteObjectsRequest(bucketName, objects))
        except RequestFailed as e:
            self.assertEqual(e.http_error_code, 404)

    def testGetPhysicalPlacement(self):
        """tests getPhysicalPlacement: with an empty file"""
        populateTestData(self.client, bucketName, self.getDataPolicyId())
        fileObjects = FileObjectList([FileObject("bogus.txt")])
        response = self.client.get_physical_placement_for_objects_spectra_s3(GetPhysicalPlacementForObjectsSpectraS3Request(bucketName, fileObjects))
        self.assertEqual(len(response.result['TapeList']), 0)

    def testGetPhysicalPlacementBadInput(self):
        """tests getPhysicalPlacement: with non-existent bucket"""
        try:
            objects = FileObjectList([FileObject("bogus.txt")])
            self.client.get_physical_placement_for_objects_spectra_s3(GetPhysicalPlacementForObjectsSpectraS3Request(bucketName, objects))
        except RequestFailed as e:
            self.assertEqual(e.http_error_code, 404)
            
    def testGetPhysicalPlacementFull(self):
        """tests getPhysicalPlacement: with an empty file"""
        populateTestData(self.client, bucketName, self.getDataPolicyId())
        objects = FileObjectList([FileObject("bogus.txt")])
        response = self.client.get_physical_placement_for_objects_with_full_details_spectra_s3(GetPhysicalPlacementForObjectsWithFullDetailsSpectraS3Request(bucketName, objects))
        self.assertEqual(len(response.result['ObjectList']), 0)

    def testGetPhysicalPlacementFullBadInput(self):
        """tests getPhysicalPlacement: with non-existent bucket"""
        try:
            objects = FileObjectList([FileObject("bogus.txt")])
            self.client.get_physical_placement_for_objects_with_full_details_spectra_s3(GetPhysicalPlacementForObjectsWithFullDetailsSpectraS3Request(bucketName, objects))
        except RequestFailed as e:
            self.assertEqual(e.http_error_code, 404)
        
    def testDeleteFolder(self):
        """tests deleteFolder"""
        populateTestData(self.client, bucketName, self.getDataPolicyId(), prefix = "folder/")

        self.client.delete_folder_recursively_spectra_s3(DeleteFolderRecursivelySpectraS3Request(bucketName, "folder"))
        
        bucketResult = self.client.get_bucket(GetBucketRequest(bucketName))
        
        self.assertEqual(len(bucketResult.result['ContentsList']), 0)
        
    def testDeleteFolderBadInput(self):
        """tests deleteFolder"""
        self.createBucket(bucketName)
        folder = "folder"
        badBuckets = {DeleteFolderRecursivelySpectraS3Request("", folder): statusCodeList(500),
                      DeleteFolderRecursivelySpectraS3Request("fakeBucket", folder): statusCodeList(404),
                      DeleteFolderRecursivelySpectraS3Request(bucketName, folder): statusCodeList(404)}
        self.checkBadInputs(self.client.delete_folder_recursively_spectra_s3, badBuckets)

    def testGetObjects(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())

        response = self.client.get_objects_details_spectra_s3(GetObjectsDetailsSpectraS3Request())
        objects = response.result['S3ObjectList']
        
        # Note that there may be additional objects on the BP
        self.assertTrue(len(objects) >= len(resources))
        testObjects = []
        for obj in objects:
            if obj['Name'] in resources:
                testObjects.append(obj)
        
        self.validateSearchObjects(testObjects, resources)
        self.assertEqual(response.paging_truncated, None)
        self.assertEqual(response.paging_total_result_count, None)
        
    def testGetObjectsWithPaging(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())
        
        response = self.client.get_objects_details_spectra_s3(GetObjectsDetailsSpectraS3Request(bucket_id = bucketName, page_offset = 0))
        
        self.validateSearchObjects(response.result['S3ObjectList'], resources)
        
        self.assertEqual(response.paging_truncated, 0)
        self.assertEqual(response.paging_total_result_count, 4)
            
    def testGetObjectsBucketName(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())

        objects = self.client.get_objects_details_spectra_s3(GetObjectsDetailsSpectraS3Request(bucket_id = bucketName))

        self.validateSearchObjects(objects.result['S3ObjectList'], resources)
            
    def testGetObjectsObjectName(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())

        objects = self.client.get_objects_details_spectra_s3(GetObjectsDetailsSpectraS3Request(bucket_id = bucketName, name = "beowulf.txt"))
        
        self.validateSearchObjects(objects.result['S3ObjectList'], ["beowulf.txt"])
            
    def testGetObjectsPageParameters(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())

        first_half = self.client.get_objects_details_spectra_s3(
                    GetObjectsDetailsSpectraS3Request(bucket_id = bucketName, page_length = 2))
        self.assertEqual(len(first_half.result['S3ObjectList']), 2)
        second_half = self.client.get_objects_details_spectra_s3(
                    GetObjectsDetailsSpectraS3Request(bucket_id = bucketName, page_length = 2, page_offset = 2))
        self.assertEqual(len(second_half.result['S3ObjectList']), 2)
        
        self.validateSearchObjects(first_half.result['S3ObjectList']+second_half.result['S3ObjectList'], resources)
            
    def testGetObjectsType(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())

        dataResponse = self.client.get_objects_details_spectra_s3(
                    GetObjectsDetailsSpectraS3Request(bucket_id = bucketName, type = "DATA"))
        objects = dataResponse.result['S3ObjectList']
        
        self.validateSearchObjects(objects, resources)

        folderResponse = self.client.get_objects_details_spectra_s3(GetObjectsDetailsSpectraS3Request(bucket_id = bucketName, type = "FOLDER"))
        objects = folderResponse.result['S3ObjectList']
        
        self.validateSearchObjects(objects, [], objType = "FOLDER")
            
    def testGetObjectsVersion(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())

        response = self.client.get_objects_details_spectra_s3(GetObjectsDetailsSpectraS3Request(bucket_id = bucketName, version = 1))
        objects = response.result['S3ObjectList']
        
        self.validateSearchObjects(objects, resources)
                
    def testGetBulkUnicode(self):
        """tests getObject: unicode parameter"""
        populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = unicodeResources)

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))
        
        objects = FileObjectList(map(lambda obj: FileObject(unicode(obj['Key'])), bucketContents.result['ContentsList']))
        bulkGetResult = self.client.get_bulk_job_spectra_s3(GetBulkJobSpectraS3Request(bucketName, objects))
        
        availableChunks = self.client.get_job_chunk_spectra_s3(GetJobChunkSpectraS3Request(bulkGetResult.result['JobId']))
        
        for obj in availableChunks.result['ObjectList']:
            fd, tempName = tempfile.mkstemp()
            f = open(tempName, "wb")

            metadata_resp = self.client.get_object(GetObjectRequest(bucketName, obj['Name'], f, offset = int(obj['Offset']), job = bulkGetResult.result['JobId']))
            
            f.close()
            os.close(fd)
            os.remove(tempName)

        #jobStatusResponse = self.client.getJob(bulkGetResult.jobId)
        #self.assertEqual(jobStatusResponse.status, LibDs3JobStatus.COMPLETED)
        
    def testGetObjectsWithFullDetails(self):
        populateTestData(self.client, bucketName, self.getDataPolicyId())
        
        request = GetObjectsWithFullDetailsSpectraS3Request(include_physical_placement=True, bucket_id=bucketName)
        response = self.client.get_objects_with_full_details_spectra_s3(request)
        
        self.assertEqual(len(response.result['ObjectList']), 4)
    
class ObjectMetadataTestCase(Ds3TestCase):
    def testHeadObject(self):
        """tests headObject"""
        metadata = {"name1":["value1"], "name2":"value2", "name3":("value3")}
        metadata_check = {"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = ["beowulf.txt"], metadata = metadata)

        metadata_resp = self.client.head_object(HeadObjectRequest(bucketName, "beowulf.txt"))
        
        self.assertEqual('EXISTS', metadata_resp.result)
        self.assertEqual(metadata_check, metadata_resp.meta_data)

    def testHeadObjectBadInput(self):
        """tests headObject: bad input to function"""
        metadata = {"name1":["value1"], "name2":"value2", "name3":("value3")}

        populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = ["beowulf.txt"], metadata = metadata)

        badBuckets = {HeadObjectRequest("fakeBucket", ""): reasonErrorList("Reason: The object name parameter is required."),
                      HeadObjectRequest("fakeBucket", "badFile"): statusCodeList(404),
                      HeadObjectRequest(bucketName, ""): reasonErrorList("Reason: The object name parameter is required."),
                      HeadObjectRequest(bucketName, "badFile"): statusCodeList(404),
                      HeadObjectRequest("", "badFile"): reasonErrorList("Reason: The bucket name parameter is required.")}
        self.checkBadInputs(self.client.head_object, badBuckets)
                
    def testGetBulkWithMetadata(self):
        """tests getObject: metadata parameter, putObject:metadata parameter"""
        metadata = {"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, self.getDataPolicyId(), resourceList = ["beowulf.txt"], metadata = metadata)

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))
        
        objects = FileObjectList(map(lambda obj: FileObject(obj['Key']), bucketContents.result['ContentsList']))
        bulkGetResult = self.client.get_bulk_job_spectra_s3(GetBulkJobSpectraS3Request(bucketName, objects))
        
        availableChunks = self.client.get_job_chunk_spectra_s3(GetJobChunkSpectraS3Request(bulkGetResult.result['JobId']))
        
        for obj in availableChunks.result['ObjectList']:
            fd, tempName = tempfile.mkstemp()
            f = open(tempName, "wb")

            metadata_resp = self.client.get_object(GetObjectRequest(bucketName, obj['Name'], f, offset = int(obj['Offset']), job = bulkGetResult.result['JobId']))
            
            f.close()
            os.close(fd)
            os.remove(tempName)

        jobStatusResponse = self.client.get_job_spectra_s3(GetJobSpectraS3Request(bulkGetResult.result['JobId']))

        self.assertEqual(metadata, metadata_resp.meta_data)
        #self.assertEqual(jobStatusResponse.status, LibDs3JobStatus.COMPLETED)
        
class BasicClientTestCase(Ds3TestCase):
    def testGetSystemInformation(self):
        result = self.client.get_system_information_spectra_s3(GetSystemInformationSpectraS3Request())

        self.assertNotEqual(result.result['ApiVersion'], None)
        self.assertNotEqual(result.result['SerialNumber'], None)

    def testVerifySystemHealth(self):
        result = self.client.verify_system_health_spectra_s3(VerifySystemHealthSpectraS3Request())
        self.assertTrue(result.result['MsRequiredToVerifyDataPlannerHealth'] >= 0)

class ParserTestCase(unittest.TestCase):
    def testGetServiceParsing(self):
        responsePayload = ("<ListAllMyBucketsResult><Buckets>"
                      "<Bucket><CreationDate>2016-01-27T00:28:34.000Z</CreationDate><Name>spectra-test</Name></Bucket>"
                      "<Bucket><CreationDate>2016-01-27T00:28:34.000Z</CreationDate><Name>test_bucket_1</Name></Bucket>"
                      "<Bucket><CreationDate>2016-01-27T00:28:34.000Z</CreationDate><Name>test_bucket_2</Name></Bucket>"
                      "<Bucket><CreationDate>2016-01-27T00:28:34.000Z</CreationDate><Name>test_bucket_3</Name></Bucket>"
                      "<Bucket><CreationDate>2016-01-27T00:28:34.000Z</CreationDate><Name>test_bucket_4</Name></Bucket>"
                      "</Buckets><Owner><DisplayName>test_user_name</DisplayName><ID>ef2fdcac-3c80-410a-8fcb-b567c31dd33d</ID></Owner></ListAllMyBucketsResult>")
        
        result = parseModel(xmldom.fromstring(responsePayload), ListAllMyBucketsResult())
        self.assertTrue(result['Owner'] is not None)
        self.assertEqual(len(result['BucketList']), 5)
        
class ABMTestCase(Ds3TestCase):
    def testPutDeleteDataPolicy(self):
        name = "test_put_delete_data_policy"
        # Create a data policy
        putResponse = self.client.put_data_policy_spectra_s3(
                    PutDataPolicySpectraS3Request(name))
        self.assertEqual(putResponse.response.status, 201)
        
        # Verify that the data policy exists on the BP
        getResponse = self.client.get_data_policy_spectra_s3(
                    GetDataPolicySpectraS3Request(name))
        self.assertEqual(getResponse.result['Name'], name)
        
        # Delete the data policy
        deleteResponse = self.client.delete_data_policy_spectra_s3(
                    DeleteDataPolicySpectraS3Request(name))
        self.assertEqual(deleteResponse.response.status, 204)
        
        # Verify that the data policy no longer exists on the BP
        try:
            self.client.get_data_policy_spectra_s3(GetDataPolicySpectraS3Request(name))
        except RequestFailed as e:
            self.assertEqual(e.code, "NotFound")
    
    def testPutDeleteEmptyStorageDomain(self):
        name = "test_put_delete_empty_storage_domain"
        
        # Create an empty storage domain
        putResponse = self.client.put_storage_domain_spectra_s3(
                    PutStorageDomainSpectraS3Request(name))
        self.assertEqual(putResponse.response.status, 201)
        
        # Verify that the storage domain exits
        getResponse = self.client.get_storage_domain_spectra_s3(
                    GetStorageDomainSpectraS3Request(name))
        self.assertEqual(getResponse.result['Name'], name)
        
        # Delete the storage domain
        deleteResponse = self.client.delete_storage_domain_spectra_s3(
                    DeleteStorageDomainSpectraS3Request(name))
        self.assertEqual(deleteResponse.response.status, 204)
        
        # Verify that the storage domain no longer exists on the BP
        try:
            self.client.get_storage_domain_spectra_s3(
                        GetStorageDomainSpectraS3Request(name))
        except RequestFailed as e:
            self.assertEqual(e.code, "NotFound")
        
    def testPutDeletePoolPartition(self):
        name = "test_put_delete_pool_partition"
        putResponse = self.client.put_pool_partition_spectra_s3(
                    PutPoolPartitionSpectraS3Request(name, "ONLINE"))
        self.assertEqual(putResponse.response.status, 201)
        
        getResponse = self.client.get_pool_partition_spectra_s3(
                    GetPoolPartitionSpectraS3Request(name))
        self.assertEqual(getResponse.result['Name'], name)
        
        deleteResponse = self.client.delete_pool_partition_spectra_s3(
                    DeletePoolPartitionSpectraS3Request(name))
        self.assertEqual(deleteResponse.response.status, 204)
        
        try:
            self.client.get_pool_partition_spectra_s3(
                        GetPoolPartitionSpectraS3Request(name))
        except RequestFailed as e:
            self.assertEqual(e.code, "NotFound")

    def testPutDeletePoolStorageDomainMember(self):
        poolName = "put_delete_pool_storage_domain_member_pool"
        domainName = "put_delete_pool_storage_domain_member_domain"
        
        ids = setupStorageDomainMember(self.client, domainName, poolName)
        
        getResponse = self.client.get_storage_domain_member_spectra_s3(
                    GetStorageDomainMemberSpectraS3Request(ids['MemberId']))
        
        self.assertEqual(getResponse.result['PoolPartitionId'], ids['PoolId'])
        self.assertEqual(getResponse.result['StorageDomainId'], ids['StorageId'])
        
        teardownStorageDomainMember(self.client, ids)
        
        try:
            self.client.get_storage_domain_member_spectra_s3(
                        GetStorageDomainMemberSpectraS3Request(ids['MemberId']))
        except RequestFailed as e:
            self.assertEqual(e.code, "NotFound")
        
    
    def testPutBucketWithDataPolicy(self):
        poolName = "put_bucket_with_data_policy_pool"
        domainName = "put_bucket_with_data_policy_domain"
        policyName = "put_bucket_with_data_policy"
        bucketName = "put_bucket_with_data_policy_bucket"
        
        ids = setupStorageDomainMember(self.client, domainName, poolName)
        
        putPolicyResponse = self.client.put_data_policy_spectra_s3(
                    PutDataPolicySpectraS3Request(policyName))
        
        putRuleResponse = self.client.put_data_persistence_rule_spectra_s3(
                    PutDataPersistenceRuleSpectraS3Request(putPolicyResponse.result['Id'], 
                                                           "STANDARD", 
                                                           ids['StorageId'], 
                                                           "PERMANENT"))
        self.assertEqual(putRuleResponse.response.status, 201)
        
        putBucketResponse = self.client.put_bucket_spectra_s3(
                    PutBucketSpectraS3Request(bucketName, data_policy_id=policyName))
        
        self.assertEqual(putBucketResponse.response.status, 201)
        self.assertEqual(putBucketResponse.result['Name'], bucketName)
        self.assertEqual(putBucketResponse.result['DataPolicyId'], putPolicyResponse.result['Id'])
        
        # Delete test items
        self.client.delete_bucket_spectra_s3(DeleteBucketSpectraS3Request(bucketName))
        
        self.client.delete_data_persistence_rule_spectra_s3(
                    DeleteDataPersistenceRuleSpectraS3Request(putRuleResponse.result['Id']))
        
        self.client.delete_data_policy_spectra_s3(
                    DeleteDataPolicySpectraS3Request(policyName))
        
        teardownStorageDomainMember(self.client, ids)
        
    def testDuplicateObjectsVersioningKeepLatest(self):
        poolName = "duplicate_objects_versioning_keep_latest_pool"
        domainName = "duplicate_objects_versioning_keep_latest_domain"
        policyName = "duplicate_objects_versioning_keep_latest_policy"
        bucketName = "duplicate_objects_versioning_keep_latest_bucket"
        
        ids = setupStorageDomainMember(self.client, domainName, poolName)
        
        putPolicyResponse = self.client.put_data_policy_spectra_s3(
                    PutDataPolicySpectraS3Request(policyName, versioning="KEEP_LATEST"))
        
        putRuleResponse = self.client.put_data_persistence_rule_spectra_s3(
                    PutDataPersistenceRuleSpectraS3Request(putPolicyResponse.result['Id'], 
                                                           "STANDARD", 
                                                           ids['StorageId'], 
                                                           "PERMANENT"))
        
        putBucketResponse = self.client.put_bucket_spectra_s3(
                    PutBucketSpectraS3Request(bucketName, data_policy_id=policyName))
        
        # Load test data and verify they exist on BP
        populateTestData(self.client, bucketName, self.getDataPolicyId(), createBucket=False)
        
        getBucketResponse = self.client.get_bucket(GetBucketRequest(bucketName))
        self.assertEqual(len(getBucketResponse.result['ContentsList']), 4)
        
        # Load test data a second time and verify no errors
        populateTestData(self.client, bucketName, self.getDataPolicyId(), createBucket=False)
        
        getBucketResponse = self.client.get_bucket(GetBucketRequest(bucketName))
        self.assertEqual(len(getBucketResponse.result['ContentsList']), 4)
        
        # Delete test items
        clearBucket(self.client, bucketName)
        
        self.client.delete_data_persistence_rule_spectra_s3(
                    DeleteDataPersistenceRuleSpectraS3Request(putRuleResponse.result['Id']))
        
        self.client.delete_data_policy_spectra_s3(
                    DeleteDataPolicySpectraS3Request(policyName))
        
        teardownStorageDomainMember(self.client, ids)
        
    def testDuplicateObjectsVersioningNone(self):
        poolName = "duplicate_objects_versioning_keep_latest_pool"
        domainName = "duplicate_objects_versioning_keep_latest_domain"
        policyName = "duplicate_objects_versioning_keep_latest_policy"
        bucketName = "duplicate_objects_versioning_keep_latest_bucket"
        
        ids = setupStorageDomainMember(self.client, domainName, poolName)
        
        putPolicyResponse = self.client.put_data_policy_spectra_s3(
                    PutDataPolicySpectraS3Request(policyName, versioning="NONE"))
        
        putRuleResponse = self.client.put_data_persistence_rule_spectra_s3(
                    PutDataPersistenceRuleSpectraS3Request(putPolicyResponse.result['Id'], 
                                                           "STANDARD", 
                                                           ids['StorageId'], 
                                                           "PERMANENT"))
        
        putBucketResponse = self.client.put_bucket_spectra_s3(
                    PutBucketSpectraS3Request(bucketName, data_policy_id=policyName))
        
        # Load test data and verify they exist on BP
        populateTestData(self.client, bucketName, self.getDataPolicyId(), createBucket=False)
        
        getBucketResponse = self.client.get_bucket(GetBucketRequest(bucketName))
        self.assertEqual(len(getBucketResponse.result['ContentsList']), 4)
        
        # Load test data a second time and verify no errors
        try:
            populateTestData(self.client, bucketName, self.getDataPolicyId(), createBucket=False)
        except RequestFailed as e:
            self.assertEqual(e.http_error_code, 409)
            self.assertEqual(e.code, "OBJECT_ALREADY_EXISTS")
        
        # Delete test items
        clearBucket(self.client, bucketName)
        
        self.client.delete_data_persistence_rule_spectra_s3(
                    DeleteDataPersistenceRuleSpectraS3Request(putRuleResponse.result['Id']))
        
        self.client.delete_data_policy_spectra_s3(
                    DeleteDataPolicySpectraS3Request(policyName))
        
        teardownStorageDomainMember(self.client, ids)
    
class SpecialCharacterTestCase(Ds3TestCase):
    def testObjectNameWithSpace(self):
        objectName = "beowulf with spaces.txt"
        fileName = "beowulf.txt"
        
        self.createBucket(bucketName)
        
        localFile = open(pathForResource(fileName), "rb")
        self.client.put_object(PutObjectRequest(bucketName, objectName, 294059L, localFile))
        localFile.close()
        
        getObjectDetails = self.client.get_object_details_spectra_s3(GetObjectDetailsSpectraS3Request(objectName, bucketName))
        self.assertEqual(getObjectDetails.result['Name'], objectName)
        
        fd, tempName = tempfile.mkstemp()
        f = open(tempName, "wb")
        
        getObjectResponse = self.client.get_object(GetObjectRequest(bucketName, objectName, f))
        
        self.assertEqual(getObjectResponse.response.status, 200)
        self.assertEqual(os.stat(tempName).st_size, 294059L)
        
        f.close()
        os.close(fd)
        os.remove(tempName)
        
    def testObjectNameWithSpecialChars(self):
        objectName = "object!@#$%^&*_-+=with()[]{}symbols"
        fileName = "beowulf.txt"
        
        self.createBucket(bucketName)
        
        localFile = open(pathForResource(fileName), "rb")
        self.client.put_object(PutObjectRequest(bucketName, objectName, 294059L, localFile))
        localFile.close()
        
        getObjectDetails = self.client.get_object_details_spectra_s3(GetObjectDetailsSpectraS3Request(objectName, bucketName))
        self.assertEqual(getObjectDetails.result['Name'], objectName)
        
        fd, tempName = tempfile.mkstemp()
        f = open(tempName, "wb")
        
        getObjectResponse = self.client.get_object(GetObjectRequest(bucketName, objectName, f))
        
        self.assertEqual(getObjectResponse.response.status, 200)
        self.assertEqual(os.stat(tempName).st_size, 294059L)
        
        f.close()
        os.close(fd)
        os.remove(tempName)
    
    def testSpecialCharactersInQueryParam(self):
        objectName = "object!@#$%^&*_-+=with()[]{}  symbols"
        fileName = "beowulf.txt"
        
        self.createBucket(bucketName)
        
        localFile = open(pathForResource(fileName), "rb")
        self.client.put_object(PutObjectRequest(bucketName, objectName, 294059L, localFile))
        localFile.close()
        
        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName, marker=objectName))
        self.assertEqual(bucketContents.result['Marker'], objectName)
        
        fd, tempName = tempfile.mkstemp()
        f = open(tempName, "wb")
        
        getObjectResponse = self.client.get_object(GetObjectRequest(bucketName, objectName, f))
        
        self.assertEqual(getObjectResponse.response.status, 200)
        self.assertEqual(os.stat(tempName).st_size, 294059L)
        
        f.close()
        os.close(fd)
        os.remove(tempName)
        
class GroupManagementTestCase(Ds3TestCase):
    def testCreateDeleteGroup(self):
        groupName = "create_delete_group"
        
        createGroup = self.client.put_group_spectra_s3(PutGroupSpectraS3Request(groupName))
        self.assertEqual(createGroup.result['Name'], groupName)
        self.assertEqual(createGroup.response.status, 201)
        
        getGroup = self.client.get_group_spectra_s3(GetGroupSpectraS3Request(groupName))
        self.assertEqual(getGroup.result['Name'], groupName)
        
        deleteGroup = self.client.delete_group_spectra_s3(DeleteGroupSpectraS3Request(groupName))
        self.assertEqual(deleteGroup.response.status, 204)
        
    def testDataPolicyForGroup(self):
        groupName = "data_policy_for_group_Group"
        policyName = "data_policy_for_group_Policy"
        
        createGroup = self.client.put_group_spectra_s3(PutGroupSpectraS3Request(groupName))
        self.assertEqual(createGroup.result['Name'], groupName)
        
        createPolicy = self.client.put_data_policy_spectra_s3(PutDataPolicySpectraS3Request(policyName))
        self.assertEqual(createPolicy.result['Name'], policyName)
        
        createAcl = self.client.put_data_policy_acl_for_group_spectra_s3(
                    PutDataPolicyAclForGroupSpectraS3Request(policyName, groupName))
        self.assertEqual(createAcl.response.status, 201)
        
        getAcl = self.client.get_data_policy_acls_spectra_s3(
                    GetDataPolicyAclsSpectraS3Request(data_policy_id=policyName, group_id=groupName))
        
        aclId = getAcl.result['DataPolicyAclList'][0]['Id']
        
        deleteAcl = self.client.delete_data_policy_acl_spectra_s3(
                    DeleteDataPolicyAclSpectraS3Request(aclId))
        self.assertEqual(deleteAcl.response.status, 204)
        
        deleteGroup = self.client.delete_group_spectra_s3(DeleteGroupSpectraS3Request(groupName))
        self.assertEqual(deleteGroup.response.status, 204)
        
        deletePolicy = self.client.delete_data_policy_spectra_s3(
                    DeleteDataPolicySpectraS3Request(policyName))
        self.assertEqual(deletePolicy.response.status, 204)
        
    def testGroupGroupMember(self):
        parentName = "create_group_group_member_Parent"
        childName = "create_group_group_member_Child"
        
        createParent = self.client.put_group_spectra_s3(PutGroupSpectraS3Request(parentName))
        self.assertEqual(createParent.result['Name'], parentName)
        
        createChild = self.client.put_group_spectra_s3(PutGroupSpectraS3Request(childName))
        self.assertEqual(createChild.result['Name'], childName)
        
        parentId = createParent.result['Id']
        childId = createChild.result['Id']
        
        createGroupGroup = self.client.put_group_group_member_spectra_s3(
                    PutGroupGroupMemberSpectraS3Request(group_id=parentId, member_group_id=childId))
        self.assertEqual(createGroupGroup.response.status, 201)
        self.assertEqual(createGroupGroup.result['GroupId'], parentId)
        self.assertEqual(createGroupGroup.result['MemberGroupId'], childId)
        
        deleteGroupGroup = self.client.delete_group_member_spectra_s3(
                    DeleteGroupMemberSpectraS3Request(createGroupGroup.result['Id']))
        self.assertEqual(deleteGroupGroup.response.status, 204)
        
        getGroup = self.client.get_group_members_spectra_s3(
                    GetGroupMembersSpectraS3Request(parentId))
        
        deleteGroup = self.client.delete_group_spectra_s3(DeleteGroupSpectraS3Request(childName))
        self.assertEqual(deleteGroup.response.status, 204)
        
        deleteGroup = self.client.delete_group_spectra_s3(DeleteGroupSpectraS3Request(parentName))
        self.assertEqual(deleteGroup.response.status, 204)
        
    def testBucketAclForGroup(self):
        groupName = "bucket_acl_for_group"
        permission = "READ"
        
        # Create bucket and group
        self.createBucket(bucketName)
        
        createGroup = self.client.put_group_spectra_s3(PutGroupSpectraS3Request(groupName))
        self.assertEqual(createGroup.result['Name'], groupName)
        
        # Create acl between bucket and group
        createAcl = self.client.put_bucket_acl_for_group_spectra_s3(
                    PutBucketAclForGroupSpectraS3Request(bucketName, groupName, permission))
        
        # Verify that acl exists
        getAcls = self.client.get_bucket_acls_spectra_s3(
                    GetBucketAclsSpectraS3Request(bucket_id=bucketName, group_id=groupName))
        self.assertEqual(len(getAcls.result['BucketAclList']), 1)
        self.assertEqual(getAcls.result['BucketAclList'][0]['Permission'], permission)
        
        # Delete the acl
        deleteAcl = self.client.delete_bucket_acl_spectra_s3(
                    DeleteBucketAclSpectraS3Request(createAcl.result['Id']))
        self.assertEqual(deleteAcl.response.status, 204)
        
        # Verify the acl was deleted
        getAcls = self.client.get_bucket_acls_spectra_s3(
                    GetBucketAclsSpectraS3Request(bucket_id=bucketName, group_id=groupName))
        self.assertEqual(len(getAcls.result['BucketAclList']), 0)
        
        # Cleanup
        deleteGroup = self.client.delete_group_spectra_s3(DeleteGroupSpectraS3Request(groupName))
        self.assertEqual(deleteGroup.response.status, 204)
        
class NotificationsTestCase(Ds3TestCase):
    def testObjectCompletionRegistration(self):
        response = self.client.put_object_cached_notification_registration_spectra_s3(
                    PutObjectCachedNotificationRegistrationSpectraS3Request("192.168.56.101"))
        self.assertTrue(response.result['Id'])
        
        registrationId = response.result['Id']
        
        getResponse = self.client.get_object_cached_notification_registration_spectra_s3(
                    GetObjectCachedNotificationRegistrationSpectraS3Request(registrationId))
        
        self.assertEqual(getResponse.result['Id'], registrationId)
        
        deleteResponse = self.client.delete_object_cached_notification_registration_spectra_s3(
                    DeleteObjectCachedNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(deleteResponse.response.status, 204)
        
    def testCompletionRegistration(self):
        response = self.client.put_job_completed_notification_registration_spectra_s3(
                    PutJobCompletedNotificationRegistrationSpectraS3Request("192.168.56.101/other"))
        self.assertTrue(response.result['Id'])
        
        registrationId = response.result['Id']
        
        getResponse = self.client.get_job_completed_notification_registration_spectra_s3(
                    GetJobCompletedNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(getResponse.response.status, 200)
        
        deleteResponse = self.client.delete_job_completed_notification_registration_spectra_s3(
                    DeleteJobCompletedNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(deleteResponse.response.status, 204)
        
    def testJobCreateRegistration(self):
        response = self.client.put_job_created_notification_registration_spectra_s3(
                    PutJobCreatedNotificationRegistrationSpectraS3Request("192.168.56.101/other"))
        self.assertTrue(response.result['Id'])
        
        registrationId = response.result['Id']
        
        getResponse = self.client.get_job_created_notification_registration_spectra_s3(
                    GetJobCreatedNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(getResponse.response.status, 200)
        
        deleteResponse = self.client.delete_job_created_notification_registration_spectra_s3(
                    DeleteJobCreatedNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(deleteResponse.response.status, 204)
        
    def testObjectLostRegistration(self):
        response = self.client.put_object_lost_notification_registration_spectra_s3(
                    PutObjectLostNotificationRegistrationSpectraS3Request("192.168.56.101/other"))
        self.assertTrue(response.result['Id'])
        
        registrationId = response.result['Id']
        
        getResponse = self.client.get_object_lost_notification_registration_spectra_s3(
                    GetObjectLostNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(getResponse.response.status, 200)
        
        deleteResponse = self.client.delete_object_lost_notification_registration_spectra_s3(
                    DeleteObjectLostNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(deleteResponse.response.status, 204)
        
    def testPartitionFailureRegistration(self):
        response = self.client.put_tape_partition_failure_notification_registration_spectra_s3(
                    PutTapePartitionFailureNotificationRegistrationSpectraS3Request("192.168.56.101/other"))
        self.assertTrue(response.result['Id'])
        
        registrationId = response.result['Id']
        
        getResponse = self.client.get_tape_partition_failure_notification_registration_spectra_s3(
                    GetTapePartitionFailureNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(getResponse.response.status, 200)
        
        deleteResponse = self.client.delete_tape_partition_failure_notification_registration_spectra_s3(
                    DeleteTapePartitionFailureNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(deleteResponse.response.status, 204)
        
    def testTapeFailureRegistration(self):
        response = self.client.put_tape_failure_notification_registration_spectra_s3(
                    PutTapeFailureNotificationRegistrationSpectraS3Request("192.168.56.101/other"))
        self.assertTrue(response.result['Id'])
        
        registrationId = response.result['Id']
        
        getResponse = self.client.get_tape_failure_notification_registration_spectra_s3(
                    GetTapeFailureNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(getResponse.response.status, 200)
        
        deleteResponse = self.client.delete_tape_failure_notification_registration_spectra_s3(
                    DeleteTapeFailureNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(deleteResponse.response.status, 204)
        
    def testObjectPersistedRegistration(self):
        def getSize(fileName):
            size = os.stat(pathForResource(fileName)).st_size
            return FileObject(fileName, size)

        # Create bulk put
        self.createBucket(bucketName)

        pathes = {fileName: pathForResource(fileName) for fileName in resources}

        fileList = map(getSize, resources)
        fileObjectList = FileObjectList(fileList)

        bulkResult = self.client.put_bulk_job_spectra_s3(PutBulkJobSpectraS3Request(bucketName, fileObjectList))
        bulkJobId = bulkResult.result['JobId']
        
        # Register the notification
        response = self.client.put_object_persisted_notification_registration_spectra_s3(
                    PutObjectPersistedNotificationRegistrationSpectraS3Request("192.168.56.101/other", job_id=bulkJobId))
        self.assertEqual(response.response.status, 201)
        
        # Transfer data
        for chunk in bulkResult.result['ObjectsList']:
            allocateChunk = self.client.allocate_job_chunk_spectra_s3(AllocateJobChunkSpectraS3Request(chunk['ChunkId']))
            for obj in allocateChunk.result['ObjectList']:
                fileName = pathes[obj['Name']]
                fileSize = obj['Length']
                localFileStream = open(fileName, "rb")
                self.client.put_object(PutObjectRequest(bucketName, obj['Name'], fileSize, localFileStream, offset=int(obj['Offset']), job=bulkJobId))
                localFileStream.close()
            
        # Verify notification and then delete
        registrationId = response.result['Id']
        
        getResponse = self.client.get_object_persisted_notification_registration_spectra_s3(
                    GetObjectPersistedNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(getResponse.response.status, 200)
        self.assertEqual(getResponse.result['JobId'], bulkJobId)
        
        deleteResponse = self.client.delete_object_persisted_notification_registration_spectra_s3(
                    DeleteObjectPersistedNotificationRegistrationSpectraS3Request(registrationId))
        self.assertEqual(deleteResponse.response.status, 204)
        
class MetadataTestCase(Ds3TestCase):
    def testPutObjectRequestWithMetadata(self):
        metadata = {"name1":"value1", "name2":"", "name3":None}
        expected_metadata = {"name1":"value1", "Content-Length":100}
        
        fd, tempname = tempfile.mkstemp()
        
        request = PutObjectRequest(bucketName, "beowulf.txt", 100, fd, headers=metadata)
        self.assertEqual(expected_metadata, request.headers)
        
        os.close(fd)