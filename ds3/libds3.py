from ctypes import *

lib = cdll.LoadLibrary("libds3.so")

def asCList(orig):
    cList = (ctypes.c_char_p * len(orig))()
    cList[:] = orig
    return cList

def toDs3BulkObjectList(fileList):
    bulkList = lib.ds3_init_bulk_object_list(len(fileList))
    bulkContents = bulkList.contents
    for i in xrange(len(fileList)):
        bulkContents.list[i].name = lib.ds3_str_init(fileList[i])
    return bulkList

class LibDs3Str(Structure):
    _fields_ = [("value", c_char_p), ("size", c_size_t)]

class LibDs3Creds(Structure):
    _fields_ = [("access_id", POINTER(LibDs3Str)), ("secret_key", POINTER(LibDs3Str))]

class LibDs3Client(Structure):
    _fields_ = [("endpoint", POINTER(LibDs3Str)), ("proxy", POINTER(LibDs3Str)), ("num_redirects", c_ulonglong), ("creds", POINTER(LibDs3Creds))]

class LibDs3ErrorResponse(Structure):
    _fields_ = [("status_code", c_ulonglong), ("status_message", POINTER(LibDs3Str)), ("error_body", POINTER(LibDs3Str))]

class LibDs3ErrorCode(object):
    DS3_ERROR_INVALID_XML = 0
    DS3_ERROR_CURL_HANDLER = 1
    DS3_ERROR_REQUEST_FAILED = 2
    DS3_ERROR_MISSING_ARGS = 3
    DS3_ERROR_BAD_STATUS_CODE = 4

class LibDs3Error(Structure):
    _fields_ = [("ds3_error_code", c_int), ("message", POINTER(LibDs3Str)), ("error", POINTER(LibDs3ErrorResponse))]

class LibDs3Bucket(Structure):
    _fields_ = [("creation_date", POINTER(LibDs3Str)), ("name", POINTER(LibDs3Str))]

class LibDs3Owner(Structure):
    _fields_ = [("name", POINTER(LibDs3Str)), ("id", POINTER(LibDs3Str))]

class LibDs3Object(Structure):
    _fields_ = [("name", POINTER(LibDs3Str)), ("etag", POINTER(LibDs3Str)), ("size", c_ulonglong), ("owner", POINTER(LibDs3Owner)), ("last_modified", POINTER(LibDs3Str)), ("storage_class", POINTER(LibDs3Str))]

class LibDs3GetServiceResponse(Structure):
    _fields_ = [("buckets", POINTER(LibDs3Bucket)), ("num_buckets", c_size_t), ("owner", POINTER(LibDs3Owner))]

class LibDs3GetBucketResponse(Structure):
    _fields_ = [("objects", POINTER(LibDs3Object)), ("num_objects", c_size_t), ("creation_date", POINTER(LibDs3Str)), ("is_truncated", c_bool), ("marker", POINTER(LibDs3Str)), ("delimiter", POINTER(LibDs3Str)), ("max_keys", c_int), ("name", POINTER(LibDs3Str)), ("next_marker", POINTER(LibDs3Str)), ("prefix", POINTER(LibDs3Str)), ("common_prefixes", POINTER(POINTER(LibDs3Str))), ("num_common_prefixes", c_ulonglong)]

class LibDs3BulkObject(Structure):
    _fields_ = [("name", POINTER(LibDs3Str)), ("length", c_ulonglong), ("offset", c_ulonglong), ("in_cache", c_bool)]

class LibDs3BulkObjectList(Structure):
    _fields_ = [("list", POINTER(LibDs3BulkObject)), ("size", c_ulonglong), ("chunk_number", c_ulonglong), ("node_id", POINTER(LibDs3Str)), ("server_id", POINTER(LibDs3Str)), ("chunk_id", POINTER(LibDs3Str))]

class LibDs3ChunkOrdering(object):
    IN_ORDER = 0
    NONE = 1

class LibDs3Priority(object):
    CRITIAL = 0
    VERY_HIGH = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5
    MINIMIZED_DUE_TO_TOO_MANY_REQUESTS = 6
class LibDs3RequestType(object):
    PUT = 0
    GET = 1

class LibDs3WriteOptimization(object):
    CAPACITY = 0
    PERFORMANCE = 1

class LibDs3BulkResponse(Structure):
    _fields_ = [("bucket_name", POINTER(LibDs3Str)), ("cached_size_in_bytes", c_ulonglong), ("chunk_ordering", c_int), ("completed_size_in_bytes", c_ulonglong), ("job_id", POINTER(LibDs3Str)), ("original_size_in_bytes", c_ulonglong), ("ds3_job_priority", c_int), ("request_type", c_int), ("start_date", POINTER(LibDs3Str)), ("user_id", POINTER(LibDs3Str)), ("user_name", POINTER(LibDs3Str)), ("write_optimization", c_int), ("list", POINTER(POINTER(LibDs3BulkObjectList))), ("list_size", c_size_t)]

class LibDs3AllocateChunkResponse(Structure):
    _fields_ = [("objects", POINTER(LibDs3BulkObjectList)), ("retry_after", c_ulonglong)]

class LibDs3GetAvailableChunksResponse(Structure):
    _fields_ = [("object_list", POINTER(LibDs3BulkResponse)), ("retry_after", c_ulonglong)]

class LibDs3Request(Structure):
    pass

lib.ds3_str_init.restype = POINTER(LibDs3Str)

lib.ds3_create_creds.restype = POINTER(LibDs3Creds)
lib.ds3_create_client.restype = POINTER(LibDs3Client)
lib.ds3_create_client_from_env.restype = POINTER(LibDs3Error)
lib.ds3_init_get_service.restype = POINTER(LibDs3Request)
lib.ds3_init_get_bucket.restype = POINTER(LibDs3Request)
lib.ds3_init_get_object.restype = POINTER(LibDs3Request)
lib.ds3_init_put_bucket.restype = POINTER(LibDs3Request)
lib.ds3_init_put_object.restype = POINTER(LibDs3Request)
lib.ds3_init_delete_bucket.restype = POINTER(LibDs3Request)
lib.ds3_init_delete_object.restype = POINTER(LibDs3Request)
lib.ds3_init_allocate_chunk.restype = POINTER(LibDs3Request)
lib.ds3_init_get_available_chunks.restype = POINTER(LibDs3Request)
lib.ds3_init_put_bulk.restype = POINTER(LibDs3Request)
lib.ds3_init_get_bulk.restype = POINTER(LibDs3Request)
lib.ds3_get_service.restype = POINTER(LibDs3Error)
lib.ds3_get_bucket.restype = POINTER(LibDs3Error)
lib.ds3_get_object.restype = POINTER(LibDs3Error)
lib.ds3_bulk.restype = POINTER(LibDs3Error)
lib.ds3_allocate_chunk.restype = POINTER(LibDs3Error)
lib.ds3_get_available_chunks.restype = POINTER(LibDs3Error)
lib.ds3_delete_bucket.restype = POINTER(LibDs3Error)
lib.ds3_put_object.restype = POINTER(LibDs3Error)

lib.ds3_write_to_file.restype = c_size_t
lib.ds3_read_from_file.restype = c_size_t

lib.ds3_convert_file_list.restype = POINTER(LibDs3BulkObjectList)
