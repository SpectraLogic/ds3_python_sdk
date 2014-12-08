from ctypes import *

libds3 = cdll.LoadLibrary("libds3.so")

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
    _fields_ =[("name", POINTER(LibDs3Str)), ("id", POINTER(LibDs3Str))]

class LibDs3GetServiceResponse(Structure):
    _fields_ = [("buckets", POINTER(LibDs3Bucket)), ("num_buckets", c_size_t), ("owner", POINTER(LibDs3Owner))]

class LibDs3Request(Structure):
    pass

libds3.ds3_create_creds.restype = POINTER(LibDs3Creds)
libds3.ds3_create_client.restype = POINTER(LibDs3Client)
libds3.ds3_init_get_service.restype = POINTER(LibDs3Request)
libds3.ds3_get_service.restype = POINTER(LibDs3Error)

class Credentials(object):
    def __init__(self, accessKey, secretKey):
        self.accessKey = accessKey
        self.secretKey = secretKey

class Ds3Client(object):
    def __init__(self, endpoint, credentials):
        self._ds3Creds = libds3.ds3_create_creds(c_char_p(credentials.accessKey), c_char_p(credentials.secretKey))
        self._client = libds3.ds3_create_client(c_char_p(endpoint), self._ds3Creds)
        self.credentials = credentials

    def getService(self):
        response = POINTER(LibDs3GetServiceResponse)()
        request = libds3.ds3_init_get_service()
        error = libds3.ds3_get_service(self._client, request, byref(response))
        return response.contents

