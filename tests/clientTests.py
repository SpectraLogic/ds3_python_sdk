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

def populateTestData(client, bucketName, resourceList = None, prefix = "", metadata = None, createBucket=True):
    if not resourceList:
        resourceList = resources

    def getSize(fileName):
        size = os.stat(pathForResource(fileName)).st_size
        return FileObject(prefix + fileName, size)

    if createBucket:
        client.put_bucket(PutBucketRequest(bucketName))

    pathes = {prefix + fileName: pathForResource(fileName) for fileName in resourceList}

    fileList = map(getSize, resourceList)
    fileObjectList = FileObjectList(fileList)

    bulkResult = client.put_bulk_job_spectra_s3(PutBulkJobSpectraS3Request(bucketName, fileObjectList))

    for chunk in bulkResult.result['ObjectsList']:
        allocateChunk = client.allocate_job_chunk_spectra_s3(AllocateJobChunkSpectraS3Request(chunk['ChunkId']))
        for obj in allocateChunk.result['ObjectList']:
            client.put_object(PutObjectRequest(bucketName, obj['Name'], offset=int(obj['Offset']), real_file_name=pathes[obj['Name']], job=bulkResult.result['JobId'], headers=metadata))
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

class Ds3TestCase(unittest.TestCase):
    def setUp(self):
        self.client = createClientFromEnv()

    def tearDown(self):
        try:
            clearBucket(self.client, bucketName)
        except RequestFailed as e:
            pass
        
    def checkBadInputs(self, testFunction, inputs):
        for test_input, status in inputs.items():
            try:
                testFunction(test_input)
            except status[0] as e:
                self.assertEqual(status[1](e), status[2])
                    
class BucketTestCase(Ds3TestCase):
    def testPutBucket(self):
        """tests putBucket"""
        self.client.put_bucket(PutBucketRequest(bucketName))

        getService = self.client.get_service(GetServiceRequest())
        self.assertEqual(getService.response.status, 200)
        bucketSet = frozenset(map(lambda service: service['Name'], getService.result['BucketList']))

        self.assertTrue(bucketName in bucketSet)
        
    def testPutBucketUnicode(self):
        """tests putBucket"""
        self.client.put_bucket(PutBucketRequest(unicode(bucketName)))

        getService = self.client.get_service(GetServiceRequest())
        self.assertEqual(getService.response.status, 200)
        bucketSet = frozenset(map(lambda service: service['Name'], getService.result['BucketList']))

        self.assertTrue(bucketName in bucketSet)
        
    def testPutBucketBadInput(self):
        """tests putBucket: bad input to function"""
        self.client.put_bucket(PutBucketRequest(bucketName))
        badBuckets = {PutBucketRequest(""): statusCodeList(400), PutBucketRequest(bucketName): statusCodeList(409)}
        self.checkBadInputs(self.client.put_bucket, badBuckets)

    def testDeleteEmptyBucket(self):
        """tests deleteBucket: deleting an empty bucket"""
        self.client.put_bucket(PutBucketRequest(bucketName))

        self.client.delete_bucket(DeleteBucketRequest(bucketName))

        getService = self.client.get_service(GetServiceRequest())
        bucketSet = frozenset(map(lambda service: service['Name'], getService.result['BucketList']))
        self.assertFalse(bucketName in bucketSet)
        
    def testDeleteBucketBadInput(self):
        """tests deleteBucket: bad input to function"""
        populateTestData(self.client, bucketName)
        
        badBuckets = {DeleteBucketRequest(""): statusCodeList(400), DeleteBucketRequest(bucketName): statusCodeList(409), DeleteBucketRequest("not-here"): statusCodeList(404)}
        self.checkBadInputs(self.client.delete_bucket, badBuckets)
            
    def testGetEmptyBucket(self):
        """tests getBucket: when bucket is empty"""
        self.client.put_bucket(PutBucketRequest(bucketName))

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
        fileList = populateTestData(self.client, bucketName, resourceList = unicodeResources)

    def testGetFilledBucket(self):
        """tests getBucket: when bucket has contents"""
        fileList = populateTestData(self.client, bucketName)

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
        populateTestData(self.client, bucketName)

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName, prefix = "beo"))

        self.assertEqual(len(bucketContents.result['ContentsList']), 1)

    def testPagination(self):
        """tests getBucket: maxKeys parameter, getBucket: nextMarker parameter"""
        fileList = []
        for i in xrange(0, 15):
            fileList.append(FileObject("file" + str(i), 0))

        self.client.put_bucket(PutBucketRequest(bucketName))
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

        self.client.put_bucket(PutBucketRequest(bucketName))

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
        
        self.client.put_bucket(PutBucketRequest(bucketName))
        
        afterResponse = self.client.get_service(GetServiceRequest())
        servicesAfter = map(lambda service: service['Name'], afterResponse.result['BucketList'])
        self.assertTrue(bucketName in servicesAfter)
        
    def testHeadBucket(self):
        self.client.put_bucket(PutBucketRequest(bucketName))
        self.client.head_bucket(HeadBucketRequest(bucketName))
        
    def testHeadBucketBadInput(self):
        badBuckets = {HeadBucketRequest(""): statusCodeList(400), HeadBucketRequest("not-here"): statusCodeList(404)}
        self.checkBadInputs(self.client.head_bucket, badBuckets)

