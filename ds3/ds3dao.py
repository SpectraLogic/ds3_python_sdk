import xml.dom.minidom
# from xml.dom.minidom import Node
import httplib

from abc import ABCMeta
 
import ds3
 
class XmlSerializer(ds3.XmlSerializer):
    
    def to_print(self, xml_string):
        self.pretty_print_xml(xml_string)
        return None
    
    def to_users(self, xml_string):
        doc = self.parse_string(xml_string)
        obj = DS3Users()
        for node in doc.getElementsByTagName('User'):
            user = DS3User()
            user.authid = self.get_name_from_node(node, 'AuthId')
            user.id = self.get_name_from_node(node, 'Id')
            user.name = self.get_name_from_node(node, 'Name')
            user.secretkey = self.get_name_from_node(node, 'SecretKey')
            obj.add_user(user)
            
        return obj
        
    def to_user(self, xml_string):
        doc = self.parse_string(xml_string)
        obj = DS3User()
        for node in doc.getElementsByTagName('Data'):
            obj.authid = self.get_name_from_node(node, 'AuthId')
            obj.id = self.get_name_from_node(node, 'Id')
            obj.name = self.get_name_from_node(node, 'Name')
            obj.secretkey = self.get_name_from_node(node, 'SecretKey')
            
        return obj
        
    def to_request_handlers(self, xml_string):
        self.pretty_print_xml(xml_string)
        return None
    
    def to_retreivers(self, xml_string):
        self.pretty_print_xml(xml_string)
        return None
        
    def to_dao_prime_object(self, xml_string):
        obj = DaoPrimeObject()
        self.pretty_print_xml(xml_string)
        
        return obj
        
    def to_dao_prime(self, xml_string):
        obj = DaoPrime()
        doc = xml.dom.minidom.parseString(xml_string)
        for node in doc.getElementsByTagName('Prime'):
            d = {}
            d['Active'] = str(self.get_name_from_node(node, 'Active'))
            d['BucketId'] = str(self.get_name_from_node(node, "BucketId"))
            d['CreatedAt'] = str(self.get_name_from_node(node, 'CreatedAt'))
            d['RequestType'] = str(self.get_name_from_node(node, 'RequestType'))
            d['Id'] = str(self.get_name_from_node(node, 'Id'))
            obj.add_obj(d)

        obj.add_child(self.to_dao_bucket(xml_string))
        
        return obj
        
    def to_dao_bucket(self, xml_string):
        obj = DaoBucket()
        doc = xml.dom.minidom.parseString(xml_string)
        for node in doc.getElementsByTagName('Bucket'):
            d = {}
            d['Name'] = str(self.get_name_from_node(node, "Name"))
            d['CreationDate'] = str(self.get_name_from_node(node, "CreationDate"))
            d['Id'] = str(self.get_name_from_node(node, 'Id'))
            d['State'] = str(self.get_name_from_node(node, 'State'))
            d['UserId'] = str(self.get_name_from_node(node, 'UserId'))
            obj.add_obj(d)
                     
        return obj
    
    def to_dao_object(self, xml_string):
        obj = DaoObject()
        doc = xml.dom.minidom.parseString(xml_string)
        for node in doc.getElementsByTagName('Object'):
            d = {}
            d['BucketId'] = str(self.get_name_from_node(node,'BucketId'))
            d['Id'] = str(self.get_name_from_node(node,'Id'))
            d['Name'] = str(self.get_name_from_node(node,'Name'))
            d['Size'] = str(self.get_name_from_node(node,'Size'))
            d['State'] = str(self.get_name_from_node(node,'State'))
            d['Type'] = str(self.get_name_from_node(node,'Type'))
            d['Version'] = str(self.get_name_from_node(node,'Version'))
            obj.add_obj(d)
            
        return obj
    
    def to_dao_tape(self, xml_string):
        obj = DaoTape()
        self.pretty_print_xml(xml_string)
        return obj
    
    def to_dao_tape_bucket(self, xml_string):
        obj = DaoTapeBucket()
        self.pretty_print_xml(xml_string)
        return obj
    
    def to_dao_tape_object(self, xml_string):
        obj = DaoTapeObject()
        self.pretty_print_xml(xml_string)
        return obj
         
class DaoRetreiversRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/beans_retriever/"
        self.httpverb = ds3.HttpVerb.GET
           
class DaoRetreiversResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_retreivers(response.read())
    
class RequestHandlersRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/request_handler/"
        self.httpverb = ds3.HttpVerb.GET
        
class RequestHandlersResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_request_handlers(response.read())
    
class GetUsersRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = '/_rest_/user/'
        self.httpverb = ds3.HttpVerb.GET
        
class GetUsersResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_users(response.read())
    
class GetUserRequest(ds3.AbstractRequest):
    def __init__(self, userid):
        self.path = self.join_paths('/_rest_/user/', userid)
        self.httpverb = ds3.HttpVerb.GET

class GetUserResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_user(response.read())
        
class DaoBucketRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/beans_retriever/com.spectralogic.s3.dao.domain.ds3.Bucket"
        self.httpverb = ds3.HttpVerb.GET
        
class DaoBucketResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_dao_bucket(response.read())
    
class DaoObjectRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/beans_retriever/com.spectralogic.s3.dao.domain.ds3.Object"
        self.httpverb = ds3.HttpVerb.GET
        
class DaoObjectResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_dao_object(response.read())
        
class DaoPrimeRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/beans_retriever/com.spectralogic.s3.dao.domain.ds3.Prime"
        self.httpverb = ds3.HttpVerb.GET
        
class DaoPrimeResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_dao_prime(response.read())

class DaoPrimeObjectRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/beans_retriever/com.spectralogic.s3.dao.domain.ds3.PrimeObject"
        self.httpverb = ds3.HttpVerb.GET
        
class DaoPrimeObjectResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_dao_prime_object(response.read())

class DaoTapeRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/beans_retriever/com.spectralogic.s3.dao.domain.tape.Tape"
        self.httpverb = ds3.HttpVerb.GET
        
class DaoTapeResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_dao_tape(response.read())

class DaoTapeBucketRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/beans_retriever/com.spectralogic.s3.dao.domain.tape.TapeBucket"
        self.httpverb = ds3.HttpVerb.GET
        
class DaoTapeBucketResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_dao_tape_bucket(response.read())

class DaoTapeObjectRequest(ds3.AbstractRequest):
    def __init__(self):
        self.path = "/_rest_/beans_retriever/com.spectralogic.s3.dao.domain.tape.TapeObject"
        self.httpverb = ds3.HttpVerb.GET
        
class DaoTapeObjectResponse(ds3.AbstractResponse):
    def process_response(self, response):
        self.check_status_code(200)
        self.result = XmlSerializer().to_dao_tape_object(response.read())

class AbstractDaoRetreiver(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        self.data = []
        self.child = []
        
    def add_obj(self, obj):
        self.data.append(obj)
        
    def add(self, key, value):
        d = {}
        d[key] = value
        self.data.append(d)
        
    def add_child(self, childobj):
        self.child.append(childobj)

    
class DaoBucket(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoBucket, self).__init__()
        
class DaoObject(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoObject, self).__init__()
        
class DaoPrime(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoPrime, self).__init__()  

class DaoPrimeObject(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoPrimeObject, self).__init__()  

class DaoTape(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoTape, self).__init__()
        
class DaoTapeBucket(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoTapeBucket, self).__init__()
        
class DaoTapeObject(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoTapeObject, self).__init__()      

class DS3User(object):
    def __init__(self):
        self.authid = ''
        self.secretkey = ''
        self.name = ''
        self.id = ''

class DS3Users(object):
    def __init__(self):
        self.list = []
        
    def add_user(self, user):
        self.list.append(user)
    def get_users(self):
        return self.list
    
class Client(ds3.Client):
    def __init__(self, endpoint):
        self.netclient = NetworkClient(endpoint)
    
    def get_users(self, request):
        return GetUsersResponse(self.netclient.get_response(request), request)
    
    def get_user(self, request):
        return GetUserResponse(self.netclient.get_response(request), request)
    
    def request_handlers(self, request):
        return RequestHandlersResponse(self.netclient.get_response(request), request)
                
    def dao_retreivers(self, request):
        return DaoRetreiversResponse(self.netclient.get_response(request), request)
    
    def dao_bucket(self, request):
        return DaoBucketResponse(self.netclient.get_response(request), request)
    
    def dao_object(self, request):
        return DaoObjectResponse(self.netclient.get_response(request), request)
    
    def dao_prime(self, request):
        return DaoPrimeResponse(self.netclient.get_response(request), request)
    
    def dao_prime_object(self, request):
        return DaoPrimeObjectResponse(self.netclient.get_response(request), request)
    
    def dao_tape(self, request):
        return DaoTapeResponse(self.netclient.get_response(request), request)
    
    def dao_tape_bucket(self, request):
        return DaoTapeBucketResponse(self.netclient.get_response(request), request)
    
    def dao_tape_object(self, request):
        return DaoTapeObjectResponse(self.netclient.get_response(request), request)
        
'''
================================================================
NetworkClient
   Network client class
'''
class NetworkClient(ds3.NetworkClient):
    def __init__(self, endpoint):
        self.networkconnection = ds3.NetworkConnection(endpoint, 'not', 'used')
        
    def get_response(self, request):
        connection = httplib.HTTPConnection(self.networkconnection.endpoint)
        date = self.get_date()
        headers = {}
        headers['Host'] = self.networkconnection.hostname +":"+ str(self.networkconnection.port)
        headers['Date'] = date
        headers['Internal-Request'] = "1"
        
        connection.request(request.httpverb, request.path, headers=headers)
        return connection.getresponse()
        
