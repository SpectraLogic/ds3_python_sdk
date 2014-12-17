from ctypes import *
import libds3

class Ds3Error(Exception):
    def __init__(self, libds3Error):
        self.message = libds3Error.contents.message.value
        libds3.lib.ds3_free_error(libds3Error)

class Credentials(object):
    def __init__(self, accessKey, secretKey):
        self.accessKey = accessKey
        self.secretKey = secretKey

class Ds3Bucket(object):
    def __init__(self, ds3Bucket):
        self.name = ds3Bucket.name.contents.value
        self.creationDate = ds3Bucket.creation_date.contents.value

class Ds3Owner(object):
    def __init__(self, ds3Owner):
        ownerContents = ds3Owner.contents
        self.name = ownerContents.name.contents.value
        self.id = ownerContents.id.contents.value

class Ds3Object(object):
    def __init__(self, ds3Object):
        self.name = ds3Object.name.contents.value
        if ds3Object.etag:
            self.etag = ds3Object.etag.contents.value
        else:
            self.etag = None
        self.size = ds3Object.size
        self.owner = Ds3Owner(ds3Object.owner)

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
                self.commonePrefixes.append(bucketContents.common_prefixes[i].contents.value)
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

class Ds3CacheList(object):
    def __init__(self, bulkObjectList):
        contents = bulkObjectList.contents
        self.chunkNumber = contents.chunk_number
        self.nodeId = contents.node_id.contents.value
        self.serverId = contents.server_id.contents.value
        self.chunkId = contents.chunk_id.contents.value
        self.objects = []
        for i in xrange(0, contents.size):
            self.objects.append(Ds3BulkObject(contents.list[i]))

class Ds3BulkPlan(object):
    def __init__(self, ds3BulkResponse):
        contents = ds3BulkResponse.contents
        self.bucketName = contents.bucket_name.contents.value
        self.cachedSize = contents.cached_size_in_bytes
        self.compltedSize = contents.completed_size_in_bytes
        self.jobId = contents.job_id.contents.value
        self.originalSize = contents.original_size_in_bytes
        self.startDate = contents.start_date.contents.value
        self.userId = contents.user_id.contents.value
        self.userName = contents.user_name.contents.value
        self.chunks = []
        for i in xrange(0, contents.list_size):
            self.chunks.append(Ds3CacheList(contents.list[i]))

class Ds3Client(object):
    def __init__(self, endpoint, credentials):
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

    def putBulk(self, bucketName, fileNameList):
        bulkObjs = libds3.lib.ds3_convert_file_list(libds3.asCList(fileNameList))
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
        error = libds3.lib.ds3_bulk(self._client, request, byref(request))
        libds3.lib.ds3_free_request(request)
        if error:
            raise Ds3Error(error)

        bulkResponse = Ds3BulkPlan(response)

        libds3.lib.ds3_free_bulk_response(response)

        return bulkResponse

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
