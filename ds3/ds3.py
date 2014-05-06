import os.path

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
    def __init__(self, verbose=None):
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
                # this is not the node we are looking for
                continue
            
            for node2 in node.childNodes:
                if node2.nodeType == Node.TEXT_NODE:
                    return node2.data
                
        return ''
    
    def get_attribute_from_node(self, doc, nodename, attribute):
        node = doc.getElementsByTagName(nodename)
        
        return node[0].getAttribute(attribute)
        
    def to_ds3error(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        obj = Ds3Error()

        obj.code = self.get_name_from_node(doc, "Code")
        obj.httperrorcode = self.get_name_from_node(doc, "HttpErrorCode")
        obj.message = self.get_name_from_node(doc, "Message")
        
        return obj
        
    def to_list_all_my_buckets_result(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        obj = ListAllMyBucketsResult()
         
        for node in doc.getElementsByTagName("Bucket"):
            bucket = self.get_name_from_node(node, "Name")
            cdate = self.get_name_from_node(node, "CreationDate")
            obj.add_bucket(bucket, cdate)
            
        for node in doc.getElementsByTagName("Owner"):
            name = self.get_name_from_node(node, "DisplayName")
            oid = self.get_name_from_node(node, "ID")
            obj.add_owner(name, oid)
            
        return obj
                    
    def to_get_bucket_result(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        obj = ListBucketResult()
        
        obj.name = self.get_name_from_node(doc, "Name")
        obj.prefix = self.get_name_from_node(doc, "Prefix")
        obj.marker = self.get_name_from_node(doc, "Marker")
        obj.maxkeys = self.get_name_from_node(doc, "MaxKeys")
        obj.istruncated = self.get_name_from_node(doc, "IsTruncated")
        obj.creationdate = self.get_name_from_node(doc, "CreationDate")
        obj.delimiter = self.get_name_from_node(doc, "Delimiter")
        obj.nextmarker = self.get_name_from_node(doc, "NextMarker")
        
        for node in doc.getElementsByTagName("Contents"):
            content = Contents()
            content.key = self.get_name_from_node(node, "Key")
            content.lastmodified = self.get_name_from_node(node, "LastModified")
            content.etag = self.get_name_from_node(node, "ETag")
            content.size = self.get_name_from_node(node, "Size")
            content.storageclass = self.get_name_from_node(node, "StorageClass")
            for node3 in node.getElementsByTagName("Owner"):
                displayname = self.get_name_from_node(node3, "DisplayName")
                ownerid = self.get_name_from_node(node3, "ID")
                content.add_owner(Owner(displayname, ownerid))
            
            obj.add_contents(content)
            
        return obj
    
        
    def to_get_object_result(self, xml_string):
        print xml_string
        return None
    
    def to_bulk_put_result(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        obj = MasterObjectList()
        print xml_string
        obj.jobid = self.get_attribute_from_node(doc, 'masterobjectlist', 'jobid')
        for node in doc.getElementsByTagName("object"):
                oo = Object()
                oo.name = node.getAttribute('name')
                oo.size = node.getAttribute('size')
                if oo.name and oo.size:
                    obj.append(oo)
        
        return obj
    
    def to_bulk_get_result(self, xml_string):
        doc = xml.dom.minidom.parseString(xml_string)
        obj = MasterObjectList()
        print xml_string
        obj.jobid = self.get_attribute_from_node(doc, 'masterobjectlist', 'jobid')
        for node in doc.getElementsByTagName("object"):
                oo = Object()
                oo.name = node.getAttribute('name')
                oo.size = node.getAttribute('size')
                if oo.name and oo.size:
                    obj.append(oo)
        
        return obj
        
    def to_get_jobs(self, xml_string):
        doc = self.parse_string(xml_string)
        obj = Primes()
        for node in doc.getElementsByTagName("Prime"):
                p = Prime()
                p.active = bool(self.get_name_from_node(node,'Active', 'Prime'))
                p.id = self.get_name_from_node(node, 'Id', 'Prime')
                p.bucketid = self.get_name_from_node(node, 'BucketId', 'Prime')
                p.requesttype = self.get_name_from_node(node,'RequestType', 'Prime')
                p.createdat = self.get_name_from_node(node,'CreatedAt', 'Prime')
                obj.append(p)      
                
        return obj
    
    def to_get_job(self, xml_string):
        doc = self.parse_string(xml_string)
        return None

    def to_delete_job(self, xml_string):
        doc = self.parse_string(xml_string)
        return None


class Credentials(object):
    def __init__(self, accessId, key):
        self.accessId = accessId.strip()
        self.key = key.strip()
        
    def get_accessId(self):
        return self.accessId
        
    def get_key(self):
        return self.key
        
    def isValid(self):
        if self.accessId and self.key:
            return True
        else:
            return False             


class HttpVerb(object):
    """ HttpVerbs as Enums """
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    POST = 'POST'
    
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
        return repr(self.summary)
    
class RequestNotImplemented(Exception):
    def __init__(self, summary):
        self.summary = summary
        
    def __str__(self):
        return repr(self.summary)
    
class AbstractRequest(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        self.path = '/'
        self.httpverb = HttpVerb.GET
        self.queryparams = {}
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
        self.process_response(response)
    
    def process_response(self, response):
        # this method must be implemented
        raise RequestNotImplemented("Not Implemented")
    
    def check_status_code(self, expectedcode):
        if self.response.status != expectedcode:
            err = "Return Code: Expected %s - Received %s" % (expectedcode, self.response.status)
            ds3error = XmlSerializer().to_ds3error(self.response.read())
            raise RequestFailed(err, ds3error)
        
    def close(self):
        self.response.close()
     
class GetServiceRequest(AbstractRequest):
    def __init__(self):
        self.path = '/'
        self.httpverb = HttpVerb.GET
    
class GetServiceResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer(True).to_list_all_my_buckets_result(response.read())

        
class GetBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        self.bucket = bucket
        self.path = self.join_paths('/', self.bucket)
        self.httpverb = HttpVerb.GET
        
    def with_next_marker(self, nextMarker):
        self.queryparams['marker'] = nextMarker
        
    def with_prefix(self, prefix):
        self.queryparams['prefix'] = prefix
        
    
class GetBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_get_bucket_result(response.read())
 
class PutBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        self.bucket = bucket
        self.path = self.join_paths('/', self.bucket)
        self.httpverb = HttpVerb.PUT
        self.body = None
           
class PutBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        #self.result = XmlSerializer(True).to_put_bucket_result(response.read())
                
class DeleteBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        self.bucket = bucket
        self.path = self.join_paths('/', self.bucket)
        self.httpverb = HttpVerb.DELETE
        
class DeleteBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(204)
        
class PutObjectRequest(AbstractRequest):
    def __init__(self, bucket, filepath):
        
        if not os.path.isfile(filepath):
            raise RequestInvalid("Object %s is not a file" % filepath)
        
        filename = posixpath.normpath(filepath)
        self.bucket = bucket
        self.objectkey = open(filename, 'rb')
        self.body = self.objectkey.read() 
        self.path = self.join_paths(self.bucket, filename)
        self.httpverb = HttpVerb.PUT
    
class PutObjectResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)

class GetObjectRequest(AbstractRequest):
    def __init__(self, bucket, objectkey, destination):
        self.bucket = bucket
        self.objectkey = objectkey
        #os.sep
        self.destination = os.path.join(os.path.normpath(destination), os.path.normpath(objectkey))
        if not os.path.exists(os.path.dirname(self.destination)):
            os.makedirs(os.path.dirname(self.destination))
    
        self.path = self.join_paths(self.bucket, self.objectkey)
        self.httpverb = HttpVerb.GET
    
class GetObjectResponse(AbstractResponse):
    def process_response(self, reponse):
        self.check_status_code(200)
        output = open(self.request.destination, 'wb')
        output.write(self.response.read())
        
class DeleteObjectRequest(AbstractRequest):
    def __init__(self, bucket, objectkey):
        self.bucket = bucket
        self.objectkey = objectkey
        self.path = self.join_paths(self.bucket, self.objectkey)
        self.httpverb = HttpVerb.DELETE
    
class DeleteObjectResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(204)
        
class BulkRequest(AbstractRequest):
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
    
class BulkPutRequest(BulkRequest):
    def __init__(self, bucket, objectlist):
        super(BulkPutRequest, self).__init__(bucket, objectlist)
        self.path = self.join_paths('/_rest_/buckets/', self.bucket)
        self.httpverb = HttpVerb.PUT
        self.queryparams={"operation": "start_bulk_put"}
    
class BulkPutResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_bulk_put_result(response.read())
        
class BulkGetRequest(BulkRequest):
    def __init__(self, bucket, objectlist):
        super(BulkGetRequest, self).__init__(bucket, objectlist)
        self.path = self.join_paths('/_rest_/buckets/', self.bucket)
        self.httpverb = HttpVerb.PUT
        self.queryparams={"operation": "start_bulk_get"}
    
class BulkGetResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_bulk_get_result(response.read())
        
class GetJobsRequest(AbstractRequest):
    def __init__(self, bucket):
        self.path = '/_rest_/job/'
        self.queryparams={"bucket", bucket}
        self.httpverb = HttpVerb.GET
            
class GetJobsResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer(True).to_get_jobs(response.read())
        
class GetJobRequest(AbstractRequest):
    def __init__(self, jobid):
        self.path = self.join_paths('/_rest_/job/', jobid)
        self.httpverb = HttpVerb.GET
            
class GetJobResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer(True).to_get_job(response.read())
        
class DeleteJobRequest(AbstractRequest):
    def __init__(self, jobid):
        self.path = self.join_paths('/_rest_/job/', jobid)
        self.httpverb = HttpVerb.DELETE
            
class DeleteJobResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(204)
        
class ListAllMyBucketsResult(object):
    def __init__(self):
        self.buckets = []
    
    def add_bucket(self, name, creationdate):
        self.buckets.append(Bucket(name, creationdate))
    
    def get_buckets(self):
        return self.buckets
    
    def add_owner(self, displayname, ownerid):
        self.owner = Owner(displayname, ownerid)
        
    def len(self):
        return len(self.buckets)
    
    
class ListBucketResult(object):
    def __init__(self):
        self.name = ''
        self.prefix = ''
        self.marker = ''
        self.maxkeys = ''
        self.istruncated = False
        self.creationdate = ''
        self.delimiter = ''
        self.nextmarker = ''
        self.contentslist = []
        
    def add_contents(self, contents):
        self.contentslist.append(contents)
        
    def get_contents(self):
        return self.contentslist
  
class Contents(object):
    def __init__(self):
        self.key = ''
        self.lastmodified = ''
        self.etag = ''
        self.size = 0
        self.storageclass = ''
        
    def add_owner(self, owner):
        self.owner = owner
    

class Bucket(object):
    def __init__(self, name=None, creationdate=None):
        self.name = name
        self.creationdate = creationdate
   
class Owner(object):
    def __init__(self, displayname=None, ownerid=None):
        self.displayname = displayname
        self.ownerid = ownerid
              
class Ds3Error(object):
    def __init__(self, code=None, httperrorcode=None, message=None):
        self.code = code
        self.httperrorcode = httperrorcode
        self.message = message

class Object(object):
    def __init__(self, name=None, size=None):
        self.name = name
        self.size = size
            
class MasterObjectList(object):
    def __init__(self, jobid=None):
        # This is a list of DS3Objects
        self.objectlist = []
        self.jobid = jobid
    def append(self, ds3obj):
        self.objectlist.append(ds3obj)
        return

class Primes(object):
    def __init__(self):
        self.primes = []
    def append(self, obj):
        if isinstance(obj, Prime):
            self.primes.append(obj)
        
class Prime(object):
    def __init__(self, active=None, requesttype=None, primeid=None, bucketid=None, createdat=None):
        self.active = active
        self.requesttype = requesttype
        self.id = primeid
        self.bucketid = bucketid
        self.createdat = createdat
        
    def add_bucket(self, bucket):
        if isinstance(bucket, Bucket):
            self.bucket = bucket
            
class Job(object):
    def __init__(self, active=None, filesystemid=None, jid=None, orderindex=None, 
                 primeid=None, size=None, state=None, virtualpageindex=None):
        self.active = False
        self.filesystemid = filesystemid
        self.jid = jid
        self.orderindex= orderindex
        self.primeid = primeid
        self.size = size
        self.state = state
        self.virtualpageindex = virtualpageindex

class Client(object):
    def __init__(self, endpoint, credentials):
        self.netclient = NetworkClient(endpoint, credentials)

    def get_netclient(self):
        return self.netclient
    
    def get_service(self, request):
        return GetServiceResponse(self.netclient.get_response(request), request)

    def get_bucket(self, request):
        return GetBucketResponse(self.netclient.get_response(request), request)

    def put_bucket(self, request):
        return PutBucketResponse(self.netclient.get_response(request), request)

    def delete_bucket(self, request):
        return DeleteBucketResponse(self.netclient.get_response(request), request)
        
    def get_object(self, request):
        return GetObjectResponse(self.netclient.get_response(request), request)

    def put_object(self, request):
        return PutObjectResponse(self.netclient.put(request), request)

    def delete_object(self, request):
        return DeleteObjectResponse(self.netclient.get_response(request), request)
    
    def bulk_put(self, request):
        return BulkPutResponse(self.netclient.bulk(request), request)
        
    def bulk_get(self, request):
        return BulkGetResponse(self.netclient.bulk(request), request)
    
    def get_jobs(self, request):
        return GetJobsResponse(self.netclient.get_response(request), request)
 
    def get_job(self, request):
        return GetJobResponse(self.netclient.get_response(request), request)
 
    def delete_job(self, request):
        return DeleteJobResponse(self.netclient.get_response(request), request)
 
class NetworkClient(object):
    def __init__(self, endpoint, credentials):
        self.networkconnection = NetworkConnection(endpoint)
        self.credentials = credentials
        self.maxredirects = 5
    
    def with_http_secure(self):
        return
    
    def with_proxy(self, proxy):
        index = proxy.find('://')
        if index >= 0:
            self.proxy = proxy[index+3:]
        else:
            self.proxy = proxy
        
    def with_max_redirects(self, maxredirects):
        self.maxredirects = maxredirects
        
    def get_response(self, request):
        cnt = 0
        r = self.send_request(request)
        while r.status == 307 and cnt < self.maxredirects:
            print 'redirecting.....'
            cnt += 1
            r = self.send_request(request)
             
        return r
           
    def send_request(self, request):
        #opener = urllib2.build_opener(VerboseHTTPHandler)
        connection = httplib.HTTPConnection(self.networkconnection.endpoint)
        date = self.get_date()
        headers = {}
        headers['Host'] = self.networkconnection.hostname +":"+ str(self.networkconnection.port)
        headers['Date'] = date
        if request.httpverb == HttpVerb.PUT:
            headers['Content-Type'] = 'application/octet-stream'
            headers['Authorization'] = self.build_authorization( verb=request.httpverb, date=date, 
                                                                 content_type='application/octet-stream', resource=request.path)
            connection.request(request.httpverb, request.path, body=request.body, headers=headers)
        else:
            headers['Authorization'] = self.build_authorization(verb=request.httpverb, date=date, resource=request.path)
            connection.request(request.httpverb, request.path, headers=headers)
            
        return connection.getresponse()
            
    def put(self, request):
        #opener = urllib2.build_opener(VerboseHTTPHandler)
        #connection = opener.open(self.networkconnection.url)
        connection = httplib.HTTPConnection(self.networkconnection.endpoint)
        date = self.get_date()
        headers = {}
        headers['Host'] = self.networkconnection.hostname +":"+ str(self.networkconnection.port)
        headers['Date'] = date
        headers['Content-Type'] = 'application/octet-stream'
        headers['Authorization'] = self.build_authorization(
            verb=request.httpverb, date=date, content_type='application/octet-stream', resource=request.path)
            #verb=request.httpverb, date=date, resource=request.path)
        #s = request.objectdata.read()
        connection.request(request.httpverb, request.path, body=request.body, headers=headers)
            
        return connection.getresponse()      
    
    def bulk(self, request):
        #opener = urllib2.build_opener(VerboseHTTPHandler)
        #connection = opener.open(self.networkconnection.url)
        connection = httplib.HTTPConnection(self.networkconnection.endpoint)
        date = self.get_date()
        headers = {}
        headers['Host'] = self.networkconnection.hostname +":"+ str(self.networkconnection.port)
        headers['Date'] = date
        headers['Content-Type'] = 'application/octet-stream'
        headers['Authorization'] = self.build_authorization(
            verb=request.httpverb, date=date, content_type='application/octet-stream', resource=request.path)
        path = self.build_path(request.path, request.queryparams)
        connection.request(request.httpverb, path, body=request.body, headers=headers)
            
        return connection.getresponse()
    
    def build_authorization(self, verb='', date='', content_type='', resource=''):
        signature = self.aws_signature(self.credentials.key, verb=verb, content_type=content_type,
                                  date=date, canonicalized_resource=resource)
        return 'AWS ' + self.credentials.accessId + ':' + signature
    
    def aws_signature(self, key, verb='GET', md5='', content_type='', date='', canonicalized_amz_header='', canonicalized_resource=''):
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
    
class VerboseHTTPResponse(httplib.HTTPResponse):
    def _read_status(self):
        s = self.fp.read()
        print '-' * 20, 'Response', '-' * 20
        print s.split('\r\n\r\n')[0]
        self.fp = StringIO.StringIO(s)
        return httplib.HTTPResponse._read_status(self)
    
class VerboseHTTPConnection(httplib.HTTPConnection):
    response_class = VerboseHTTPResponse
    def send(self, s):
        print '-' * 50
        print s.strip()
        httplib.HTTPConnection.send(self, s)

class VerboseHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return self.do_open(VerboseHTTPConnection, req)


class NetworkConnection(object):
    """
    This class abstracts the HTTP network connection from the client to the server.
    """
    def __init__(self, endpoint, proxy=None):
        self.url = urlparse.urlparse(self.ensure_schema(endpoint))
        self.proxy = proxy
        self.hostname = self.url.hostname
        self.port = self.url.port
        self.endpoint = endpoint
        
    def ensure_schema(self, endpoint):
        if endpoint.startswith('http'):
            return endpoint
        else:
            return 'http://' + endpoint
