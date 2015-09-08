from ctypes import *
import libds3

class Ds3Error(Exception):
    def __init__(self, libds3Error):
        self.reason = libds3Error.contents.message.contents.value
        response = libds3Error.contents.error
        self._hasResponse = False
        if response:
            self._hasResponse = True
            self.statusCode = response.contents.status_code
            self.statusMessage = response.contents.status_message.contents.value
            if response.contents.error_body:
                self.message = response.contents.error_body.contents.value
            else:
                self.message = None

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
    def __init__(self, accessKey, secretKey):
        self.accessKey = accessKey
        self.secretKey = secretKey

class Ds3Bucket(object):
    def __init__(self, ds3Bucket):
        self.name = ds3Bucket.name.contents.value
        self.creationDate = ds3Bucket.creation_date.contents.value
    def __str__(self):
        return "Name: " + self.name + " | Creation Date: " + self.creationDate
    def __repr__(self):
        return self.__str__()

class Ds3Owner(object):
    def __init__(self, ds3Owner):
        ownerContents = ds3Owner.contents
        self.name = ownerContents.name.contents.value
        self.id = ownerContents.id.contents.value
    def __str__(self):
        return "Name: " + self.name + " | ID: " + self.id
    def __repr__(self):
        return self.__str__()

class Ds3Object(object):
    def __init__(self, ds3Object):
        self.name = ds3Object.name.contents.value
        if ds3Object.etag:
            self.etag = ds3Object.etag.contents.value
        else:
            self.etag = None
        self.size = ds3Object.size
        self.owner = Ds3Owner(ds3Object.owner)
    def __str__(self):
        return "Name: " + self.name + " | Size: " + str(self.size) + " | Etag: " + str(self.etag) + " | Owner: " + str(self.owner)
    def __repr__(self):
        return self.__str__()

class Ds3BucketDetails(object):
    def __init__(self, ds3Bucket):
        bucketContents = ds3Bucket.contents
        self.name = bucketContents.name.contents.value
        if bucketContents.creation_date:
            self.creationDate = bucketContents.creation_date.contents.value
        else:
            self.creation_date = None

        self.isTruncated = bool(bucketContents.is_truncated)
        if bucketContents.marker:
            self.marker = bucketContents.marker.contents.value
        else:
            self.marker = None
        if bucketContents.delimiter:
            self.delimiter = bucketContents.delimiter.contents.value
        else:
            self.delimiter = None
        self.maxKeys = bucketContents.max_keys
        if bucketContents.next_marker:
            self.nextMarker = bucketContents.next_marker.contents.value
        else:
            self.nextMarker = None
        if bucketContents.prefix:
            self.prefix = bucketContents.prefix.contents.value
        else:
            self.prefix = None
        self.commonPrefixes = []
        if bucketContents.num_common_prefixes > 0:
            for i in xrange(0, bucketContents.num_common_prefixes):
                self.commonPrefixes.append(bucketContents.common_prefixes[i].contents.value)
        self.objects = []
        if bucketContents.num_objects > 0:
            for i in xrange(0, bucketContents.num_objects):
                self.objects.append(Ds3Object(bucketContents.objects[i]))

class Ds3BulkObject(object):
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
    def __init__(self, bulkObjectList):
        contents = bulkObjectList.contents
        self.chunkNumber = contents.chunk_number
        if contents.node_id:
            self.nodeId = contents.node_id.contents.value
        else:
            self.nodeId = None
        if contents.server_id:
            self.serverId = contents.server_id.contents.value
        else:
            self.serverId = None
        self.chunkId = contents.chunk_id.contents.value
        self.objects = []
        for i in xrange(0, contents.size):
            self.objects.append(Ds3BulkObject(contents.list[i]))

class Ds3BulkPlan(object):
    def __init__(self, ds3BulkResponse):
        contents = ds3BulkResponse.contents
        if contents.bucket_name:
            self.bucketName = contents.bucket_name.contents.value
        if contents.cached_size_in_bytes:
            self.cachedSize = contents.cached_size_in_bytes
        if contents.completed_size_in_bytes:
            self.compltedSize = contents.completed_size_in_bytes
        if contents.job_id:
            self.jobId = contents.job_id.contents.value
        if contents.original_size_in_bytes:
            self.originalSize = contents.original_size_in_bytes
        if contents.start_date:
            self.startDate = contents.start_date.contents.value
        if contents.user_id:
            self.userId = contents.user_id.contents.value
        if contents.user_name:
            self.userName = contents.user_name.contents.value
        self.requestType = contents.request_type
        self.status = contents.status

        self.chunks = []
        for i in xrange(0, contents.list_size):
            self.chunks.append(Ds3CacheList(contents.list[i]))
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
    def __init__(self, ds3AllocateChunkResponse):
        contents = ds3AllocateChunkResponse.contents
        self.retryAfter = contents.retry_after
        self.chunk = Ds3CacheList(contents.objects)

