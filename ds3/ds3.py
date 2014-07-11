import hmac
import base64
import xml.dom.minidom
from xml.dom.minidom import Node
import xml.etree.ElementTree as xmldom

from hashlib import sha1
import httplib
import urllib2
import urlparse
import StringIO
from email.Utils import formatdate

from abc import ABCMeta
import posixpath

class XmlSerializer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def pretty_print_xml(self, xml_string):
        if xml_string:
            print xml.dom.minidom.parseString(xml_string).toprettyxml()
        
    def parse_string(self, xml_string):
        if self.verbose:
            self.pretty_print_xml(xml_string)
            
        return xml.dom.minidom.parseString(xml_string)
    
    def get_name_from_node(self, doc, nodename, parentname=None):
        for node in doc.getElementsByTagName(nodename):
            if parentname and not node.parentNode.nodeName == parentname:
                # this is not the node you are looking for
                continue
            
            for childnode in node.childNodes:
                if childnode.nodeType == Node.TEXT_NODE:
                    return childnode.data
                
        return ''
    
    def get_attribute_from_node(self, doc, nodename, attribute):
        node = doc.getElementsByTagName(nodename)
        return node[0].getAttribute(attribute)
        
    def to_ds3error(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        code = self.get_name_from_node(doc, "Code")
        httperrorcode = self.get_name_from_node(doc, "HttpErrorCode")
        message = self.get_name_from_node(doc, "Message") 
        obj = Ds3Error(code, httperrorcode, message)
        
        return obj
        
    def to_list_all_my_buckets_result(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        owner_node = doc.getElementsByTagName("Owner")
        servlist = ListAllMyBucketsResult(Owner(self.get_name_from_node(owner_node[0], "DisplayName"),
                                           self.get_name_from_node(owner_node[0], "ID")))
         
        for bucket_node in doc.getElementsByTagName("Bucket"):
            servlist.append(Bucket(self.get_name_from_node(bucket_node, "Name"),
                                   self.get_name_from_node(bucket_node, "CreationDate")))
            
        return servlist
                    
    def to_get_bucket_result(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        listbucket = ListBucketResult(self.get_name_from_node(doc, "Name"),
                                      self.get_name_from_node(doc, "Prefix"),
                                      self.get_name_from_node(doc, "Marker"),
                                      self.get_name_from_node(doc, "MaxKeys"),
                                      self.get_name_from_node(doc, "IsTruncated"),
                                      self.get_name_from_node(doc, "CreationDate"),
                                      self.get_name_from_node(doc, "Delimiter"),
                                      self.get_name_from_node(doc, "NextMarker"))
        
        for contentnode in doc.getElementsByTagName("Contents"):
            ownernode = contentnode.getElementsByTagName("Owner")  # only one owner pwer Content data 
            owner = Owner(self.get_name_from_node(ownernode[0], "DisplayName"),
                          self.get_name_from_node(ownernode[0], "ID"))
            contents = Contents(owner,
                               self.get_name_from_node(contentnode, "Key"),
                               self.get_name_from_node(contentnode, "LastModified"),
                               self.get_name_from_node(contentnode, "ETag"),
                               self.get_name_from_node(contentnode, "Size"),
                               self.get_name_from_node(contentnode, "StorageClass"))
            
            listbucket.append(contents)
            
        return listbucket
    
    
    def to_bulk_put_result(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        jobid = self.get_attribute_from_node(doc, 'MasterObjectList', 'JobId')
        mobjlist = MasterObjectList(jobid)
        for object_node in doc.getElementsByTagName('Object'):
            # add each DS3 object to the master object list
            mobjlist.append(Object(object_node.getAttribute('Name'), object_node.getAttribute('Size')))
        
        return mobjlist
    
    def to_bulk_get_result(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        jobid = self.get_attribute_from_node(doc, 'MasterObjectList', 'JobId')
        mobjlist = MasterObjectList(jobid)
        for object_node in doc.getElementsByTagName("Object"):
            # add each DS3 object to the master object list
            mobjlist.append(Object(object_node.getAttribute('Name'), object_node.getAttribute('Size')))
        
        return mobjlist
        
    def to_get_jobs(self, xml_string):
        doc = self.parse_string(xml_string)
        jobs = Jobs()
        for job_node in doc.getElementsByTagName("Job"):
            jobinfo = JobInfo(job_node.getAttribute('BucketName'),
                                  job_node.getAttribute('JobId'),
                                  job_node.getAttribute('Priority'),
                                  job_node.getAttribute('RequestType'),
                                  job_node.getAttribute('StartDate'))
            jobs.append(jobinfo)
                
        return jobs
    
    def to_get_job(self, xml_string):
        doc = self.parse_string(xml_string)
        for job_node in doc.getElementsByTagName("Job"):
            jobinfo = JobInfo(job_node.getAttribute('BucketName'),
                              job_node.getAttribute('JobId'),
                              job_node.getAttribute('Priority'),
                              job_node.getAttribute('RequestType'),
                              job_node.getAttribute('StartDate'))
            job = Job(jobinfo)
        
        # parse the objects on a per chunk basis
        for objs_node in doc.getElementsByTagName("Objects"):
            chunk = objs_node.getAttribute('ChunkNumber')
            serverid = objs_node.getAttribute('ServerId')
            jobjlist = JobObjectList(chunk, serverid)
            for jobj in objs_node.getElementsByTagName("Object"):
                jobjlist.append(JobObject(jobj.getAttribute('Name'), 
                                         jobj.getAttribute('Size'),
                                         jobj.getAttribute('State')))
        
            job.append(jobjlist)
            
        return job


class Credentials(object):
    def __init__(self, accessId, key):
        self.accessId = accessId.strip()
        self.key = key.strip()
        
    def is_valid(self):
        return True if self.accessId and self.key else False


class HttpVerb(object):
    """ HttpVerbs as Enums """
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    POST = 'POST'
    
class HeadBucketStatus(object):
    """Head bucket return values"""
    EXISTS = 'EXISTS'  # 200
    NOTAUTHORIZED = 'NOTAUTHORIZED' # 403
    DOESNTEXIST = 'DOESNTEXIST' # 404
    UNKNOWN = 'UNKNOWN'
    
class RequestInvalid(Exception):
    def __init__(self, summary):
        self.summary = summary
        
    def __str__(self):
        return repr(self.summary)
      
class RequestFailed(Exception):
    def __init__(self, summary, ds3error):
        self.summary = summary
        self.code = ds3error.code
        self.httperrorcode = ds3error.httperrorcode
        self.message = ds3error.message
        
    def __str__(self):
        return '{0} \n Code={1} \n HttpError={2} \n {3}'.format(self.summary, self.code, 
                                                                self.httperrorcode, self.message)
    
class AbstractRequest(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        self.path = '/'
        self.httpverb = HttpVerb.GET
        self.queryparams = {}
        self.headers = {}
        self.body = None


    def join_paths(self, path1, path2):
        final_path = ''
        if not path1.startswith('/'):
            final_path += '/'
            final_path += path1
        else:
            final_path += path1

        if path1.endswith('/') and path2.startswith('/'):
            final_path += path2[1:]
        elif path1.endswith('/'):
            final_path += path2
        else:
            final_path += '/' + path2
        return final_path


class AbstractResponse(object):
    __metaclass__ = ABCMeta
    def __init__(self, response, request):
        self.request = request
        self.response = response
        self.objectdata = None
        self.process_response(response)
    
    def process_response(self, response):
        # this method must be implemented
        raise NotImplementedError("Request Implemented")
    
    def __check_status_code__(self, expectedcode):
        self.statuscode = self.response.status
        if self.response.status != expectedcode:
            err = "Return Code: Expected %s - Received %s" % (expectedcode, self.response.status)
            ds3error = XmlSerializer().to_ds3error(self.response.read())
            raise RequestFailed(err, ds3error)
        
    def close(self):
        self.response.close()
     
class GetServiceRequest(AbstractRequest):
    def __init__(self):
        super(GetServiceRequest, self).__init__()
    
class GetServiceResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
        self.result = XmlSerializer().to_list_all_my_buckets_result(response.read())

        
class GetBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        super(GetBucketRequest, self).__init__()
        self.bucket = bucket
        self.path = self.join_paths('/', self.bucket)
        self.httpverb = HttpVerb.GET
        
    def with_marker(self, marker):
        """Key to start when listing objects"""
        self.queryparams['marker'] = marker
        
    def with_prefix(self, prefix):
        """Limits the objects to only those that start with this prefix"""
        self.queryparams['prefix'] = prefix
        
    def with_max_keys(self, maxkeys):
        """Max_keys limits the number of objects returned"""
        self.queryparams['max-keys'] = maxkeys
        
    
class GetBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
        self.result = XmlSerializer().to_get_bucket_result(response.read())
 
class PutBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        super(PutBucketRequest, self).__init__()
        self.bucket = bucket
        self.path = self.join_paths('/', self.bucket)
        self.httpverb = HttpVerb.PUT
           
class PutBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
                
class DeleteBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        super(DeleteBucketRequest, self).__init__()
        self.bucket = bucket
        self.path = self.join_paths('/', self.bucket)
        self.httpverb = HttpVerb.DELETE
        
class DeleteBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(204)
        
class HeadBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        super(HeadBucketRequest, self).__init__()
        self.bucket = bucket
        self.path = self.join_paths('/', self.bucket)
        self.httpverb = HttpVerb.HEAD
        
class HeadBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.statuscode = self.response.status
        if self.response.status == 200:
            self.result = HeadBucketStatus.EXISTS
        elif self.response.status == 403:
            self.result = HeadBucketStatus.NOTAUTHORIZED
        elif self.response.status == 404:
            self.result = HeadBucketStatus.DOESNTEXIST
        else:
            self.result = HeadBucketStatus.UNKNOWN
        
class PutObjectRequest(AbstractRequest):
    def __init__(self, bucket, filename, filedata):
        super(PutObjectRequest, self).__init__()
        self.bucket = bucket
        self.body = filedata
        self.path = self.join_paths(self.bucket, filename)
        self.httpverb = HttpVerb.PUT
    
class PutObjectResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)

class GetObjectRequest(AbstractRequest):
    def __init__(self, bucket, objectkey):
        super(GetObjectRequest, self).__init__()
        self.bucket = bucket
        self.objectkey = objectkey
    
        self.path = self.join_paths(self.bucket, self.objectkey)
        self.httpverb = HttpVerb.GET
        
    def with_range(self, startbyte, endbyte):
        self.headers['Range'] = 'bytes={0}-{1}'.format(startbyte, endbyte)
    
class GetObjectResponse(AbstractResponse):
    def process_response(self, reponse):
        self.__check_status_code__(200)
        self.objectdata = self.response.read()
        
class DeleteObjectRequest(AbstractRequest):
    def __init__(self, bucket, objectkey):
        super(DeleteObjectRequest, self).__init__()
        self.bucket = bucket
        self.objectkey = objectkey
        self.path = self.join_paths(self.bucket, self.objectkey)
        self.httpverb = HttpVerb.DELETE
    
class DeleteObjectResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(204)
        
class BulkRequest(AbstractRequest):
    """Base class for handling bulk gets and puts"""
    def __init__(self, bucket, objectlist):
        self.bucket = bucket
        objects = xmldom.Element('objects')
        for file_object in objectlist:
            obj_elm = xmldom.Element('object')
            obj_elm.set('name', posixpath.normpath(file_object.name))
            obj_elm.set('size', str(file_object.size))
            objects.append(obj_elm)
        self.objectlist = objects
        self.body = xmldom.tostring(objects)
        self.headers = {}
    
class BulkPutRequest(BulkRequest):
    def __init__(self, bucket, objectlist):
        super(BulkPutRequest, self).__init__(bucket, objectlist)
        self.path = self.join_paths('/_rest_/bucket/', self.bucket)
        self.httpverb = HttpVerb.PUT
        self.queryparams={"operation": "start_bulk_put"}
    
class BulkPutResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
        self.result = XmlSerializer().to_bulk_put_result(response.read())
        
class BulkGetRequest(BulkRequest):
    def __init__(self, bucket, objectlist):
        super(BulkGetRequest, self).__init__(bucket, objectlist)
        self.path = self.join_paths('/_rest_/bucket/', self.bucket)
        self.httpverb = HttpVerb.PUT
        self.queryparams={"operation": "start_bulk_get"}
    
class BulkGetResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
        self.result = XmlSerializer().to_bulk_get_result(response.read())
        
class GetJobsRequest(AbstractRequest):
    def __init__(self, bucket):
        super(GetJobsRequest, self).__init__()
        self.path = '/_rest_/job/'
        self.queryparams={'bucket': bucket}
        self.httpverb = HttpVerb.GET
            
class GetJobsResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
        self.result = XmlSerializer().to_get_jobs(response.read())
        
class GetJobRequest(AbstractRequest):
    def __init__(self, jobid):
        super(GetJobRequest, self).__init__()
        self.path = self.join_paths('/_rest_/job/', jobid)
        self.httpverb = HttpVerb.GET
            
class GetJobResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
        self.result = XmlSerializer().to_get_job(response.read())
        
class CancelJobRequest(AbstractRequest):
    def __init__(self, jobid):
        super(CancelJobRequest, self).__init__()
        self.path = self.join_paths('/_rest_/job/', jobid)
        self.httpverb = HttpVerb.DELETE
            
class CancelJobResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
     
class ModifyJobRequest(AbstractRequest):
    def __init__(self, jobid, priority):
        super(ModifyJobRequest, self).__init__()
        self.path = self.join_paths('/_rest_/job/', jobid)
        self.queryparams={'priority': priority}
        self.httpverb = HttpVerb.GET
            
class ModifyJobResponse(AbstractResponse):
    def process_response(self, response):
        self.__check_status_code__(200)
        self.result = XmlSerializer().to_get_job(response.read())
   

class ListAllMyBucketsResult(object):
    def __init__(self, owner):
        self.owner = owner
        self.buckets = []
        
    def append(self, bucket):
        if not isinstance(bucket, Bucket):
            raise TypeError("Can only append a DS3 Bucket")
        
        self.buckets.append(bucket)
        
    def __len__(self):
        return len(self.buckets)
    
    
class ListBucketResult(object):
    def __init__(self, name, prefix, marker, maxkeys, istruncated, creationdate, delimiter, nextmarker):
        self.name = name
        self.prefix = prefix
        self.marker = marker
        self.maxkeys = maxkeys
        self.istruncated = istruncated
        self.creationdate = creationdate
        self.delimiter = delimiter
        self.nextmarker = nextmarker
        self.contentslist = []
        
    def append(self, contents):
        if not isinstance(contents, Contents):
            raise TypeError("Can only append a DS3 Contents Object")
        
        self.contentslist.append(contents)
        
    def __str__(self):
        return 'Name={0} Prefix={1} Marker={2} MaxKeys={3} isTruncated={4} ' \
                'CreationDate={5} Delimiter={6} NextMarker={7}'.format(self.name, self.prefix, self.marker, self.maxkeys, 
                                                                       self.istruncated, self.creationdate, self.delimiter, 
                                                                       self.nextmarker, len(self.contentslist))  
  
class Contents(object):
    def __init__(self, owner, key, lastmodified, etag, size, storageclass):
        if not isinstance(owner, Owner):
            raise TypeError("Contents must be created with Owner object")
 
        self.owner = owner
        self.key = key
        self.lastmodified = lastmodified
        self.etag = etag
        self.size = size
        self.storageclass = storageclass
        
    def __str__(self):
        return '{0} Key={1} LastModified={2} Etag={3} Size={4} StorageClass={5}'.format(self.owner, self.key, self.lastmodified, 
                                                                                        self.etag, self.size, self.storageclass)
        
class Bucket(object):
    def __init__(self, name, creationdate=None):
        self.name = name
        self.creationdate = creationdate
        
    def __str__(self):
        return 'Name={0} CreationDate={1}'.format(self.name, self.creationdate)
   
class Owner(object):
    """Bucket Owner meta data"""
    def __init__(self, displayname, ownerid):
        self.displayname = displayname
        self.ownerid = ownerid
        
    def __str__(self):
        return 'DisplayName={0} OwnerId={1}'.format(self.displayname, self.ownerid)
              
class Ds3Error(object):
    def __init__(self, code, httperrorcode, message):
        self.code = code
        self.httperrorcode = httperrorcode
        self.message = message

class Object(object):
    """DS3 Object is metadata"""
    def __init__(self, name, size):
        self.name = name
        self.size = size
        
    def __str__(self):
        return 'Name={0} Size={1}'.format(self.name, self.size)
            
class MasterObjectList(object):
    def __init__(self, jobid=None):
        # This is a list of DS3 Objects
        self.objectlist = []
        self.jobid = jobid
    def append(self, ds3obj):
        if not isinstance(ds3obj, Object):
            raise TypeError("Can only append a DS3 Object")
        self.objectlist.append(ds3obj)
                   
class Jobs(object):
    def __init__(self):
        self.joblist = []
        
    def append(self, obj):
        if not isinstance(obj, JobInfo):
            raise TypeError("Can only append JobInfo Objects")
            
        self.joblist.append(obj)
    
class JobInfo(object):
    def __init__(self, bucketname, jobid, priority, jobtype, startdate):
        self.bucketname = bucketname
        self.jobid = jobid
        self.priority = priority
        self.jobtype = jobtype
        self.startdate = startdate
    def __str__(self):
        return 'BucketName={0} JobId={1} Priority={2} StartDate={3}'.format(self.bucketname, self.jobid, self.priority, self.startdate)
   
class JobObjectList(object):
    """JobObjectList is a container for DS3 JobObjects.   
        The DS3 object container has attributes for Chunk number and DS3 server hostname/address.  
    """
    def __init__(self, chunk, serverid):
        self.chunknumber = chunk
        self.serverid = serverid
        self.jobobjects = []
    def append(self, ds3obj):
        if not isinstance(ds3obj, JobObject):
            raise TypeError("Can only append a DS3 JobObject")
        
        self.jobobjects.append(ds3obj)
        
    def __str__(self):
        return 'ChunkNumber={0} ServerId={1} JobObjects={2}'.format(self.chunknumber, self.serverid, len(self.jobobjects))
 
class JobObject(object):
    """DS3 Job Object metadata"""
    def __init__(self, name, size, state):
        self.name = name
        self.size = size
        self.state = state
        
    def __str__(self):
        return 'Name={0} Size={1} State={2}'.format(self.name, self.size, self.state)
        
class Job(object):
    def __init__(self, jobinfo):
        if not isinstance(jobinfo, JobInfo):
            raise TypeError("Can only init a Job with a JobInfo object")
        
        self.jobinfo = jobinfo
        self.jobobjectlists = []  # list of ObjectList
    def append(self, jobjlist):
        if not isinstance(jobjlist, JobObjectList):
            raise TypeError("Can only append JobObjectList Objects")
            
        self.jobobjectlists.append(jobjlist)
        
    def __str__(self):
        return '{0}, JobObjectLists={1}'.format(self.jobinfo, len(self.jobobjectlists))

class Client(object):
    def __init__(self, endpoint, credentials):
        self.netclient = NetworkClient(endpoint, credentials)

    def get_netclient(self):
        return self.netclient
    
    def get_service(self, request):
        return GetServiceResponse(self.netclient.get_response(request), request)

    def get_bucket(self, request):
        return GetBucketResponse(self.netclient.get_response(request), request)
  
    def head_bucket(self, request):
        return HeadBucketResponse(self.netclient.get_response(request), request)

    def put_bucket(self, request):
        return PutBucketResponse(self.netclient.get_response(request), request)

    def delete_bucket(self, request):
        return DeleteBucketResponse(self.netclient.get_response(request), request)
        
    def get_object(self, request):
        return GetObjectResponse(self.netclient.get_response(request), request)

    def put_object(self, request):
        return PutObjectResponse(self.netclient.get_response(request), request)

    def delete_object(self, request):
        return DeleteObjectResponse(self.netclient.get_response(request), request)
    
    def bulk_put(self, request):
        return BulkPutResponse(self.netclient.get_response(request), request)
        
    def bulk_get(self, request):
        return BulkGetResponse(self.netclient.get_response(request), request)
    
    def get_jobs(self, request):
        return GetJobsResponse(self.netclient.get_response(request), request)
 
    def get_job(self, request):
        return GetJobResponse(self.netclient.get_response(request), request)
 
    def cancel_job(self, request):
        return CancelJobResponse(self.netclient.get_response(request), request)
 
    def modify_job(self, request):
        return ModifyJobResponse(self.netclient.get_response(request), request)
    
class NetworkClient(object):
    def __init__(self, endpoint, credentials):
        self.networkconnection = NetworkConnection(endpoint)
        self.credentials = credentials
        self.maxredirects = 5
        self.secure = False  # the default is HTTP. If true use HTTPS
        self.proxy = None
    
    def with_secure(self, secure):
        """If true the client will use HTTPS instead of HTTP."""
        self.secure = secure
        return self
    
    def with_proxy(self, proxy):
        """Set HTTP proxy"""
        index = proxy.find('://')
        if index >= 0:
            self.proxy = proxy[index+3:]
        else:
            self.proxy = proxy
        return self
        
    def with_max_redirects(self, maxredirects):
        """Set the maximum 307 redirects the SDK will automatically handle before throwing an exception.""" 
        self.maxredirects = maxredirects
        return self
    
    def get_response(self, request):
        retrycnt = 0
        response = self.send_request(request)
        
        # if needed, loop to handle 307 redirects 
        while response.status == 307 and retrycnt < self.maxredirects:
            retrycnt += 1
            response = self.send_request(request)
             
        return response
    
    def send_request(self, request):
        """create http or https connectiong and send the DS3 request."""
        if self.secure:
            connection = httplib.HTTPSConnection(self.networkconnection.endpoint)
        else:
            connection = httplib.HTTPConnection(self.networkconnection.endpoint)
            
        #use proxy if one was specified
        if self.proxy:
            connection.set_tunnel(self.proxy)
            
        date = self.get_date()
        path = request.path
        if request.queryparams:
            path = self.build_path(request.path, request.queryparams)
            
        headers = {}
        headers['Host'] = self.networkconnection.hostname +":"+ str(self.networkconnection.port)
        headers['Date'] = date
        # add additonal header information if specficied in the request. This might be a byte range for example
        if request.headers:
            headers.update(request.headers)
            
        if request.httpverb == HttpVerb.PUT:
            headers['Content-Type'] = 'application/octet-stream'
            headers['Authorization'] = self.build_authorization( verb=request.httpverb, date=date, 
                                                                 content_type='application/octet-stream', resource=request.path)
            connection.request(request.httpverb, path, body=request.body, headers=headers)
        else:
            headers['Authorization'] = self.build_authorization(verb=request.httpverb, date=date, resource=request.path)
            connection.request(request.httpverb, path, headers=headers)
            
        return connection.getresponse()
     
    
    def build_authorization(self, verb='', date='', content_type='', resource=''):
        ###Build the S3 authorization###
        signature = self.aws_signature(self.credentials.key, verb=verb, content_type=content_type,
                                  date=date, canonicalized_resource=resource)
        return 'AWS ' + self.credentials.accessId + ':' + signature
    
    def aws_signature(self, key, verb='GET', md5='', content_type='', date='', canonicalized_amz_header='', canonicalized_resource=''):
        ###compute and sign S3 signature###
        signature_string = verb + '\n'
        signature_string += md5 + '\n'
        signature_string += content_type+ '\n'
        signature_string += date + '\n'
        signature_string += canonicalized_amz_header
        signature_string += canonicalized_resource
        return self.sign(key, signature_string)
    
    def sign(self, key, contents):
        signer = hmac.new(key.encode('utf-8'), digestmod=sha1)
        signer.update(contents)
        digest = signer.digest()
        return base64.encodestring(digest).strip().decode('utf-8')

    def build_path(self, resource, query_params={}):
        if len(query_params) == 0:
            return resource
        new_path = resource + '?'

        new_path += '&'.join(map(lambda tupal: (tupal[0] + '=' + tupal[1]), 
                                 query_params.iteritems()))
        return new_path

    def get_date(self):
        return formatdate()

class NetworkConnection(object):
    """
    This class abstracts the HTTP network connection from the client to the server.
    """
    def __init__(self, endpoint):
        self.url = urlparse.urlparse(self.ensure_schema(endpoint))
        self.hostname = self.url.hostname
        self.port = self.url.port
        self.endpoint = endpoint
        
    def ensure_schema(self, endpoint):
        if endpoint.startswith('http'):
            return endpoint
        else:
            return 'http://' + endpoint
