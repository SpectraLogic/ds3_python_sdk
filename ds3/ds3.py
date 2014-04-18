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
 

class XmlSerializer(object):
    
    def get_name_from_node(self, doc, nodename):
        for node in doc.getElementsByTagName(nodename):
            for node2 in node.childNodes:
                if node2.nodeType == Node.TEXT_NODE:
                    return node2.data
                
        return ''
    
    def get_attribute_from_node(self, doc, nodename, attribute):
        
        return ''
        
    def to_ds3error(self, xml_string):
        obj = Ds3Error()
        doc = xml.dom.minidom.parseString(xml_string)
        
        obj.code = self.get_name_from_node(doc, "Code")
        obj.httperrorcode = self.get_name_from_node(doc, "HttpErrorCode")
        obj.message = self.get_name_from_node(doc, "Message")
        
        return obj
        
    def to_list_all_my_buckets_result(self, xml_string):
        obj = ListAllMyBucketsResult()
        doc = xml.dom.minidom.parseString(xml_string)
        
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
        obj = ListBucketResult()
        doc = xml.dom.minidom.parseString(xml_string)
        
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
        obj = ListBucketResult()
        doc = xml.dom.minidom.parseString(xml_string)
        obj.jobid = self.get_attribute_from_node(doc, 'masterobjectlist', 'jobid')
        
        print xml_string
        return None
            
    
def pretty_print_xml(xml_string):
    print xml.dom.minidom.parseString(xml_string).toprettyxml()

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

'''
====================================================================
HttpVerb
  Static class for http verbs
'''
class HttpVerb(object):
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
    def __init__(self, response, request=None):
        self.request = request
        self.response = response
        self.process_response(response)
    
    def process_response(self, response):
        # this method must be implemented
        raise RequestNotImplemented("Not Implemented")
    
    def print_xml(self):
        pretty_print_xml(self.response.read())

    def check_status_code(self, expectedcode):
        if self.response.status != expectedcode:
            ds3error = XmlSerializer().to_ds3error(self.response.read())
            err = "Return Code: Expected %s - Received %s" % (expectedcode, self.response.status)
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
        self.result = XmlSerializer().to_list_all_my_buckets_result(response.read())

        
class GetBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        self.bucket = bucket
        #self.nextmarker = ''
        #self.prefix = ''
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
           
class PutBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
                
class DeleteBucketRequest(AbstractRequest):
    def __init__(self, bucket):
        self.bucket = bucket
        self.path = self.join_paths('/', self.bucket)
        self.httpverb = HttpVerb.DELETE
        
class DeleteBucketResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(204)
        
class PutObjectRequest(AbstractRequest):
    def __init__(self, bucket, objectkey):
        if not os.path.isfile(objectkey):
            raise RequestInvalid("Object %s is not a file" % objectkey)
        
        self.bucket = bucket
        self.objectkey = objectkey
        print "Put Object", objectkey, "is", os.path.getsize(objectkey)
        self.objectdata = open(objectkey) 
        self.path = self.join_paths(self.bucket, self.objectkey)
        self.httpverb = HttpVerb.PUT
    
class PutObjectResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)

class GetObjectRequest(AbstractRequest):
    def __init__(self, bucket, objectkey, destination):
        self.bucket = bucket
        self.objectkey = objectkey
        self.destination = destination
        self.path = self.join_paths(self.bucket, self.objectkey)
        self.httpverb = HttpVerb.GET
    
class GetObjectResponse(AbstractResponse):
    def process_response(self, reponse):
        self.check_status_code(200)
        output = open(self.request.destination, 'w')
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
            obj_elm.set('name', file_object.name)
            obj_elm.set('size', str(file_object.size))
            objects.append(obj_elm)
        self.objectlist = objects
        self.body = xmldom.tostring(objects)
    
class BulkPutRequest(AbstractRequest):
    def __init__(self, bucket, objectlist):
        super(BulkPutRequest, self).__init__(bucket, objectlist)
        self.path = self.join_paths('/_rest_/buckets/', self.bucket)
        self.httpverb = HttpVerb.PUT
        self.queryparams={"operation": "start_bulk_put"}
    
class BulkPutResponse(AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.response = XmlSerializer().to_bulk_put_result(response.read())
        
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
    def __init__(self, name, size=None):
        self.name = name
        if size == None:
            self.size = os.path.getsize(name)
        else:
            self.size = size
            
class MasterObjectList(object):
    def __init__(self, jobid=None):
        # This is a list of DS3Objects
        self.objectlist = []
        self.jobid = jobid
    def add_object(self, ds3obj):
        self.objectlist.append(ds3obj)
        return
    
'''
============================================================
Client
'''
class Client(object):
    def __init__(self, endpoint, credentials):
        self.netclient = NetworkClient(endpoint, credentials)

    def get_netclient(self):
        return self.netclient
    
    def get_service(self, request):
        return GetServiceResponse(self.netclient.get_response(request))

    def get_bucket(self, request):
        return GetBucketResponse(self.netclient.get_response(request))

    def put_bucket(self, request):
        return PutBucketResponse(self.netclient.get_response(request))

    def delete_bucket(self, request):
        return DeleteBucketResponse(self.netclient.get_response(request))
        
    def get_object(self, request):
        return GetObjectResponse(self.netclient.get_response(request), request)

    def put_object(self, request):
        return PutObjectResponse(self.netclient.put(request))

    def delete_object(self, request):
        return DeleteObjectResponse(self.netclient.get_response(request))
    
    def bulk_put(self, request):
        return BulkPutResponse(self.netclient.bulk_put(request))
    
        """
        objects = xmldom.Element('objects')
        for file_object in object_list:
            obj_elm = xmldom.Element('object')
            obj_elm.set('name', file_object.name)
            obj_elm.set('size', str(file_object.size))
            objects.append(obj_elm)
        response = self.__put(
            join_paths('/_rest_/buckets/', bucket),
            xmldom.tostring(objects),
            query_params={"operation": "start_bulk_put"})
        return response.read()
        """
        
    def bulk_get(self, bucket, object_list):
        """
        objects = xmldom.Element('objects')
        for file_object in object_list:
            obj_elm = xmldom.Element('object')
            obj_elm.set('name', file_object.name)
            objects.append(obj_elm)
        response = self.__put(
            join_paths('/_rest_/buckets/', bucket),
            xmldom.tostring(objects),
            query_params={"operation": "start_bulk_get"})
        return response.read()
        """
             
'''
================================================================
NetworkClient
   Network client class
'''
class NetworkClient(object):
    def __init__(self, endpoint, credentials):
        self.networkconnection = NetworkConnection(endpoint, credentials.accessId, credentials.key)
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
        headers['Authorization'] = self.build_authorization(
            verb=request.httpverb, date=date, resource=request.path)
        #connection.request(request.get_verb(), urlparse.urljoin(self.networkconnection.endpoint, request.get_path()), headers=headers)
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
        s = request.objectdata.read()
        print "size of", request.objectkey, len(s)
        connection.request(request.httpverb, request.path, body=s, headers=headers)
        if isinstance(request.objectdata, file) and not request.objectdata.closed:
            request.objectdata.close()
            
        return connection.getresponse()      
    
    def bulk_put(self, request):
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
            #verb=request.httpverb, date=date, resource=request.path)
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
        print "contents: " + contents
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


'''
================================================================
NetworkConnection
   This class abstracts the HTTP network connection from the client to the server.
'''
class NetworkConnection(object):
    def __init__(self, endpoint, accessid, key, proxy=None):
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