class JobTestCase(Ds3TestCase):
    def testGetJobs(self):
        populateTestData(self.client, bucketName)
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
        fileList = populateTestData(self.client, bucketName, resourceList = [fileName])
        
        self.assertEqual(len(fileList), 1)
        self.assertEqual(fileList[0].name, fileName)
        self.assertEqual(fileList[0].size, 301063L)
        
        fd, tempname = tempfile.mkstemp()
        
        getObjectResult = self.client.get_object(GetObjectRequest(bucketName, fileName, real_file_name=tempname))
        self.assertEqual(getObjectResult.response.status, 200)
        self.assertEqual(os.stat(tempname).st_size, 301063L)
        
        os.close(fd)
        os.remove(tempname)
        
    def testGetAndPutObjectStream(self):
        self.client.put_bucket(PutBucketRequest(bucketName))
        
        fileName = "beowulf.txt"
        localFile = open(pathForResource(fileName), "rb")
        self.client.put_object(PutObjectRequest(bucketName, fileName, stream=localFile))
        localFile.close()
        
        fd, tempname = tempfile.mkstemp()
        f = open(tempname, "wb")
        
        getObjectResult = self.client.get_object(GetObjectRequest(bucketName, fileName, stream=f))
        self.assertEqual(getObjectResult.response.status, 200)
        self.assertEqual(os.stat(tempname).st_size, 301063L)
        
        f.close()
        os.close(fd)
        os.remove(tempname)
    
    def testDeleteObject(self):
        """tests deleteObject: when object exists"""
        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"])

        self.client.delete_object(DeleteObjectRequest(bucketName, "beowulf.txt"))
        
        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(len(bucketContents.result['ContentsList']), 0)

    def testDeleteObjectUnicode(self):
        """tests deleteObject: unicode parameter"""
        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"])

        self.client.delete_object(DeleteObjectRequest(bucketName, unicode("beowulf.txt")))
        
        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(len(bucketContents.result['ContentsList']), 0)
        
    def testDeleteObjectBadInput(self):
        """tests deleteObject: bad input to function"""
        self.client.put_bucket(PutBucketRequest(bucketName))
        
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
        fileList = populateTestData(self.client, bucketName)

        deleteFiles = DeleteObjectList(map(lambda obj: DeleteObject(obj.name), fileList))
        
        deletedResponse = self.client.delete_objects(DeleteObjectsRequest(bucketName, deleteFiles))

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(len(bucketContents.result['ContentsList']), 0)

    def testDeleteObjectsUnicode(self):
        """tests deleteObjects: unicode parameter"""
        fileList = populateTestData(self.client, bucketName)

        deleteList = DeleteObjectList(map(lambda obj: DeleteObject(obj.name), fileList))
        deletedResponse = self.client.delete_objects(DeleteObjectsRequest(bucketName, deleteList))

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))

        self.assertEqual(len(bucketContents.result['ContentsList']), 0)
        
    def testDeleteObjectsEmpty(self):
        """tests deleteObjects: when list passed is empty"""
        self.client.put_bucket(PutBucketRequest(bucketName))
        try:
            self.client.delete_objects(DeleteObjectsRequest(bucketName, DeleteObjectList([])))
        except RequestFailed as e:
            self.assertEqual(e.message, "The bulk command requires a list of objects to process")
        
    def testDeleteBadObjects(self):
        """tests deleteObjects: when bucket is empty"""
        self.client.put_bucket(PutBucketRequest(bucketName))

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
        populateTestData(self.client, bucketName)
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
        populateTestData(self.client, bucketName)
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
        populateTestData(self.client, bucketName, prefix = "folder/")

        self.client.delete_folder_recursively_spectra_s3(DeleteFolderRecursivelySpectraS3Request(bucketName, "folder"))
        
        bucketResult = self.client.get_bucket(GetBucketRequest(bucketName))
        
        self.assertEqual(len(bucketResult.result['ContentsList']), 0)
        
    def testDeleteFolderBadInput(self):
        """tests deleteFolder"""
        self.client.put_bucket(PutBucketRequest(bucketName))
        folder = "folder"
        badBuckets = {DeleteFolderRecursivelySpectraS3Request("", folder): statusCodeList(500),
                      DeleteFolderRecursivelySpectraS3Request("fakeBucket", folder): statusCodeList(404), 
                      DeleteFolderRecursivelySpectraS3Request(bucketName, folder): statusCodeList(404)}
        self.checkBadInputs(self.client.delete_folder_recursively_spectra_s3, badBuckets)

    def testGetObjects(self):
        populateTestData(self.client, bucketName)

        objects = self.client.get_objects_spectra_s3(GetObjectsSpectraS3Request())

        self.validateSearchObjects(objects.result['S3ObjectList'], resources)
            
    def testGetObjectsBucketName(self):
        populateTestData(self.client, bucketName)

        objects = self.client.get_objects_spectra_s3(GetObjectsSpectraS3Request(bucket_id = bucketName))

        self.validateSearchObjects(objects.result['S3ObjectList'], resources)
            
    def testGetObjectsObjectName(self):
        populateTestData(self.client, bucketName)

        objects = self.client.get_objects_spectra_s3(GetObjectsSpectraS3Request(bucket_id = bucketName, name = "beowulf.txt"))
        
        self.validateSearchObjects(objects.result['S3ObjectList'], ["beowulf.txt"])
            
    def testGetObjectsPageParameters(self):
        populateTestData(self.client, bucketName)

        first_half = self.client.get_objects_spectra_s3(GetObjectsSpectraS3Request(bucket_id = bucketName, page_length = 2))
        self.assertEqual(len(first_half.result['S3ObjectList']), 2)
        second_half = self.client.get_objects_spectra_s3(GetObjectsSpectraS3Request(bucket_id = bucketName, page_length = 2, page_offset = 2))
        self.assertEqual(len(second_half.result['S3ObjectList']), 2)
        
        self.validateSearchObjects(first_half.result['S3ObjectList']+second_half.result['S3ObjectList'], resources)
            
    def testGetObjectsType(self):
        populateTestData(self.client, bucketName)

        dataResponse = self.client.get_objects_spectra_s3(GetObjectsSpectraS3Request(bucket_id = bucketName, type = "DATA"))
        objects = dataResponse.result['S3ObjectList']
        
        self.validateSearchObjects(objects, resources)

        folderResponse = self.client.get_objects_spectra_s3(GetObjectsSpectraS3Request(bucket_id = bucketName, type = "FOLDER"))
        objects = folderResponse.result['S3ObjectList']
        
        self.validateSearchObjects(objects, [], objType = "FOLDER")
            
    def testGetObjectsVersion(self):
        populateTestData(self.client, bucketName)

        response = self.client.get_objects_spectra_s3(GetObjectsSpectraS3Request(bucket_id = bucketName, version = 1))
        objects = response.result['S3ObjectList']
        
        self.validateSearchObjects(objects, resources)
                
    def testGetBulkUnicode(self):
        """tests getObject: unicode parameter"""
        populateTestData(self.client, bucketName, resourceList = unicodeResources)

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))
        
        objects = FileObjectList(map(lambda obj: FileObject(unicode(obj['Key'])), bucketContents.result['ContentsList']))
        bulkGetResult = self.client.get_bulk_job_spectra_s3(GetBulkJobSpectraS3Request(bucketName, objects))
        
        tempFiles = []
        
        availableChunks = self.client.get_job_chunk_spectra_s3(GetJobChunkSpectraS3Request(bulkGetResult.result['JobId']))
        
        for obj in availableChunks.result['ObjectList']:
            newFile = tempfile.mkstemp()
            tempFiles.append(newFile)

            metadata_resp = self.client.get_object(GetObjectRequest(bucketName, obj['Name'], offset = int(obj['Offset']), job = bulkGetResult.result['JobId'], real_file_name = newFile[1]))
        
        for tempFile in tempFiles:
            os.close(tempFile[0])
            os.remove(tempFile[1])

        #jobStatusResponse = self.client.getJob(bulkGetResult.jobId)
        #self.assertEqual(jobStatusResponse.status, LibDs3JobStatus.COMPLETED)
    
