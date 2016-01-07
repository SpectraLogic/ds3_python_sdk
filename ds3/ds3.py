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

from ctypes import *
import libds3

def checkExistence(obj, wrapper = lambda ds3Str: ds3Str.contents.value, defaultReturnValue = None):
    if obj:
        return wrapper(obj)
    else:
        return defaultReturnValue

def arrayToList(array, length, wrapper = lambda ds3Str: ds3Str.contents.value):
    result = []
    for i in xrange(0, length):
        result.append(wrapper(array[i]))
    return result

class Ds3Error(Exception):
    """Returns an exception to the client. Attributes:

    reason (string):  error contents message
    response (string): error contents error
    if(has_response == true)
        statusCode (int): http return value

        statusMessage (string): http return status_message

        message (string): error body

    Cast to string for description.
    """
    def __init__(self, libds3Error):
        self.reason = libds3Error.contents.message.contents.value
        response = libds3Error.contents.error
        self._hasResponse = False
        self.statusCode = None
        self.statusMessage = None
        self.message = None
        if response:
            self._hasResponse = True
            self.statusCode = response.contents.status_code
            self.statusMessage = response.contents.status_message.contents.value
            self.message = checkExistence(response.contents.error_body)
        libds3.lib.ds3_free_error(libds3Error)
    def __str__(self):
        errorMessage = "Reason: " + self.reason
        if self._hasResponse:
            errorMessage += " | StatusCode: " + str(self.statusCode)
            errorMessage += " | StatusMessage: " + self.statusMessage
            if self.message:
                errorMessage += " | Message: " + self.message

        return errorMessage
    def __repr__(self):
        return self.__str__()

class Credentials(object):
    """Credential object to build client

    Construct with (accessKey, secretKey) for target device or build client from environment variables    
    """    
    def __init__(self, accessKey, secretKey):
        self.accessKey = accessKey
        self.secretKey = secretKey

class Ds3Bucket(object):
    """Descibes a Bucket (name and creationDate)

    Members:
        name (string) : The name of the bucket.

        creationDate (date) : The date and time the bucket was created in the format YYYY-MM-DDThh:mm:ss.xxxZ.
  
    Cast to string for description.

    """
    def __init__(self, ds3Bucket):
        self.name = ds3Bucket.name.contents.value
        self.creationDate = ds3Bucket.creation_date.contents.value
    def __str__(self):
        return "Name: " + self.name + " | Creation Date: " + self.creationDate
    def __repr__(self):
        return self.__str__()

class Ds3Owner(object):
    """Describes an object owner (name and id)

    Members:
        name (string) : The name of the owner.

        id (string) : The UUID of the object owner.
  
    Cast to string for description.

    """
    def __init__(self, ds3Owner):
        ownerContents = ds3Owner.contents
        self.name = ownerContents.name.contents.value
        self.id = ownerContents.id.contents.value
    def __str__(self):
        return "Name: " + self.name + " | ID: " + self.id
    def __repr__(self):
        return self.__str__()

class Ds3Object(object):
    """Describes a Object

    Members:
        name (string) : The object name

        etag (string) : The http entity tag.

        size (long) : The size of the object in bytes.

        owner (Ds3Owner) : The owner of the object.

    Cast to string for description.

    """
    def __init__(self, ds3Object):
        self.name = ds3Object.name.contents.value
        self.etag = checkExistence(ds3Object.etag)
        self.size = ds3Object.size
        self.owner = Ds3Owner(ds3Object.owner)
    def __str__(self):
        return "Name: " + self.name + " | Size: " + str(self.size) + " | Etag: " + str(self.etag) + " | Owner: " + str(self.owner)
    def __repr__(self):
        return self.__str__()

