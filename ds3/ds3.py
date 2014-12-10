from ctypes import *
import libds3

class Ds3Error(Exception):
    def __init__(self, libds3Error):
        self.message = libds3Error.contents.message.value

class Credentials(object):
    def __init__(self, accessKey, secretKey):
        self.accessKey = accessKey
        self.secretKey = secretKey

class Ds3Bucket(object):
    def __init__(self, ds3Bucket):
        self.name = ds3Bucket.name.contents.value
        self.creationDate = ds3Bucket.creation_date.contents.value

class Ds3Client(object):
    def __init__(self, endpoint, credentials):
        self._ds3Creds = libds3.lib.ds3_create_creds(c_char_p(credentials.accessKey), c_char_p(credentials.secretKey))
        self._client = libds3.lib.ds3_create_client(c_char_p(endpoint), self._ds3Creds)
        self.credentials = credentials

    def getService(self):
        response = POINTER(libds3.LibDs3GetServiceResponse)()
        request = libds3.lib.ds3_init_get_service()
        error = libds3.lib.ds3_get_service(self._client, request, byref(response))
        if error:
            raise Ds3Error(error)
        contents = response.contents

        for i in xrange(0, response.contents.num_buckets):
            yield Ds3Bucket(contents.buckets[i])