class ObjectMetadataTestCase(Ds3TestCase):
    def testHeadObject(self):
        """tests headObject"""
        metadata = {"name1":["value1"], "name2":"value2", "name3":("value3")}
        metadata_check = {"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"], metadata = metadata)

        metadata_resp = self.client.head_object(HeadObjectRequest(bucketName, "beowulf.txt"))
        
        self.assertEqual('EXISTS', metadata_resp.result)
        self.assertEqual(metadata_check, metadata_resp.meta_data)

    def testHeadObjectBadInput(self):
        """tests headObject: bad input to function"""
        metadata = {"name1":["value1"], "name2":"value2", "name3":("value3")}

        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"], metadata = metadata)

        badBuckets = {HeadObjectRequest("fakeBucket", ""): reasonErrorList("Reason: The object name parameter is required."),
                      HeadObjectRequest("fakeBucket", "badFile"): statusCodeList(404),
                      HeadObjectRequest(bucketName, ""): reasonErrorList("Reason: The object name parameter is required."),
                      HeadObjectRequest(bucketName, "badFile"): statusCodeList(404),
                      HeadObjectRequest("", "badFile"): reasonErrorList("Reason: The bucket name parameter is required.")}
        self.checkBadInputs(self.client.head_object, badBuckets)
                
    def testGetBulkWithMetadata(self):
        """tests getObject: metadata parameter, putObject:metadata parameter"""
        metadata = {"name1":["value1"], "name2":["value2"], "name3":["value3"]}

        populateTestData(self.client, bucketName, resourceList = ["beowulf.txt"], metadata = metadata)

        bucketContents = self.client.get_bucket(GetBucketRequest(bucketName))
        
        objects = FileObjectList(map(lambda obj: FileObject(obj['Key']), bucketContents.result['ContentsList']))
        bulkGetResult = self.client.get_bulk_job_spectra_s3(GetBulkJobSpectraS3Request(bucketName, objects))
        
        tempFiles = []
        
        availableChunks = self.client.get_job_chunk_spectra_s3(GetJobChunkSpectraS3Request(bulkGetResult.result['JobId']))
        
        for obj in availableChunks.result['ObjectList']:
            newFile = tempfile.mkstemp()
            tempFiles.append(newFile)

            metadata_resp = self.client.get_object(GetObjectRequest(bucketName, obj['Name'], offset = int(obj['Offset']), job = bulkGetResult.result['JobId'], real_file_name = newFile[1]))
        
        for tempFile in tempFiles:
            os.close(tempFile[0])
            os.remove(tempFile[1])

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
        populateTestData(self.client, bucketName, createBucket=False)
        
        getBucketResponse = self.client.get_bucket(GetBucketRequest(bucketName))
        self.assertEqual(len(getBucketResponse.result['ContentsList']), 4)
        
        # Load test data a second time and verify no errors
        populateTestData(self.client, bucketName, createBucket=False)
        
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
        populateTestData(self.client, bucketName, createBucket=False)
        
        getBucketResponse = self.client.get_bucket(GetBucketRequest(bucketName))
        self.assertEqual(len(getBucketResponse.result['ContentsList']), 4)
        
        # Load test data a second time and verify no errors
        try:
            populateTestData(self.client, bucketName, createBucket=False)
        except RequestFailed as e:
            self.assertEqual(e.http_error_code, 409)
            self.assertEqual(e.code, "CONFLICT")
        
        # Delete test items
        clearBucket(self.client, bucketName)
        
        self.client.delete_data_persistence_rule_spectra_s3(
                    DeleteDataPersistenceRuleSpectraS3Request(putRuleResponse.result['Id']))
        
        self.client.delete_data_policy_spectra_s3(
                    DeleteDataPolicySpectraS3Request(policyName))
        
        teardownStorageDomainMember(self.client, ids)

