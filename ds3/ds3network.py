#   Copyright 2014-2016 Spectra Logic Corporation. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License"). You may not use
#   this file except in compliance with the License. A copy of the License is located at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   or in the "license" file accompanying this file.
#   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied. See the License for the
#   specific language governing permissions and limitations under the License.

#   This code is auto-generated, do not modify

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

def typeCheckString(input_arg):
  return ensureUTF8(typeCheck(input_arg, basestring))

def ensureUTF8(input_arg):
  if isinstance(input_arg, unicode):
    return input_arg.encode('utf-8')
  return input_arg
  
def typeCheck(input_arg, type_to_check):
  if isinstance(input_arg, type_to_check):
    return input_arg
  else:
    raise TypeError("expected instance of type " + type_to_check.__name__ + ", got instance of type " + type(input_arg).__name__)

class Ds3Error(object):
  def __init__(self, code, http_error_code, message):
    self.code = code
    self.http_error_code = http_error_code
    self.message = message
    
class RequestFailed(Exception):
  def __init__(self, summary, ds3_error):
    self.summary = summary
    self.code = ds3_error.code
    self.http_error_code = ds3_error.http_error_code
    self.message = ds3_error.message

  def __str__(self):
    return '{0} \n Code={1} \n HttpError={2} \n {3}'.format(self.summary, self.code, 
                                                                self.http_error_code, self.message)

class HttpVerb(object):
  """ HttpVerbs as Enums """
  GET = 'GET'
  PUT = 'PUT'
  DELETE = 'DELETE'
  HEAD = 'HEAD'
  POST = 'POST'

class Credentials(object):
  def __init__(self, accessId, key):
    self.accessId = accessId.strip()
    self.key = key.strip()
      
  def is_valid(self):
    return True if self.accessId and self.key else False
    
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
    
  def to_ds3error(self, xml_string, status_code, reason):
    if not xml_string:
      #There is no error payload
      return Ds3Error(reason, status_code, None)
    
    doc = xml.dom.minidom.parseString(xml_string)
    code = self.get_name_from_node(doc, "Code")
    http_error_code = int(self.get_name_from_node(doc, "HttpErrorCode"))
    message = self.get_name_from_node(doc, "Message") 
    obj = Ds3Error(code, http_error_code, message)
        
    return obj

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
    if request.query_params:
      path = self.build_path(request.path, request.query_params)
            
    headers = {}
    headers['Host'] = self.networkconnection.hostname +":"+ str(self.networkconnection.port)
    headers['Date'] = date
    
    canonicalized_resource = self.canonicalize_path(request.path, request.query_params)
    
    # add additonal header information if specficied in the request. This might be a byte range for example
    if request.headers:
      headers.update(request.headers)
            
    if request.http_verb == HttpVerb.PUT:
      headers['Content-Type'] = 'application/octet-stream'
      headers['Authorization'] = self.build_authorization( verb=request.http_verb, date=date, 
                                                           content_type='application/octet-stream', resource=canonicalized_resource)
      connection.request(request.http_verb, path, body=request.body, headers=headers)
    else:
      headers['Authorization'] = self.build_authorization(verb=request.http_verb, date=date, resource=canonicalized_resource)
      connection.request(request.http_verb, path, headers=headers)
    
    return connection.getresponse()
    
  def canonicalize_path(self, request_path, query_params):
    path = request_path
    if 'delete' in query_params:
      path += '?delete'
    if 'versioning' in query_params:
      path += '?versioning=' + str(query_params['versioning'])
    if 'uploads' in query_params:
      path += '?uploads'
      if query_params['uploads'] is not None:
        path += '=' + str(query_params['uploads'])
    return path
     
    
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

    new_path += '&'.join(map(lambda tupal: self.build_query_param(tupal), 
                             query_params.iteritems()))
    return new_path
    
  def build_query_param(self, param):
    if param[1] is None:
      return param[0]
    return param[0] + '=' + str(param[1])

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