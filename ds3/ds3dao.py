import xml.dom.minidom
# from xml.dom.minidom import Node
import httplib

from abc import ABCMeta
 
import ds3
 
class XmlSerializer(ds3.XmlSerializer):
    
    
    def to_dao_prime(self, xml_string):
        print xml_string
        return None
        
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

class AbstractDaoRetreiver(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        print "AbstractDaoRetreiever"
        self.data = []
        
    def add_obj(self, obj):
        self.data.append(obj)
        
    def add(self, key, value):
        d = {}
        d[key] = value
        self.data.append(d)

    
class DaoBucket(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoBucket, self).__init__()
        
class DaoObject(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoObject, self).__init__()
        
class DaoPrime(AbstractDaoRetreiver):
    def __init__(self):
        super(DaoPrime, self).__init__()  

     
'''
============================================================
Client
'''
class Client(ds3.Client):
    def __init__(self, endpoint, credentials):
        self.netclient = NetworkClient(endpoint, credentials)
        
    def dao_bucket(self, request):
        return DaoBucketResponse(self.netclient.get_response(request))
    
    def dao_object(self, request):
        return DaoObjectResponse(self.netclient.get_response(request))
    
    def dao_prime(self, request):
        return DaoPrimeResponse(self.netclient.get_response(request))
    
        
'''
================================================================
NetworkClient
   Network client class
'''
class NetworkClient(ds3.NetworkClient):
    def __init__(self, endpoint, credentials):
        self.networkconnection = ds3.NetworkConnection(endpoint, credentials.accessId, credentials.key)
        self.credentials = credentials
        
    def get_response(self, request):
        connection = httplib.HTTPConnection(self.networkconnection.endpoint)
        date = self.get_date()
        headers = {}
        headers['Host'] = self.networkconnection.hostname +":"+ str(self.networkconnection.port)
        headers['Date'] = date
        headers['Internal-Request'] = "1"
        headers['Authorization'] = self.build_authorization(
            verb=request.httpverb, date=date, resource=request.path)
        #connection.request(request.get_verb(), urlparse.urljoin(self.networkconnection.endpoint, request.get_path()), headers=headers)
        connection.request(request.httpverb, request.path, headers=headers)
        return connection.getresponse()
        