def normalizePath(url):
    return urllib.quote(url)
    
class SpecialCharacterTestCase(Ds3TestCase):
    def testObjectNameWithSpace(self):
        bucketName = "test_name_with_space"
        objectName = "beowulf with spaces.txt"
        fileName = "beowulf.txt"
        
        self.client.put_bucket(PutBucketRequest(bucketName))
        
        localFile = open(pathForResource(fileName), "rb")
        self.client.put_object(PutObjectRequest(bucketName, objectName, stream=localFile))
        localFile.close()
        
        getObjectSpectra = self.client.get_object_spectra_s3(GetObjectSpectraS3Request(objectName, bucketName))
        self.assertEqual(getObjectSpectra.result['Name'], objectName)
        
        fd, tempName = tempfile.mkstemp()
        
        getObjectResponse = self.client.get_object(GetObjectRequest(bucketName, objectName, real_file_name=tempName))
        
        self.assertEqual(getObjectResponse.response.status, 200)
        self.assertEqual(os.stat(tempName).st_size, 301063L)
        
        os.close(fd)
        
        clearBucket(self.client, bucketName)
        
    def testObjectNameWithSpecialChars(self):
        bucketName = "test_name_with_space"
        objectName = "object!@#$%^&*_-+=with()[]{}symbols"
        fileName = "beowulf.txt"
        
        self.client.put_bucket(PutBucketRequest(bucketName))
        
        localFile = open(pathForResource(fileName), "rb")
        self.client.put_object(PutObjectRequest(bucketName, objectName, stream=localFile))
        localFile.close()
        
        getObjectSpectra = self.client.get_object_spectra_s3(GetObjectSpectraS3Request(objectName, bucketName))
        self.assertEqual(getObjectSpectra.result['Name'], objectName)
        
        fd, tempName = tempfile.mkstemp()
        
        getObjectResponse = self.client.get_object(GetObjectRequest(bucketName, objectName, real_file_name=tempName))
        
        self.assertEqual(getObjectResponse.response.status, 200)
        self.assertEqual(os.stat(tempName).st_size, 301063L)
        
        os.close(fd)
        
        clearBucket(self.client, bucketName)
        