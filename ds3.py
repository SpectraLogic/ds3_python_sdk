import httplib
import hmac
import base64
import xml.dom.minidom
import xml.etree.ElementTree as xmldom

from hashlib import sha1
from urlparse import urlparse
from email.Utils import formatdate

def sign(key, contents):
    signer = hmac.new(key.encode('utf-8'), digestmod=sha1)
    signer.update(contents)
    digest = signer.digest()
    return base64.encodestring(digest).strip().decode('utf-8')

def aws_signature(key, verb='GET', md5='',
    content_type='', date='',
    canonicalized_amz_header='', canonicalized_resource=''):
    signature_string = verb + '\n'
    signature_string += md5 + '\n'
    signature_string += content_type+ '\n'
    signature_string += date + '\n'
    signature_string += canonicalized_amz_header
    signature_string += canonicalized_resource
    return sign(key, signature_string) 

def get_date():
    return formatdate()

def join_paths(path1, path2):
    final_path = ''
    if not path1.startswith('/'):
        final_path+='/'
    final_path+=path1
    
    if path1.endswith('/') and path2.startswith('/'):
        final_path += path2[1:]
    elif path1.endswith('/'):
        final_path += path2
    else:
        final_path += '/' + path2
    return final_path

def build_path(resource, query_params):
    if len(query_params) == 0:
        return resource
    new_path = resource + '?'

    new_path += '&'.join(map(lambda tupal: (tupal[0] + '=' + tupal[1]), query_params.iteritems()))        
    return new_path 

class Credentials(object):
    def __init__(self, client_id, key):
        self.client_id = client_id
        self.key = key

class ObjectData(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size

class Ds3(object):
    def __init__(self, endpoint, credentials):
        self.endpoint = endpoint
        self.credentials = credentials
        url = urlparse(self.endpoint)
        self.hostname = url.hostname
        self.port = url.port

    def service_list(self):
        response = self.__get('/')
        print xml.dom.minidom.parseString(response.read()).toprettyxml()

    def bucket_list(self, bucket):
        response = self.__get(join_paths('/', bucket))
        print xml.dom.minidom.parseString(response.read()).toprettyxml()

    def create_bucket(self, bucket):
        response = self.__put(join_paths('/', bucket))
        print response.status
        print response.read()

    def get_object(self, bucket, object_name):
        response = self.__get(join_paths(bucket, object_name))
        print response.read()

    def put_object(self, bucket, object_name, object_data):
        response = self.__put(join_paths(bucket, object_name), object_data)
        print response.status
        print response.read()

    def bulk_put(self, bucket, object_list):
        objects = xmldom.Element('objects')
        for file_object in object_list:
            objElm = xmldom.Element('object')
            objElm.set('name', file_object.name)
            objElm.set('size', file_object.size)
            objects.append(objElm)
        response = self.__put(join_paths('/', bucket) + '/?start-bulk-put', xmldom.tostring(objects))
        print response.status
        print response.read()

    def bulk_get(self, bucket, object_list):
        objects = xmldom.Element('objects')
        for file_object in object_list:
            objElm = xmldom.Element('object')
            objElm.set('name', file_object.name)
            objects.append(objElm)
        response = self.__put(join_paths('/', bucket) + '/?start-bulk-get', xmldom.tostring(objects))
        print response.status
        print response.read()

    def delete_object(self, bucket, object_name):
        response = self.__delete(join_paths(bucket, object_name))
        print response.status
        print response.read()

    def __get(self, resource):
        return self.__http_opt('GET', resource)

    def __delete(self, resource):
        return self.__http_opt('DELETE', resource)

    def __http_opt(self, verb, resource):
        print resource
        connection = httplib.HTTPConnection(self.endpoint)
        date = get_date()
        headers = {}
        headers['Host'] = self.hostname
        headers['Date'] = date 
        headers['Authorization'] = self.__build_authorization(verb=verb, date=date, resource=resource) 
        connection.request(verb, resource, headers=headers) 

        return connection.getresponse()

    def __put(self, resource, body='', query_params = {}):
        print resource
        connection = httplib.HTTPConnection(self.endpoint)
        date = get_date()
        headers = {}
        headers['Host'] = self.hostname
        headers['Date'] = date
        headers['Content-Type'] = 'application/octet-stream'
        headers['Authorization'] = self.__build_authorization(verb='PUT', date=date, content_type='application/octet-stream', resource=resource) 
        resource_path = build_path(resource, query_params)
        connection.request('PUT', resource, body=body, headers=headers)

        return connection.getresponse()

    def __build_authorization(self, verb='', date='', content_type='', resource=''):
        signature = aws_signature(self.credentials.key, verb=verb, content_type=content_type, date=date, canonicalized_resource=resource)
        return 'AWS ' + self.credentials.client_id + ':' + signature

def main():
    client = Ds3('192.168.6.163:8080', Credentials('cnlhbg==', 'R8ATmVhzTyGX'))
    #client.service_list()
    bucket = 'remoteTest24' 
    #client.create_bucket(bucket)

    client.bucket_list(bucket)
    #import random
    #import string

    #object_list = [ObjectData('test4', '256'), ObjectData('test5', '1024'), ObjectData('test6', '2048')]
    #for item in object_list:
    #    client.put_object(bucket, item.name, ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(int(item.size))]))
    #client.bulk_put(bucket, object_list)
    #client.get_object('remoteTest23', 'user/hduser/gutenberg/4300.txt.utf-8')
    #client.put_object('remoteTest24', 'test4', 'Here is some test data!')
    #client.delete_object('remoteTest23', 'test2.txt')
    #client.get_object('remoteTest23', 'test2.txt')
    #client.bucket_list('remoteTest23')

if __name__ == '__main__':
    main()