class Ds3BucketDetails(object):
    """Response for ListObjects (Get Bucket)

    Members:

        commonPrefixes (List<string>) : If a delimiter is specified, contains the portion of an object's name between the prefix and the next occurrence of the delimiter.

        creationDate (string) : The date and time the bucket was created in the format YYYY-MM-DDThh:mm:ss.xxxZ.

        delimiter (string) : The character used to group object names.

        isTruncated (bool) : Specifies whether the results were truncated (true) or not (false) due to the number of results exceeding MaxKeys. 

        marker (string) : The object name where the bucket listing begins. Included in the response if it was specified in the request.

        maxKeys (int) : The maximum number of keys (object names) returned in the response.

        name (string) : The name of the bucket.

        nextMarker (string) : If the delimiter parameter was specified, and isTruncated is true, indicates the object name to use in the marker field in the next request to get the next set of objects. 

        objects (List<Ds3Objects>) : Bucket contents matching search criteria

        prefix (string) : The string used to limit the response keys. Only object names that begin with the specified prefix are listed.

        size (long) : The size of the object in bytes.

    Cast to string for description.
    """
    def __init__(self, ds3Bucket):
        bucketContents = ds3Bucket.contents
        self.name = bucketContents.name.contents.value
        self.creationDate = checkExistence(bucketContents.creation_date)

        self.isTruncated = bool(bucketContents.is_truncated)
        self.marker = checkExistence(bucketContents.marker)
        self.delimiter = checkExistence(bucketContents.delimiter)
        self.maxKeys = bucketContents.max_keys
        self.nextMarker = checkExistence(bucketContents.next_marker)
        self.prefix = checkExistence(bucketContents.prefix)
        self.commonPrefixes = arrayToList(bucketContents.common_prefixes, bucketContents.num_common_prefixes)
        self.objects = arrayToList(bucketContents.objects, bucketContents.num_objects, wrapper = Ds3Object)

class Ds3BulkObject(object):
    """Object description from bulk response

    Members:
        name (string) : The object name

        length (long) : The length in bytes of the object or part of the object. 

        offset (long) : The offset in bytes from the start of the object.

        inCache (bool) : Indicates if the object is currently in cache on the BlackPearl Deep Storage Gateway.

    Cast to string for description.

    """
    def __init__(self, bulkObject):
        self.name = bulkObject.name.contents.value
        self.length = bulkObject.length
        self.offset = bulkObject.offset
        self.inCache = bool(bulkObject.in_cache)
    def __str__(self):
        return "Name:" + self.name + " | Length: " + str(self.length) + " | Offset: " + str(self.offset) + " | InCache: " + str(self.inCache)
    def __repr__(self):
        return self.__str__()

class Ds3CacheList(object):
    """Collection of chunks to process.

    Members:

        chunkId (string) : The UUID for the job chunk.

        chunkNumber (string) : The position of the chunk within the job.

        nodeId (string) : The UUID for the BlackPearl node.

        objects (List<Ds3BulkObject>) : Container for information about the objects.
    """
    def __init__(self, bulkObjectList):
        contents = bulkObjectList.contents
        self.chunkNumber = contents.chunk_number
        self.nodeId = checkExistence(contents.node_id)
        self.serverId = checkExistence(contents.server_id)
        self.chunkId = contents.chunk_id.contents.value
        self.objects = arrayToList(contents.list, contents.size, wrapper = Ds3BulkObject)