class Ds3AvailableChunksResponse(object):
    def __init__(self, ds3AvailableChunksResponse):
        contents = ds3AvailableChunksResponse.contents
        self.retryAfter = contents.retry_after
        self.bulkPlan = Ds3BulkPlan(contents.object_list)

def createClientFromEnv():
    libDs3Client = POINTER(libds3.LibDs3Client)()
    error = libds3.lib.ds3_create_client_from_env(byref(libDs3Client))
    if error:
        raise Ds3Error(error)
    clientContents = libDs3Client.contents
    clientCreds = clientContents.creds.contents
    creds = Credentials(clientCreds.access_id.contents.value, clientCreds.secret_key.contents.value)
    proxyValue = None
    if clientContents.proxy:
        proxyValue = clientContents.proxy.contents.value
    client = Ds3Client(clientContents.endpoint.contents.value, creds, proxyValue)
    libds3.lib.ds3_free_creds(clientContents.creds)
    libds3.lib.ds3_free_client(libDs3Client)
    return client

class Ds3SearchObject(object):
    def __init__(self, ds3SearchObject):
        def checkExistence(ds3Str):
            if ds3Str:
                return ds3Str.contents.value
            else:
                return None
        contents=ds3SearchObject.contents
        self.bucketId=checkExistence(contents.bucket_id)
        self.id=checkExistence(contents.id)
        self.name=checkExistence(contents.name)
        self.size=contents.size
        if contents.owner:
            self.owner=Ds3Owner(contents.owner)
        else:
            self.owner=None
        self.lastModified=checkExistence(contents.last_modified)
        self.storageClass=checkExistence(contents.storage_class)
        self.type=checkExistence(contents.type)
        self.version=checkExistence(contents.version)
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

def extractSearchObjects(searchObjects):
    objects=[]
    for index in range(0, searchObjects.contents.num_objects):
        objects.append(Ds3SearchObject(searchObjects.contents.objects[index]))
    return objects

