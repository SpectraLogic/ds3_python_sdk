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
import urllib
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

class StreamWithLength(object):
  def __init__(self, stream, length):
    self.stream = stream
    self.length = length
    self.total_read = 0
    
  def read(self, size=None):
    size_to_read = size
    # if already read to max length, do not read any more
    if self.total_read >= self.length:
      size_to_read = 0
    
    # if no size is specified or specified size is greater than length restriction
    # then read up to the length restriction
    elif size is None or size + self.total_read > self.length:
      size_to_read = self.length - self.total_read
    
    self.total_read = self.total_read + size_to_read
    return self.stream.read(size_to_read)

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
    self.secure = self.endpoint_secure(endpoint)
    self.proxy = None
    
  def endpoint_secure(self, endpoint):
    """Determines type of connection based on HTTP or HTTPS in endpoint path"""
    if endpoint.startswith('https://'):
      return True
    return False # The default is HTTP

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
    
  def setup_connection(self, target):
    if self.secure:
      return httplib.HTTPSConnection(target)
    return httplib.HTTPConnection(target)
    
  def send_request(self, request):
    """create http or https connection and send the DS3 request. Set the proxy if one is specified"""
    connection = None
    if self.proxy:
      connection = self.setup_connection(self.proxy)
      connection.set_tunnel(self.networkconnection.endpoint)
    else:
      connection = self.setup_connection(self.networkconnection.endpoint)
            
    date = self.get_date()
    path = self.build_path(request.path, request.query_params)
            
    headers = {}
    if self.networkconnection.port:
      headers['Host'] = self.networkconnection.hostname +":"+ str(self.networkconnection.port)
    else:
      headers['Host'] = self.networkconnection.hostname
    headers['Date'] = date
    
    canonicalized_resource = self.canonicalize_path(self.build_path(request.path), request.query_params)
    
    # add additonal header information if specficied in the request. This might be a byte range for example
    amz_headers = {}
    for key, value in request.headers.iteritems():
      if key == 'Content-Length':
        # Add to headers,  but not to amz-headers
        headers[key] = value
      elif not key.startswith('x-amz-meta-'):
        amz_headers['x-amz-meta-' + key] = self.canonicalize_header_value(value)
      else:
        amz_headers[key] = self.canonicalize_header_value(value)
    
    headers.update(amz_headers)
            
    if request.http_verb == HttpVerb.PUT or request.http_verb == HttpVerb.POST:
      canonicalized_amz_header = self.canonicalized_amz_headers(amz_headers)
      headers['Content-Type'] = 'application/octet-stream'
      headers['Authorization'] = self.build_authorization( verb=request.http_verb, 
                                                           date=date, 
                                                           content_type='application/octet-stream', 
                                                           canonicalized_amz_header=canonicalized_amz_header,
                                                           resource=canonicalized_resource)
      connection.request(request.http_verb, path, body=request.body, headers=headers)
    else:
      headers['Authorization'] = self.build_authorization(verb=request.http_verb, date=date, resource=canonicalized_resource)
      connection.request(request.http_verb, path, headers=headers)
    
    return connection.getresponse()
    
  def canonicalize_header_value(self, value):
    #if a header value is a list, then it is converted into a comma separated list
    if not isinstance(value, list):
      return value
    parts = []
    for part in value:
      parts.append(part)
    return ','.join(parts)
    
  def canonicalized_amz_headers(self, amz_headers):
    if not amz_headers:
      return ''
    
    headers = []
    for key, value in amz_headers.iteritems():
      headers.append(key + ':' + str(value))
      
    headers.sort()
    result = "\n".join(headers)
    return result + '\n'
    
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
     
    
  def build_authorization(self, verb='', date='', content_type='', resource='', canonicalized_amz_header=''):
    ###Build the S3 authorization###
    signature = self.aws_signature(self.credentials.key, verb=verb, content_type=content_type,
                                  date=date, canonicalized_amz_header=canonicalized_amz_header, canonicalized_resource=resource)
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

  def normalize_string(self, url):
    return urllib.quote(url)
    
  def build_path(self, resource, query_params={}):
    if len(query_params) == 0:
      return self.normalize_string(resource)
    new_path = self.normalize_string(resource) + '?'

    new_path += '&'.join(map(lambda tupal: self.build_query_param(tupal), 
                             query_params.iteritems()))
    return new_path
    
  def build_query_param(self, param):
    if param[1] is None:
      return param[0]
    return param[0] + '=' + self.normalize_string(str(param[1]))

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
    self.endpoint = self.remove_http_from_endpoint(endpoint)
    
  def remove_http_from_endpoint(self, endpoint):
    if not endpoint.startswith('http'):
      return endpoint
    index = endpoint.find('://')
    if endpoint >= 0:
      return endpoint[index+3:]
    return endpoint
        
  def ensure_schema(self, endpoint):
    if endpoint.startswith('http'):
      return endpoint
    else:
      return 'http://' + endpoint