class Ds3BulkPlan(object):
    """Collection of job chunks and associated parameters.

    Members:
        startDate (string) : The date and time the job was started in the format YYYY-MM-DDThh:mm:ss.xxxZ.

        userId (string) : The UUID for the user who initiated the job.

        userName (string) : The username of the user who initiated the job.

        requestType (string) : Specifies whether job chunks are written as quickly as possible (PERFORMANCE) or across as few tapes as possible (CAPACITY). Values: CAPACITY, PERFORMANCE,

        status (string) : Values COMPLETED, CANCELLED, IN_PROGRESS

        cachedSize (long) : The amount of data successfully transferred to the BlackPearl Deep Storage Gateway from the client. 

        completedSize (long) : The amount of data written to tape media.

        originalSize (long) : The amount of data for the job to transfer.

        jobId (string) : The UUID for the job.

        chunks (Ds3CacheList) : list of chunks to process.

    Cast to string for description.
    """
    def __init__(self, ds3BulkResponse):
        contents = ds3BulkResponse.contents
        self.bucketName = checkExistence(contents.bucket_name)
        self.cachedSize = checkExistence(contents.cached_size_in_bytes, 0)
        self.completedSize = checkExistence(contents.completed_size_in_bytes, 0)
        self.jobId = checkExistence(contents.job_id)
        self.originalSize = checkExistence(contents.original_size_in_bytes, 0)
        self.startDate = checkExistence(contents.start_date)
        self.userId = checkExistence(contents.user_id)
        self.userName = checkExistence(contents.user_name)
        self.requestType = contents.request_type
        self.status = contents.status
        self.chunks = arrayToList(contents.list, contents.list_size, wrapper = Ds3CacheList)
    def __str__(self):
        response = "JobId: " + self.jobId
        response += " | Status: " + str(self.status)
        response += " | Request Type: " + str(self.requestType)
        response += " | BucketName: " + self.bucketName
        response += " | UserName: " + self.userName
        response += " | Chunks: " + str(self.chunks)
        return response
    def __repr__(self):
        return self.__str__()

class Ds3AllocateChunkResponse(object):
    """This class has been deprecated
    """
    def __init__(self, ds3AllocateChunkResponse):
        contents = ds3AllocateChunkResponse.contents
        self.retryAfter = contents.retry_after
        self.chunk = Ds3CacheList(contents.objects)

class Ds3AvailableChunksResponse(object):
    """A list of all chunks in a job that can currently be processed.

    Members:

        retryAfter (int) : retry interval in seconds.

        bulkPlan(Ds3BulkPlan) : collection of chunks.

        """
    def __init__(self, ds3AvailableChunksResponse):
        contents = ds3AvailableChunksResponse.contents
        self.retryAfter = contents.retry_after
        self.bulkPlan = Ds3BulkPlan(contents.object_list)

class Ds3SearchObject(object):
    """Search parameters for Get Objects

    Members:

        bucketId (string) : The UUID or name for a bucket.

        id (string) : The UUID for an object.

        lastModified (string) : The date the object was created in the format YYYY-MM-DD hh:mm:ss.xxx.

        name (string) : The name of an object.

        owner (Ds3Owner) : The owner of an object.

        size (long) : The size of the object in bytes.

        storageClass (string) : unused.

        type (string) : The type of object. Values: DATA, FOLDER

        version (string) : The version of an object.

    Cast to string for description.
    """
    def __init__(self, ds3SearchObject):
        contents = ds3SearchObject.contents
        self.bucketId = checkExistence(contents.bucket_id)
        self.id = checkExistence(contents.id)
        self.name = checkExistence(contents.name)
        self.size = contents.size
        self.owner = checkExistence(contents.owner, wrapper = Ds3Owner)
        self.lastModified = checkExistence(contents.last_modified)
        self.storageClass = checkExistence(contents.storage_class)
        self.type = checkExistence(contents.type)
        self.version = checkExistence(contents.version)
    def __str__(self):
        response = "BucketId: " + str(self.bucketId)
        response += " | Id: " + str(self.id)
        response += " | Name: " + str(self.name)
        response += " | Size: " + str(self.size)
        response += " | Owner: (" + str(self.id) + ")"
        response += " | LastModified: " + str(self.lastModified)
        response += " | StorageClass: " + str(self.storageClass)
        response += " | Type: " + str(self.type)
        response += " | Version: " + str(self.version)
        return response

class Ds3BuildInformation(object):
    """Describes the Black Pearl Software

    Members:

        branch (string) : The branch used to build the API.

        revision (string) : The revision of the software build.

        version (string) : The version of the software build.

    Cast to string for description.
    """
    def __init__(self, ds3BuildInfo):
        contents = ds3BuildInfo.contents
        self.branch = checkExistence(contents.branch)
        self.revision = checkExistence(contents.revision)
        self.version = checkExistence(contents.version)
    def __str__(self):
        response = "Branch: " + str(self.branch)
        response += " | Revision: " + str(self.revision)
        response += " | Version: " + str(self.version)
        return response