class Ds3Client(object):
    def __init__(self, endpoint, credentials, proxy = None):
        self._ds3Creds = libds3.lib.ds3_create_creds(c_char_p(credentials.accessKey), c_char_p(credentials.secretKey))
        self._client = libds3.lib.ds3_create_client(c_char_p(endpoint), self._ds3Creds)
        self.credentials = credentials

    def getService(self):
        response = POINTER(libds3.LibDs3GetServiceResponse)()
        request = libds3.lib.ds3_init_get_service()
        error = libds3.lib.ds3_get_service(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)
        contents = response.contents
        for i in xrange(0, response.contents.num_buckets):
            yield Ds3Bucket(contents.buckets[i])

        libds3.lib.ds3_free_service_response(response)

    def getBucket(self, bucketName, prefix = None, nextMarker = None, delimiter = None, maxKeys = None):
        response = POINTER(libds3.LibDs3GetBucketResponse)()
        request = libds3.lib.ds3_init_get_bucket(bucketName)
        if prefix:
            libds3.lib.ds3_request_set_prefix(request, prefix)
        if nextMarker:
            libds3.lib.ds3_request_set_marker(request, nextMarker)
        if delimiter:
            libds3.lib.ds3_request_set_delimiter(request, delimiter)
        if maxKeys:
            libds3.lib.ds3_request_set_max_keys(request, maxKeys)
        error = libds3.lib.ds3_get_bucket(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        bucket = Ds3BucketDetails(response)

        libds3.lib.ds3_free_bucket_response(response)

        return bucket

    def getObject(self, bucketName, objectName, offset, jobId, realFileName = None):
        '''
        Gets an object from the ds3 endpoint.  Use `realFileName` when the `objectName`
        that you are getting to ds3 does not match what will be on the local filesystem
        '''
        effectiveFileName = objectName
        if realFileName:
            effectiveFileName = realFileName
        request = libds3.lib.ds3_init_get_object_for_job(bucketName, objectName, offset, jobId)
        localFile = open(effectiveFileName, "w")
        error = libds3.lib.ds3_get_object(self._client, request, byref(c_int(localFile.fileno())), libds3.lib.ds3_write_to_fd)
        localFile.close()
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)


    def putBucket(self, bucketName):
        request = libds3.lib.ds3_init_put_bucket(bucketName)
        error = libds3.lib.ds3_put_bucket(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def putObject(self, bucketName, objectName, offset, size, jobId, realFileName = None):
        '''
        Puts an object to the ds3 endpoint.  Use `realFileName` when the `objectName`
        that you are putting to ds3 does not match what is on the local filesystem.
        '''
        effectiveFileName = objectName
        if realFileName:
            effectiveFileName = realFileName
        request = libds3.lib.ds3_init_put_object_for_job(bucketName, objectName, offset, size, jobId)
        localFile = open(effectiveFileName, "r")
        error = libds3.lib.ds3_put_object(self._client, request, byref(c_int(localFile.fileno())), libds3.lib.ds3_read_from_fd)
        localFile.close()
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def deleteObject(self, bucketName, objName):
        request = libds3.lib.ds3_init_delete_object(bucketName, objName)
        error = libds3.lib.ds3_delete_object(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def deleteBucket(self, bucketName):
        request = libds3.lib.ds3_init_delete_bucket(bucketName)
        error = libds3.lib.ds3_delete_bucket(self._client, request)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

    def putBulk(self, bucketName, fileInfoList):
        '''
        Initiates a start bulk put with the remote ds3 endpoint.  The fileInfoList is a list of (objectName, size) tuples.
        `objectName` does not have to be the actual name on the local file system, but it will be the name that you must
        initiate a single object put to later.
        '''
        bulkObjs = libds3.lib.ds3_init_bulk_object_list(len(fileInfoList))
        bulkObjsList = bulkObjs.contents.list
        for i in xrange(0, len(fileInfoList)):
            bulkObjsList[i].name = libds3.lib.ds3_str_init(fileInfoList[i][0])
            bulkObjsList[i].length = fileInfoList[i][1]
        response = POINTER(libds3.LibDs3BulkResponse)()
        request = libds3.lib.ds3_init_put_bulk(bucketName, bulkObjs)
        error = libds3.lib.ds3_bulk(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        bulkResponse = Ds3BulkPlan(response)

        libds3.lib.ds3_free_bulk_response(response)

        return bulkResponse

    def getBulk(self, bucketName, fileNameList, chunkOrdering = True):
        bulkObjs = libds3.toDs3BulkObjectList(fileNameList)
        response = POINTER(libds3.LibDs3BulkResponse)()
        chunkOrderingValue = libds3.LibDs3ChunkOrdering.IN_ORDER
        if not chunkOrdering:
            chunkOrderingValue = libds3.LibDs3ChunkOrdering.NONE
        request = libds3.lib.ds3_init_get_bulk(bucketName, bulkObjs, chunkOrderingValue)
        error = libds3.lib.ds3_bulk(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        bulkResponse = Ds3BulkPlan(response)

        libds3.lib.ds3_free_bulk_response(response)

        return bulkResponse
        """
        Query Parameters Required: [], Optional: [bucketId, id, name, page_length, page_offset, type, version]
        </RequestRequirements>
        <SampleUrl>
        http[s]://datapathdnsnameofappliance/_rest_/object/[?page_length={32-bit integer}][&page_offset={32-bit integer}][&bucket_id={unique identifier or attribute}][&id={unique identifier or attribute}][&name={text}][&type={data|folder}][&version={64-bit integer}]
        </SampleUrl>"""
        
        """
        LIBRARY_API void ds3_request_set_custom_header(ds3_request* request, const char* header_name, const char* header_value);
        LIBRARY_API void ds3_request_set_prefix(ds3_request* request, const char* prefix);
        LIBRARY_API void ds3_request_set_delimiter(ds3_request* request, const char* delimiter);
        LIBRARY_API void ds3_request_set_marker(ds3_request* request, const char* marker);
        LIBRARY_API void ds3_request_set_max_keys(ds3_request* request, uint32_t max_keys);
        LIBRARY_API void ds3_request_set_md5(ds3_request* request, const char* md5);
        LIBRARY_API void ds3_request_set_metadata(ds3_request* request, const char* name, const char* value);
        LIBRARY_API void ds3_request_set_name(ds3_request* request, const char* name);
        LIBRARY_API void ds3_request_set_id(ds3_request* request, const char* id);
        LIBRARY_API void ds3_request_set_type(ds3_request* request, object_type type);
        LIBRARY_API void ds3_request_set_version(ds3_request* request, const char* version);"""

    def getObjects(self, bucketName, id = None, name = None, page_length = None, page_offset = None, type = None, version = None):
        request = libds3.lib.ds3_init_get_objects(bucketName)
        response = POINTER(libds3.LibDs3GetObjectsResponse)()
        
        if id:
            libds3.lib.ds3_request_set_id(request, id);
        if name:
            libds3.lib.ds3_request_set_name(request, name);
        if page_length:
            libds3.lib.ds3_request_set_page_length(request, page_length);
        if page_offset:
            libds3.lib.ds3_request_set_page_offset(request, page_offset);
        if type:
            libds3.lib.ds3_request_set_type(request, type);
        if version:
            libds3.lib.ds3_request_set_version(request, version);

        error = libds3.lib.ds3_get_objects(self._client, request, byref(response))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        result = extractSearchObjects(response)

        libds3.lib.ds3_free_objects_response(response)

        return result

    def allocateChunk(self, chunkId):
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
        request = libds3.lib.ds3_init_get_job(jobId)
        return self._sendJobRequest(libds3.lib.ds3_get_job, request)

    def putJob(self, jobId):
        request = libds3.lib.ds3_init_put_job(jobId)
        return self._sendJobRequest(libds3.lib.ds3_put_job, request)

    def deleteJob(self, jobId):
        request = libds3.lib.ds3_init_delete_job(jobId)
        error = libds3.lib.ds3_delete_job(jobId)
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)