class Ds3SystemInformation(object):
    """Describes the Black Pearl Hardware and Software

    Members:

        apiVersion (string) : The version of the DS3 API. The version is in the form X.Y, where X is the MD5 checksum across all request handler major revisions and Y is the MD5 checksum across all request handler full versions (including the minor revision).

        buildInformation (ds3BuildInfo) : A container for the information about the build.

        serialNumber (string) : The serial number of the BlackPearl Deep Storage Gateway 

    Cast to string for description.
    """
    def __init__(self, ds3SystemInfo):
        contents = ds3SystemInfo.contents
        self.apiVersion = checkExistence(contents.api_version)
        self.serialNumber = checkExistence(contents.serial_number)
        self.buildInformation = checkExistence(contents.build_information, wrapper = Ds3BuildInformation)
    def __str__(self):
        response = "API Version: " + str(self.apiVersion)
        response += " | Serial Number: " + str(self.serialNumber)
        response += " | Build Information: " + str(self.buildInformation)
        return response

class Ds3SystemHealthInformation(object):
    """Verifies that the system appears to be online and functioning normally. If critical components in the data path between the client and the BlackPearl gateway are unresponsive, an error is generated.

    Members:

        msRequiredToVerifyDataPlannerHealth (long) : The amount of time, in milliseconds, that it took the gateway to respond.
    """
    def __init__(self, ds3HealthInfo):
        contents = ds3HealthInfo.contents
        self.msRequiredToVerifyDataPlannerHealth = contents.ms_required_to_verify_data_planner_health

def typeCheck(input_arg, type_to_check):
    if isinstance(input_arg, type_to_check):
        return input_arg
    else:
        raise TypeError("expected instance of type " + type_to_check.__name__ + ", got instance of type " + type(input_arg).__name__)

def ensureUTF8(input_arg):
    if isinstance(input_arg, unicode):
        return input_arg.encode('utf-8')
    return input_arg

def typeCheckString(input_arg):
    return ensureUTF8(typeCheck(input_arg, basestring))

def typeCheckObjectList(fileList):
    result = []
    for item in fileList:
        if isinstance(item, tuple):
            result.append((typeCheckString(item[0]), item[1]))
        else:
            result.append(typeCheckString(item))
    return result

def enumCheck(input_arg, enum_dict):
    if input_arg in enum_dict.keys():
        return enum_dict[input_arg]
    else:
        raise TypeError("expected value to be one of " + str(enum_dict.keys()) + ", got " + str(input_arg))

def enumCheckDs3ObjectType(input_arg):
    return enumCheck(input_arg, {"DATA":0, "FOLDER":1})

def addMetadataToRequest(request, metadata):
    if metadata:
        for key in metadata:
            if type(metadata[key]) is list or type(metadata[key]) is tuple:
                for value in metadata[key]:
                    libds3.lib.ds3_request_set_metadata(request, typeCheckString(key), typeCheckString(value));
            else:
                libds3.lib.ds3_request_set_metadata(request, typeCheckString(key), typeCheckString(metadata[key]));

def extractMetadataFromResponse(metaData):
    result = {}
    keys = libds3.lib.ds3_metadata_keys(metaData)
    if keys:
        for key_index in xrange(0, keys.contents.num_keys):
            key = keys.contents.keys[key_index].contents.value
            metadataEntry = libds3.lib.ds3_metadata_get_entry(metaData, key)
            result[key] = arrayToList(metadataEntry.contents.values, metadataEntry.contents.num_values)
            libds3.lib.ds3_free_metadata_entry(metadataEntry)
        libds3.lib.ds3_free_metadata_keys(keys)
    return result

def createClientFromEnv():
    """Build a Ds3Client from environment varialbles.

        Required: DS3_ACCESS_KEY, DS3_SECRET_KEY, DS3_ENDPOINT

        Optional: http_proxy

    """ 
    libDs3Client = POINTER(libds3.LibDs3Client)()
    error = libds3.lib.ds3_create_client_from_env(byref(libDs3Client))
    if error:
        raise Ds3Error(error)
    clientContents = libDs3Client.contents
    clientCreds = clientContents.creds.contents
    creds = Credentials(clientCreds.access_id.contents.value, clientCreds.secret_key.contents.value)
    proxyValue = checkExistence(clientContents.proxy)
    client = Ds3Client(clientContents.endpoint.contents.value, creds, proxyValue)
    libds3.lib.ds3_free_creds(clientContents.creds)
    libds3.lib.ds3_free_client(libDs3Client)
    return client

class Ds3Client(object):
    """This object is used to communicate with a remote DS3/Spectra S3 endpoint.  All communication with the Spectra S3 API is done with this class.
    """
    def __init__(self, endpoint, credentials, proxy = None):
        self._ds3Creds = libds3.lib.ds3_create_creds(c_char_p(credentials.accessKey), c_char_p(credentials.secretKey))
        self._client = libds3.lib.ds3_create_client(c_char_p(endpoint), self._ds3Creds)
        self.credentials = credentials
        self.endpoint = endpoint
        self.proxy = proxy
        if proxy:
            libds3.lib.ds3_client_proxy(self._client, proxy)

    def verifySystemHealth(self):
        """Returns how long it took to verify the health of the system.
        In the event that the system is in a bad state, an error will be thrown.
        """
        response = POINTER(libds3.LibDs3VerifySystemHealthResponse)()
        request = libds3.lib.ds3_init_verify_system_health()
        error = libds3.lib.ds3_verify_system_health(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)
        result = Ds3SystemHealthInformation(response)
        libds3.lib.ds3_free_verify_system_health(response)
        return result

    def getService(self):
        """Returns a list of all the buckets the current access id has access to.
        """
        response = POINTER(libds3.LibDs3GetServiceResponse)()
        request = libds3.lib.ds3_init_get_service()
        error = libds3.lib.ds3_get_service(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)
        contents = response.contents
        for i in xrange(0, contents.num_buckets):
            yield Ds3Bucket(contents.buckets[i])

        libds3.lib.ds3_free_service_response(response)


    def getBucket(self, bucketName, prefix = None, nextMarker = None, delimiter = None, maxKeys = None):
        """Returns a list of all the objects in a specific bucket as specified by `bucketName`.  This will return at most 1000 objects.
        In order to retrieve more, pagination must be used.  The `nextMarker` is used to specify where the next 1000 objects will
        start listing from.

        `delimiter` can be used to list objects like directories.  So for example, if delimiter is set to '/' then it will return
        a list of 'directories' in the commons prefixes field in the response.  In order to list all the files in that directory use the prefix parameter.
        For example:

            client.getBucket("my_bucket", prefix = 'dir', delimiter = '/')

        The above will list any files and directories that are in the 'dir' directory. 
        """
        response = POINTER(libds3.LibDs3GetBucketResponse)()
        request = libds3.lib.ds3_init_get_bucket(typeCheckString(bucketName))
        if prefix:
            libds3.lib.ds3_request_set_prefix(request, typeCheckString(prefix))
        if nextMarker:
            libds3.lib.ds3_request_set_marker(request, nextMarker)
        if delimiter:
            libds3.lib.ds3_request_set_delimiter(request, typeCheckString(delimiter))
        if maxKeys:
            libds3.lib.ds3_request_set_max_keys(request, maxKeys)
        error = libds3.lib.ds3_get_bucket(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        bucket = Ds3BucketDetails(response)

        libds3.lib.ds3_free_bucket_response(response)

        return bucket

    def headObject(self, bucketName, objectName):
        """Returns the metadata for the retrieved object as a dictionary of lists.  If the object does not exist  
        an error is thrown with a status code of 404.
        """
        response = POINTER(libds3.LibDs3Metadata)()
        request = libds3.lib.ds3_init_head_object(typeCheckString(bucketName), typeCheckString(objectName))

        error = libds3.lib.ds3_head_object(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        metadata = extractMetadataFromResponse(response)

        libds3.lib.ds3_free_metadata(response)

        return metadata

    def headBucket(self, bucketName):
        """Checks whether a bucket exists.
        """
        request = libds3.lib.ds3_init_head_bucket(typeCheckString(bucketName))
        error = libds3.lib.ds3_head_bucket(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def deleteFolder(self, bucketName, folderName):
        """Deletes a folder and all the objects contained within it.
        """
        request = libds3.lib.ds3_init_delete_folder(typeCheckString(bucketName), typeCheckString(folderName))
        error = libds3.lib.ds3_delete_folder(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def getSystemInformation(self):
        """Returns the version and other information about the Spectra S3 endpoint.
        """
        response = POINTER(libds3.LibDs3GetSystemInformationResponse)()
        request = libds3.lib.ds3_init_get_system_information()
        error = libds3.lib.ds3_get_system_information(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)
        result = Ds3SystemInformation(response)
        libds3.lib.ds3_free_get_system_information(response)
        return result


    def getObject(self, bucketName, objectName, offset, jobId, realFileName = None):
        """Gets an object from the Spectra S3 endpoint.  Use `realFileName` when the `objectName`
        that you are getting from Spectra S3 does not match what will be on the local filesystem.
        Returns the metadata for the retrieved object as a dictionary, where keys are
        associated with a list of the values for that key.

        This can only be used within the context of a Bulk Get Job.
        """
        objectName = typeCheckString(objectName)
        effectiveFileName = objectName
        if realFileName:
            effectiveFileName = typeCheckString(realFileName)
        response = POINTER(libds3.LibDs3Metadata)()
        request = libds3.lib.ds3_init_get_object_for_job(typeCheckString(bucketName), objectName, offset, jobId)
        localFile = open(effectiveFileName, "wb")
        localFile.seek(offset, 0)
        error = libds3.lib.ds3_get_object_with_metadata(self._client, request, byref(c_int(localFile.fileno())), libds3.lib.ds3_write_to_fd, byref(response))
        localFile.close()
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        metadata = extractMetadataFromResponse(response)
        libds3.lib.ds3_free_metadata(response)
        return metadata

    def putBucket(self, bucketName):
        """Creates a new bucket where objects can be stored.
        """
        bucketName = typeCheckString(bucketName)
        request = libds3.lib.ds3_init_put_bucket(bucketName)
        error = libds3.lib.ds3_put_bucket(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def putObject(self, bucketName, objectName, offset, size, jobId, realFileName = None, metadata = None):
        """Puts an object to the Spectra S3 endpoint.  Use `realFileName` when the `objectName`
        that you are putting to Spectra S3 does not match what is on the local filesystem.
        Use metadata to set the metadata for the object. metadata's value should be
        a dictionary, where keys are associated with either a value or a list of the
        values for that key.

        This can only be used within the context of a Spectra S3 Bulk Put job.
        """
        objectName = typeCheckString(objectName)
        effectiveFileName = objectName
        if realFileName:
            effectiveFileName = typeCheckString(realFileName)
        request = libds3.lib.ds3_init_put_object_for_job(typeCheckString(bucketName), objectName, c_ulonglong(offset), c_ulonglong(size), jobId)

        addMetadataToRequest(request, metadata)

        localFile = open(effectiveFileName, "rb")
        localFile.seek(offset, 0)
        error = libds3.lib.ds3_put_object(self._client, request, byref(c_int(localFile.fileno())), libds3.lib.ds3_read_from_fd)
        localFile.close()
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def deleteObject(self, bucketName, objName):
        """Deletes an object from the specified bucket.  If deleting several files at once, use `deleteObjects` instead.
        """
        request = libds3.lib.ds3_init_delete_object(typeCheckString(bucketName), typeCheckString(objName))
        error = libds3.lib.ds3_delete_object(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def deleteObjects(self, bucketName, fileNameList):
        """Deletes multiple objects from the bucket using a single API call.
        """
        bulkObjs = libds3.toDs3BulkObjectList(typeCheckObjectList(fileNameList))
        request = libds3.lib.ds3_init_delete_objects(typeCheckString(bucketName))
        error = libds3.lib.ds3_delete_objects(self._client, request, bulkObjs)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def deleteBucket(self, bucketName):
        """Deletes a bucket.  If the bucket is not empty, then this request will fail.  All objects must be deleted first
        before the bucket can be deleted.
        """
        request = libds3.lib.ds3_init_delete_bucket(typeCheckString(bucketName))
        error = libds3.lib.ds3_delete_bucket(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def putBulk(self, bucketName, fileInfoList):
        """Initiates a start bulk put with the remote Spectra S3 endpoint.  The `fileInfoList` is a list of (objectName, size) tuples.
        `objectName` does not have to be the actual name on the local file system, but it will be the name that you must
        initiate a single object put to later.  `size` must reflect the actual size of the file that is being put.
        """
        bulkObjs = libds3.toDs3BulkObjectList(typeCheckObjectList(fileInfoList))
        response = POINTER(libds3.LibDs3BulkResponse)()
        request = libds3.lib.ds3_init_put_bulk(typeCheckString(bucketName), bulkObjs)
        error = libds3.lib.ds3_bulk(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        bulkResponse = Ds3BulkPlan(response)

        libds3.lib.ds3_free_bulk_response(response)

        return bulkResponse

    def getBulk(self, bucketName, fileNameList, chunkOrdering = True):
        """Initiates a start bulk get with the remote Spectra S3 endpoint.  All the files that will be retrieved must be specified in
        `fileNameList`.
        """
        bulkObjs = libds3.toDs3BulkObjectList(typeCheckObjectList(fileNameList))
        response = POINTER(libds3.LibDs3BulkResponse)()
        chunkOrderingValue = libds3.LibDs3ChunkOrdering.IN_ORDER
        if not chunkOrdering:
            chunkOrderingValue = libds3.LibDs3ChunkOrdering.NONE
        request = libds3.lib.ds3_init_get_bulk(typeCheckString(bucketName), bulkObjs, chunkOrderingValue)
        error = libds3.lib.ds3_bulk(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        bulkResponse = Ds3BulkPlan(response)

        libds3.lib.ds3_free_bulk_response(response)

        return bulkResponse

    def getObjects(self, bucketName = None, creationDate = None, objId = None, name = None, pageLength = None, pageOffset = None, objType = None, version = None):
        """Returns a list of objects. 

        Optional Search parameters:

            bucketName (string) : The UUID or name for a bucket.

            creationDate (string) : The date the object was created in the format YYYY-MM-DD hh:mm:ss.xxx.

            name (string) : The name of an object.

            objId (string) : The UUID for an object.

            objType (string) : The type of object. Values: DATA, FOLDER

            pageLength (int) : The maximum number of objects to list. The default is all items after pageOffset.

            pageOffset (int) : The starting point for the first object to list. The default is 0. 

            version (string) : The version of an object.
        """
        request = libds3.lib.ds3_init_get_objects()
        response = POINTER(libds3.LibDs3GetObjectsResponse)()

        if bucketName:
            libds3.lib.ds3_request_set_bucket_name(request, typeCheckString(bucketName))
        if creationDate:
            libds3.lib.ds3_request_set_creation_date(request, typeCheckString(creationDate))
        if objId:
            libds3.lib.ds3_request_set_id(request, typeCheckString(objId))
        if name:
            libds3.lib.ds3_request_set_name(request, typeCheckString(name))
        if pageLength:
             libds3.lib.ds3_request_set_page_length(request, typeCheckString(str(pageLength)))
        if pageOffset:
             libds3.lib.ds3_request_set_page_offset(request, typeCheckString(str(pageOffset)))
        if objType:
            libds3.lib.ds3_request_set_type(request, enumCheckDs3ObjectType(objType))
        if version:
            libds3.lib.ds3_request_set_version(request, typeCheckString(str(version)))

        error = libds3.lib.ds3_get_objects(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        result = arrayToList(response.contents.objects, response.contents.num_objects, wrapper = Ds3SearchObject)

        libds3.lib.ds3_free_objects_response(response)

        return result

    def allocateChunk(self, chunkId):
        """*Deprecated* - Allocates a specific chunk to be allocated in cache so that the objects in that chunk can safely be put without a need
        to handle 307 redirects.
        """
        request = libds3.lib.ds3_init_allocate_chunk(chunkId)
        response = POINTER(libds3.LibDs3AllocateChunkResponse)()
        error = libds3.lib.ds3_allocate_chunk(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)
        result = Ds3AllocateChunkResponse(response)

        libds3.lib.ds3_free_allocate_chunk_response(response)

        return result

    def getAvailableChunks(self, jobId):
        """Returns a list of all chunks in a job that can currently be processed.  It will return a subset of all chunks, and it
        will return that same set of chunks until all the data in one of the chunks returned has been either completely gotten,
        or been completely put.
        """
        request = libds3.lib.ds3_init_get_available_chunks(jobId)
        response = POINTER(libds3.LibDs3GetAvailableChunksResponse)()
        error = libds3.lib.ds3_get_available_chunks(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)

        if error:
            raise Ds3Error(error)

        result = Ds3AvailableChunksResponse(response)

        libds3.lib.ds3_free_available_chunks_response(response)

        return result

    def _sendJobRequest(self, func, request):
        response = POINTER(libds3.LibDs3BulkResponse)()
        error = func(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        bulkResponse = Ds3BulkPlan(response)

        libds3.lib.ds3_free_bulk_response(response)

        return bulkResponse

    def getJob(self, jobId):
        """Returns information about a job, including all the chunks in the job, as well as the status of the job.
        """
        request = libds3.lib.ds3_init_get_job(jobId)
        return self._sendJobRequest(libds3.lib.ds3_get_job, request)

    def getJobs(self):
        """Returns a list of all jobs.
        """
        request = libds3.lib.ds3_init_get_jobs()
        response = POINTER(libds3.LibDs3GetJobsResponse)()
        error = libds3.lib.ds3_get_jobs(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        result = []
        for index in xrange(0, response.contents.jobs_size):
            result.append(Ds3BulkPlan(response.contents.jobs[index]))
        libds3.lib.ds3_free_get_jobs_response(response)

        return result

    def putJob(self, jobId):
        """Modifies a job to reset the timeout timer for the job.
        """
        request = libds3.lib.ds3_init_put_job(jobId)
        return self._sendJobRequest(libds3.lib.ds3_put_job, request)

    def deleteJob(self, jobId):
        """Cancels a currently in progress job.
        """
        request = libds3.lib.ds3_init_delete_job(jobId)
        error = libds3.lib.ds3_delete_job(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def getPhysicalPlacement(self, bucketName, fileNameList, fullDetails = False):
        """Returns where in the Spectra S3 system each file in `fileNameList` is located.
        """
        response = POINTER(libds3.LibDs3GetPhysicalPlacementResponse)()
        bulkObjs = libds3.toDs3BulkObjectList(typeCheckObjectList(fileNameList))
        bucketName=typeCheckString(bucketName)
        if fullDetails:
            request = libds3.lib.ds3_init_get_physical_placement(bucketName, bulkObjs)
        else:
            request = libds3.lib.ds3_init_get_physical_placement_full_details(bucketName, bulkObjs)
        error = libds3.lib.ds3_get_physical_placement(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)

        if error:
            raise Ds3Error(error)

        placements = []
        if response:
            placements = arrayToList(response.contents.tapes, response.contents.num_tapes, lambda obj: obj.barcode.contents.value)
            libds3.lib.ds3_free_get_physical_placement_response(response)

        return placements
