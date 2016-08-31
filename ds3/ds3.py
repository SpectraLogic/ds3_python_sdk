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

import xml.etree.ElementTree as xmldom
import os

from abc import ABCMeta
import posixpath
from ds3network import *

def createClientFromEnv():
  """Build a Client from environment variables.

     Required: DS3_ACCESS_KEY, DS3_SECRET_KEY, DS3_ENDPOINT

     Optional: http_proxy
  """
  access_key = os.environ.get('DS3_ACCESS_KEY')
  secret_key = os.environ.get('DS3_SECRET_KEY')
  endpoint = os.environ.get('DS3_ENDPOINT')
  proxy = os.environ.get('http_proxy')

  if None in (access_key, secret_key, endpoint):
    raise Exception('Required environment variables are not set: DS3_ACCESS_KEY, DS3_SECRET_KEY, DS3_ENDPOINT')

  creds = Credentials(access_key, secret_key)
  client = Client(endpoint, creds, proxy)
  return client

# Models

class HeadRequestStatus(object):
  """Head bucket and head object return values"""
  EXISTS = 'EXISTS'  # 200
  NOTAUTHORIZED = 'NOTAUTHORIZED' # 403
  DOESNTEXIST = 'DOESNTEXIST' # 404
  UNKNOWN = 'UNKNOWN'

class FileObject(object):
  def __init__(self, name, size=None):
    self.name = name
    self.size = size

  def to_xml(self):
    xml_object = xmldom.Element('Object')
    xml_object.set('Name', posixpath.normpath(self.name))
    if self.size is not None:
      xml_object.set('Size', str(self.size))
    return xml_object

class FileObjectList(object):
  def __init__(self, object_list):
    for obj in object_list:
      if not isinstance(obj, FileObject):
        raise TypeError("FileObjectList should only contain type: FileObject")
    self.object_list = object_list

  def to_xml(self):
    xml_object_list = xmldom.Element('Objects')
    for obj in self.object_list:
      xml_object_list.append(obj.to_xml())
    return xml_object_list

class DeleteObject(object):
  def __init__(self, key):
    self.key = key

  def to_xml(self):
    xml_key = xmldom.Element('Key')
    xml_key.text = self.key

    xml_object = xmldom.Element('Object')
    xml_object.append(xml_key)
    return xml_object

class DeleteObjectList(object):
  def __init__(self, object_list):
    for obj in object_list:
      if not isinstance(obj, DeleteObject):
        raise TypeError("DeleteObjectList should only contain type: DeleteObject")
    self.object_list = object_list

  def to_xml(self):
    xml_object_list = xmldom.Element('Delete')
    for obj in self.object_list:
      xml_object_list.append(obj.to_xml())
    return xml_object_list

class Part(object):
  def __init__(self, part_number, etag):
    self.part_number = str(part_number)
    self.etag = etag

  def to_xml(self):
    xml_part_number = xmldom.Element('PartNumber')
    xml_part_number.text = self.part_number

    xml_etag = xmldom.Element('ETag')
    xml_etag.text = self.etag

    xml_part = xmldom.Element('Part')
    xml_part.append(xml_part_number)
    xml_part.append(xml_etag)
    return xml_part

class PartList(object):
  def __init__(self, part_list):
    for part in part_list:
      if not isinstance(part, Part):
        raise TypeError("PartList should only contain type: Part")
    self.part_list = part_list

  def to_xml(self):
    xml_part_list = xmldom.Element('CompleteMultipartUpload')
    for part in self.part_list:
      xml_part_list.append(part.to_xml())
    return xml_part_list

# Type Descriptors

class PhysicalPlacement(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Ds3Target', 'Ds3Targets', Ds3Target()),
      ('Pool', 'Pools', Pool()),
      ('Tape', 'Tapes', Tape())
    }

class Blob(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'ByteOffset' : None,
      'Checksum' : None,
      'ChecksumType' : None,
      'Id' : None,
      'Length' : None,
      'ObjectId' : None
    }
    self.element_lists = {}

class Bucket(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'DataPolicyId' : None,
      'Id' : None,
      'LastPreferredChunkSizeInBytes' : None,
      'LogicalUsedCapacity' : None,
      'Name' : None,
      'UserId' : None
    }
    self.element_lists = {}

class BucketAcl(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BucketId' : None,
      'GroupId' : None,
      'Id' : None,
      'Permission' : None,
      'UserId' : None
    }
    self.element_lists = {}

class CanceledJob(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BucketId' : None,
      'CachedSizeInBytes' : None,
      'CanceledDueToTimeout' : None,
      'ChunkClientProcessingOrderGuarantee' : None,
      'CompletedSizeInBytes' : None,
      'CreatedAt' : None,
      'DateCanceled' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'Naked' : None,
      'Name' : None,
      'OriginalSizeInBytes' : None,
      'Priority' : None,
      'Rechunked' : None,
      'RequestType' : None,
      'Truncated' : None,
      'UserId' : None
    }
    self.element_lists = {}

class CapacitySummaryContainer(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Pool' : StorageDomainCapacitySummary(),
      'Tape' : StorageDomainCapacitySummary()
    }
    self.element_lists = {}

class CompletedJob(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BucketId' : None,
      'CachedSizeInBytes' : None,
      'ChunkClientProcessingOrderGuarantee' : None,
      'CompletedSizeInBytes' : None,
      'CreatedAt' : None,
      'DateCompleted' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'Naked' : None,
      'Name' : None,
      'OriginalSizeInBytes' : None,
      'Priority' : None,
      'Rechunked' : None,
      'RequestType' : None,
      'Truncated' : None,
      'UserId' : None
    }
    self.element_lists = {}

class DataPathBackend(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Activated' : None,
      'AutoActivateTimeoutInMins' : None,
      'AutoInspect' : None,
      'DefaultImportConflictResolutionMode' : None,
      'Id' : None,
      'InstanceId' : None,
      'LastHeartbeat' : None,
      'PartiallyVerifyLastPercentOfTapes' : None,
      'UnavailableMediaPolicy' : None,
      'UnavailablePoolMaxJobRetryInMins' : None,
      'UnavailableTapePartitionMaxJobRetryInMins' : None
    }
    self.element_lists = {}

class DataPersistenceRule(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DataPolicyId' : None,
      'Id' : None,
      'IsolationLevel' : None,
      'MinimumDaysToRetain' : None,
      'State' : None,
      'StorageDomainId' : None,
      'Type' : None
    }
    self.element_lists = {}

class DataPolicy(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'AlwaysForcePutJobCreation' : None,
      'AlwaysMinimizeSpanningAcrossMedia' : None,
      'AlwaysReplicateDeletes' : None,
      'BlobbingEnabled' : None,
      'ChecksumType' : None,
      'CreationDate' : None,
      'DefaultBlobSize' : None,
      'DefaultGetJobPriority' : None,
      'DefaultPutJobPriority' : None,
      'DefaultVerifyJobPriority' : None,
      'EndToEndCrcRequired' : None,
      'Id' : None,
      'LtfsObjectNamingAllowed' : None,
      'Name' : None,
      'RebuildPriority' : None,
      'Versioning' : None
    }
    self.element_lists = {}

class DataPolicyAcl(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DataPolicyId' : None,
      'GroupId' : None,
      'Id' : None,
      'UserId' : None
    }
    self.element_lists = {}

class DataReplicationRule(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DataPolicyId' : None,
      'Ds3TargetDataPolicy' : None,
      'Ds3TargetId' : None,
      'Id' : None,
      'State' : None,
      'Type' : None
    }
    self.element_lists = {}

class DegradedBlob(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BlobId' : None,
      'BucketId' : None,
      'Id' : None,
      'PersistenceRuleId' : None,
      'ReplicationRuleId' : None
    }
    self.element_lists = {}

class Group(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BuiltIn' : None,
      'Id' : None,
      'Name' : None
    }
    self.element_lists = {}

class GroupMember(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'GroupId' : None,
      'Id' : None,
      'MemberGroupId' : None,
      'MemberUserId' : None
    }
    self.element_lists = {}

class ActiveJob(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Aggregating' : None,
      'BucketId' : None,
      'CachedSizeInBytes' : None,
      'ChunkClientProcessingOrderGuarantee' : None,
      'CompletedSizeInBytes' : None,
      'CreatedAt' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'MinimizeSpanningAcrossMedia' : None,
      'Naked' : None,
      'Name' : None,
      'OriginalSizeInBytes' : None,
      'Priority' : None,
      'Rechunked' : None,
      'RequestType' : None,
      'Truncated' : None,
      'UserId' : None
    }
    self.element_lists = {}

class JobChunk(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BlobStoreState' : None,
      'ChunkNumber' : None,
      'Id' : None,
      'JobCreationDate' : None,
      'JobId' : None,
      'NodeId' : None,
      'PendingTargetCommit' : None,
      'ReadFromDs3TargetId' : None,
      'ReadFromPoolId' : None,
      'ReadFromTapeId' : None
    }
    self.element_lists = {}

class Node(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DataPathHttpPort' : None,
      'DataPathHttpsPort' : None,
      'DataPathIpAddress' : None,
      'DnsName' : None,
      'Id' : None,
      'LastHeartbeat' : None,
      'Name' : None,
      'SerialNumber' : None
    }
    self.element_lists = {}

class S3Object(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BucketId' : None,
      'CreationDate' : None,
      'Id' : None,
      'Latest' : None,
      'Name' : None,
      'Type' : None,
      'Version' : None
    }
    self.element_lists = {}

class StorageDomain(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'AutoEjectMediaFullThreshold' : None,
      'AutoEjectUponCron' : None,
      'AutoEjectUponJobCancellation' : None,
      'AutoEjectUponJobCompletion' : None,
      'AutoEjectUponMediaFull' : None,
      'Id' : None,
      'LtfsFileNaming' : None,
      'MaxTapeFragmentationPercent' : None,
      'MaximumAutoVerificationFrequencyInDays' : None,
      'MediaEjectionAllowed' : None,
      'Name' : None,
      'SecureMediaAllocation' : None,
      'VerifyPriorToAutoEject' : None,
      'WriteOptimization' : None
    }
    self.element_lists = {}

class StorageDomainCapacitySummary(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'PhysicalAllocated' : None,
      'PhysicalFree' : None,
      'PhysicalUsed' : None
    }
    self.element_lists = {}

class StorageDomainFailure(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Date' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'StorageDomainId' : None,
      'Type' : None
    }
    self.element_lists = {}

class StorageDomainMember(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Id' : None,
      'PoolPartitionId' : None,
      'State' : None,
      'StorageDomainId' : None,
      'TapePartitionId' : None,
      'TapeType' : None,
      'WritePreference' : None
    }
    self.element_lists = {}

class SystemFailure(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Date' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'Type' : None
    }
    self.element_lists = {}

class SpectraUser(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'AuthId' : None,
      'DefaultDataPolicyId' : None,
      'Id' : None,
      'Name' : None,
      'SecretKey' : None
    }
    self.element_lists = {}

class Ds3TargetFailureNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class JobCompletedNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'JobId' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class JobCreatedNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class JobCreationFailedNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class PoolFailureNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class S3ObjectCachedNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'JobId' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class S3ObjectLostNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class S3ObjectPersistedNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'JobId' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class StorageDomainFailureNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class SystemFailureNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class TapeFailureNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class TapePartitionFailureNotificationRegistration(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Format' : None,
      'Id' : None,
      'LastFailure' : None,
      'LastHttpResponseCode' : None,
      'LastNotification' : None,
      'NamingConvention' : None,
      'NotificationEndPoint' : None,
      'NotificationHttpMethod' : None,
      'NumberOfFailuresSinceLastSuccess' : None,
      'UserId' : None
    }
    self.element_lists = {}

class CacheFilesystem(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'AutoReclaimInitiateThreshold' : None,
      'AutoReclaimTerminateThreshold' : None,
      'BurstThreshold' : None,
      'Id' : None,
      'MaxCapacityInBytes' : None,
      'MaxPercentUtilizationOfFilesystem' : None,
      'NodeId' : None,
      'Path' : None
    }
    self.element_lists = {}

class Pool(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'AssignedToStorageDomain' : None,
      'AvailableCapacity' : None,
      'BucketId' : None,
      'Guid' : None,
      'Health' : None,
      'Id' : None,
      'LastAccessed' : None,
      'LastModified' : None,
      'LastVerified' : None,
      'Mountpoint' : None,
      'Name' : None,
      'PartitionId' : None,
      'PoweredOn' : None,
      'Quiesced' : None,
      'ReservedCapacity' : None,
      'State' : None,
      'StorageDomainId' : None,
      'TotalCapacity' : None,
      'Type' : None,
      'UsedCapacity' : None
    }
    self.element_lists = {}

class PoolFailure(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Date' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'PoolId' : None,
      'Type' : None
    }
    self.element_lists = {}

class PoolPartition(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Id' : None,
      'Name' : None,
      'Type' : None
    }
    self.element_lists = {}

class SuspectBlobPool(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BlobId' : None,
      'BucketId' : None,
      'DateWritten' : None,
      'Id' : None,
      'LastAccessed' : None,
      'PoolId' : None
    }
    self.element_lists = {}

class SuspectBlobTape(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BlobId' : None,
      'Id' : None,
      'OrderIndex' : None,
      'TapeId' : None
    }
    self.element_lists = {}

class Tape(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'AssignedToStorageDomain' : None,
      'AvailableRawCapacity' : None,
      'BarCode' : None,
      'BucketId' : None,
      'DescriptionForIdentification' : None,
      'EjectDate' : None,
      'EjectLabel' : None,
      'EjectLocation' : None,
      'EjectPending' : None,
      'FullOfData' : None,
      'Id' : None,
      'LastAccessed' : None,
      'LastCheckpoint' : None,
      'LastModified' : None,
      'LastVerified' : None,
      'PartiallyVerifiedEndOfTape' : None,
      'PartitionId' : None,
      'PreviousState' : None,
      'SerialNumber' : None,
      'State' : None,
      'StorageDomainId' : None,
      'TakeOwnershipPending' : None,
      'TotalRawCapacity' : None,
      'Type' : None,
      'VerifyPending' : None,
      'WriteProtected' : None
    }
    self.element_lists = {}

class TapeDensityDirective(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Density' : None,
      'Id' : None,
      'PartitionId' : None,
      'TapeType' : None
    }
    self.element_lists = {}

class TapeDrive(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'ErrorMessage' : None,
      'ForceTapeRemoval' : None,
      'Id' : None,
      'LastCleaned' : None,
      'PartitionId' : None,
      'SerialNumber' : None,
      'State' : None,
      'TapeId' : None,
      'Type' : None
    }
    self.element_lists = {}

class DetailedTapeFailure(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Date' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'TapeDriveId' : None,
      'TapeId' : None,
      'Type' : None
    }
    self.element_lists = {}

class TapeLibrary(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Id' : None,
      'ManagementUrl' : None,
      'Name' : None,
      'SerialNumber' : None
    }
    self.element_lists = {}

class TapePartition(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DriveType' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'ImportExportConfiguration' : None,
      'LibraryId' : None,
      'Name' : None,
      'Quiesced' : None,
      'SerialNumber' : None,
      'State' : None
    }
    self.element_lists = {}

class TapePartitionFailure(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Date' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'PartitionId' : None,
      'Type' : None
    }
    self.element_lists = {}

class Ds3Target(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'AccessControlReplication' : None,
      'AdminAuthId' : None,
      'AdminSecretKey' : None,
      'DataPathEndPoint' : None,
      'DataPathHttps' : None,
      'DataPathPort' : None,
      'DataPathProxy' : None,
      'DataPathVerifyCertificate' : None,
      'DefaultReadPreference' : None,
      'Id' : None,
      'Name' : None,
      'PermitGoingOutOfSync' : None,
      'Quiesced' : None,
      'ReplicatedUserDefaultDataPolicy' : None,
      'State' : None
    }
    self.element_lists = {}

class Ds3TargetFailure(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Date' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'TargetId' : None,
      'Type' : None
    }
    self.element_lists = {}

class Ds3TargetReadPreference(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BucketId' : None,
      'Id' : None,
      'ReadPreference' : None,
      'TargetId' : None
    }
    self.element_lists = {}

class SuspectBlobTarget(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'BlobId' : None,
      'Ds3TargetId' : None,
      'Id' : None
    }
    self.element_lists = {}

class BulkObject(object):
  def __init__(self):
    self.attributes = [
      'Bucket',
      'Id',
      'InCache',
      'Latest',
      'Length',
      'Name',
      'Offset',
      'Version'
    ]
    self.elements = {
      'PhysicalPlacement' : PhysicalPlacement()
    }
    self.element_lists = {}

class BulkObjectList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Object', None, BulkObject())
    }

class BuildInformation(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Branch' : None,
      'Revision' : None,
      'Version' : None
    }
    self.element_lists = {}

class BlobStoreTaskInformation(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DateScheduled' : None,
      'DateStarted' : None,
      'Description' : None,
      'DriveId' : None,
      'Ds3TargetId' : None,
      'Id' : None,
      'Name' : None,
      'PoolId' : None,
      'Priority' : None,
      'State' : None,
      'TapeId' : None
    }
    self.element_lists = {}

class BlobStoreTasksInformation(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Tasks', None, BlobStoreTaskInformation())
    }

class CacheEntryInformation(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Blob' : Blob(),
      'State' : None
    }
    self.element_lists = {}

class CacheFilesystemInformation(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'AvailableCapacityInBytes' : None,
      'CacheFilesystem' : CacheFilesystem(),
      'Summary' : None,
      'TotalCapacityInBytes' : None,
      'UnavailableCapacityInBytes' : None,
      'UsedCapacityInBytes' : None
    }
    self.element_lists = {
      ('Entries', None, CacheEntryInformation())
    }

class CacheInformation(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Filesystems', None, CacheFilesystemInformation())
    }

class BucketDetails(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Name' : None
    }
    self.element_lists = {}

class ListBucketResult(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'CreationDate' : None,
      'Delimiter' : None,
      'Marker' : None,
      'MaxKeys' : None,
      'Name' : None,
      'NextMarker' : None,
      'Prefix' : None,
      'IsTruncated' : None
    }
    self.element_lists = {
      ('CommonPrefixes', None, CommonPrefixes()),
      ('Contents', None, Contents())
    }

class ListAllMyBucketsResult(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Owner' : User()
    }
    self.element_lists = {
      ('Bucket', 'Buckets', BucketDetails())
    }

class CompleteMultipartUploadResult(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Bucket' : None,
      'ETag' : None,
      'Key' : None,
      'Location' : None
    }
    self.element_lists = {}

class DeleteObjectError(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Code' : None,
      'Key' : None,
      'Message' : None
    }
    self.element_lists = {}

class DeleteResult(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Deleted', None, S3ObjectToDelete()),
      ('Error', None, DeleteObjectError())
    }

class DetailedTapePartition(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DriveType' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'ImportExportConfiguration' : None,
      'LibraryId' : None,
      'Name' : None,
      'Quiesced' : None,
      'SerialNumber' : None,
      'State' : None
    }
    self.element_lists = {
      ('DriveTypes', None, None),
      ('TapeTypes', None, None)
    }

class Error(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Code' : None,
      'HttpErrorCode' : None,
      'Message' : None,
      'Resource' : None,
      'ResourceId' : None
    }
    self.element_lists = {}

class InitiateMultipartUploadResult(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Bucket' : None,
      'Key' : None,
      'UploadId' : None
    }
    self.element_lists = {}

class Job(object):
  def __init__(self):
    self.attributes = [
      'Aggregating',
      'BucketName',
      'CachedSizeInBytes',
      'ChunkClientProcessingOrderGuarantee',
      'CompletedSizeInBytes',
      'EntirelyInCache',
      'JobId',
      'Naked',
      'Name',
      'OriginalSizeInBytes',
      'Priority',
      'RequestType',
      'StartDate',
      'Status',
      'UserId',
      'UserName'
    ]
    self.elements = {}
    self.element_lists = {
      ('Node', 'Nodes', JobNode())
    }

class Objects(object):
  def __init__(self):
    self.attributes = [
      'ChunkId',
      'ChunkNumber',
      'NodeId'
    ]
    self.elements = {}
    self.element_lists = {
      ('Object', None, BulkObject())
    }

class MasterObjectList(object):
  def __init__(self):
    self.attributes = [
      'Aggregating',
      'BucketName',
      'CachedSizeInBytes',
      'ChunkClientProcessingOrderGuarantee',
      'CompletedSizeInBytes',
      'EntirelyInCache',
      'JobId',
      'Naked',
      'Name',
      'OriginalSizeInBytes',
      'Priority',
      'RequestType',
      'StartDate',
      'Status',
      'UserId',
      'UserName'
    ]
    self.elements = {}
    self.element_lists = {
      ('Node', 'Nodes', JobNode()),
      ('Objects', None, Objects())
    }

class JobList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Job', None, Job())
    }

class ListPartsResult(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Bucket' : None,
      'Key' : None,
      'MaxParts' : None,
      'NextPartNumberMarker' : None,
      'Owner' : User(),
      'PartNumberMarker' : None,
      'IsTruncated' : None,
      'UploadId' : None
    }
    self.element_lists = {
      ('Part', None, MultiPartUploadPart())
    }

class ListMultiPartUploadsResult(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Bucket' : None,
      'Delimiter' : None,
      'KeyMarker' : None,
      'MaxUploads' : None,
      'NextKeyMarker' : None,
      'NextUploadIdMarker' : None,
      'Prefix' : None,
      'IsTruncated' : None,
      'UploadIdMarker' : None
    }
    self.element_lists = {
      ('CommonPrefixes', None, CommonPrefixes()),
      ('Upload', None, MultiPartUpload())
    }

class MultiPartUpload(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Initiated' : None,
      'Key' : None,
      'Owner' : User(),
      'UploadId' : None
    }
    self.element_lists = {}

class MultiPartUploadPart(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'ETag' : None,
      'LastModified' : None,
      'PartNumber' : None
    }
    self.element_lists = {}

class JobNode(object):
  def __init__(self):
    self.attributes = [
      'EndPoint',
      'HttpPort',
      'HttpsPort',
      'Id'
    ]
    self.elements = {}
    self.element_lists = {}

class Contents(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'ETag' : None,
      'Key' : None,
      'LastModified' : None,
      'Owner' : User(),
      'Size' : None,
      'StorageClass' : None
    }
    self.element_lists = {}

class S3ObjectToDelete(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Key' : None
    }
    self.element_lists = {}

class User(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DisplayName' : None,
      'ID' : None
    }
    self.element_lists = {}

class DetailedS3Object(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Blobs' : BulkObjectList(),
      'BlobsBeingPersisted' : None,
      'BlobsDegraded' : None,
      'BlobsInCache' : None,
      'BlobsTotal' : None,
      'BucketId' : None,
      'CreationDate' : None,
      'ETag' : None,
      'Id' : None,
      'Latest' : None,
      'Name' : None,
      'Owner' : None,
      'Size' : None,
      'Type' : None,
      'Version' : None
    }
    self.element_lists = {}

class SystemInformation(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'ApiVersion' : None,
      'BackendActivated' : None,
      'BuildInformation' : BuildInformation(),
      'InstanceId' : None,
      'Now' : None,
      'SerialNumber' : None
    }
    self.element_lists = {}

class HealthVerificationResult(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DatabaseFilesystemFreeSpace' : None,
      'MsRequiredToVerifyDataPlannerHealth' : None
    }
    self.element_lists = {}

class NamedDetailedTapePartition(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'DriveType' : None,
      'ErrorMessage' : None,
      'Id' : None,
      'ImportExportConfiguration' : None,
      'LibraryId' : None,
      'Name' : None,
      'Quiesced' : None,
      'SerialNumber' : None,
      'State' : None
    }
    self.element_lists = {
      ('DriveTypes', None, None),
      ('TapeTypes', None, None)
    }

class TapeFailure(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Cause' : None,
      'Tape' : Tape()
    }
    self.element_lists = {}

class TapeFailureList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Failure', None, TapeFailure())
    }

class BucketAclList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('BucketAcl', None, BucketAcl())
    }

class DataPolicyAclList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('DataPolicyAcl', None, DataPolicyAcl())
    }

class BucketList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Bucket', None, Bucket())
    }

class CacheFilesystemList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('CacheFilesystem', None, CacheFilesystem())
    }

class DataPersistenceRuleList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('DataPersistenceRule', None, DataPersistenceRule())
    }

class DataPolicyList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('DataPolicy', None, DataPolicy())
    }

class DataReplicationRuleList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('DataReplicationRule', None, DataReplicationRule())
    }

class DegradedBlobList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('DegradedBlob', None, DegradedBlob())
    }

class SuspectBlobPoolList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('SuspectBlobPool', None, SuspectBlobPool())
    }

class SuspectBlobTapeList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('SuspectBlobTape', None, SuspectBlobTape())
    }

class SuspectBlobTargetList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('SuspectBlobTarget', None, SuspectBlobTarget())
    }

class GroupMemberList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('GroupMember', None, GroupMember())
    }

class GroupList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Group', None, Group())
    }

class ActiveJobList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Job', None, ActiveJob())
    }

class CanceledJobList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('CanceledJob', None, CanceledJob())
    }

class CompletedJobList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('CompletedJob', None, CompletedJob())
    }

class NodeList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Node', None, Node())
    }

class Ds3TargetFailureNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Ds3TargetFailureNotificationRegistration', None, Ds3TargetFailureNotificationRegistration())
    }

class JobCompletedNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('JobCompletedNotificationRegistration', None, JobCompletedNotificationRegistration())
    }

class JobCreatedNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('JobCreatedNotificationRegistration', None, JobCreatedNotificationRegistration())
    }

class JobCreationFailedNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('JobCreationFailedNotificationRegistration', None, JobCreationFailedNotificationRegistration())
    }

class S3ObjectCachedNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('S3ObjectCachedNotificationRegistration', None, S3ObjectCachedNotificationRegistration())
    }

class S3ObjectLostNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('S3ObjectLostNotificationRegistration', None, S3ObjectLostNotificationRegistration())
    }

class S3ObjectPersistedNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('S3ObjectPersistedNotificationRegistration', None, S3ObjectPersistedNotificationRegistration())
    }

class PoolFailureNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('PoolFailureNotificationRegistration', None, PoolFailureNotificationRegistration())
    }

class StorageDomainFailureNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('StorageDomainFailureNotificationRegistration', None, StorageDomainFailureNotificationRegistration())
    }

class SystemFailureNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('SystemFailureNotificationRegistration', None, SystemFailureNotificationRegistration())
    }

class TapeFailureNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapeFailureNotificationRegistration', None, TapeFailureNotificationRegistration())
    }

class TapePartitionFailureNotificationRegistrationList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapePartitionFailureNotificationRegistration', None, TapePartitionFailureNotificationRegistration())
    }

class S3ObjectList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('S3Object', None, S3Object())
    }

class DetailedS3ObjectList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Object', None, DetailedS3Object())
    }

class PoolFailureList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('PoolFailure', None, PoolFailure())
    }

class PoolPartitionList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('PoolPartition', None, PoolPartition())
    }

class PoolList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Pool', None, Pool())
    }

class StorageDomainFailureList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('StorageDomainFailure', None, StorageDomainFailure())
    }

class StorageDomainMemberList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('StorageDomainMember', None, StorageDomainMember())
    }

class StorageDomainList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('StorageDomain', None, StorageDomain())
    }

class SystemFailureList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('SystemFailure', None, SystemFailure())
    }

class TapeDensityDirectiveList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapeDensityDirective', None, TapeDensityDirective())
    }

class TapeDriveList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapeDrive', None, TapeDrive())
    }

class DetailedTapeFailureList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapeFailure', None, DetailedTapeFailure())
    }

class TapeLibraryList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapeLibrary', None, TapeLibrary())
    }

class TapePartitionFailureList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapePartitionFailure', None, TapePartitionFailure())
    }

class TapePartitionList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapePartition', None, TapePartition())
    }

class NamedDetailedTapePartitionList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('TapePartition', None, NamedDetailedTapePartition())
    }

class TapeList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Tape', None, Tape())
    }

class Ds3TargetFailureList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Ds3TargetFailure', None, Ds3TargetFailure())
    }

class Ds3TargetReadPreferenceList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Ds3TargetReadPreference', None, Ds3TargetReadPreference())
    }

class Ds3TargetList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('Ds3Target', None, Ds3Target())
    }

class SpectraUserList(object):
  def __init__(self):
    self.attributes = []
    self.elements = {}
    self.element_lists = {
      ('User', None, SpectraUser())
    }


class CommonPrefixes(object):
  def __init__(self):
    self.attributes = []
    self.elements = {
      'Prefix' : None
    }
    self.element_lists = {}

def parseModel(root, model):

  if root.tag is 'Data':
    children = list(root.iter())
    if not children:
      return None
    else:
      root = children[0]

  if root is None:
    raise TypeError('Nothing to parse: root node is None')

  # Primitive type
  if model is None:
    return root.text

  result = {}
  # Adds attributes to the result model
  for attr in model.attributes:
    temp = root.attrib.get(attr)
    if temp is not None:
      result[attr] = temp
    else:
      result[attr] = None

  # Adds child xmlNodes to the result model
  for elmt in model.elements:
    xmlElement = root.find(elmt)
    if xmlElement is not None:
      result[elmt] = parseModel(xmlElement, model.elements[elmt])
    else:
      result[elmt] = None

  # Adds lists of child xmlNodes to the result model
  for elmt in model.element_lists:
    xmlElements = None
    if elmt[1] is None:
      # No encapsulating node
      xmlElements = root.findall(elmt[0])
    else:
      # Get nodes from within encapsulating node
      encapsNode = root.find(elmt[1])
      if encapsNode is not None:
        xmlElements = encapsNode.findall(elmt[0])

    tempList = []
    for xmlElmt in xmlElements:
      tempList.append(parseModel(xmlElmt, elmt[2]))
    result[elmt[0] + 'List'] = tempList

  return result

# Request Handlers

class AbstractRequest(object):
  __metaclass__ = ABCMeta
  def __init__(self):
    self.path = '/'
    self.http_verb = HttpVerb.GET
    self.query_params = {}
    self.headers = {}
    self.body = None

class AbortMultiPartUploadRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name, upload_id):
    super(AbortMultiPartUploadRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name
    self.query_params['upload_id'] = upload_id



    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.DELETE

class CompleteMultiPartUploadRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name, part_list, upload_id):
    super(CompleteMultiPartUploadRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name
    self.query_params['upload_id'] = upload_id

    if part_list is not None:
      if not isinstance(part_list, PartList):
        raise TypeError('CompleteMultiPartUploadRequest should have request payload of type: PartList')
      self.body = xmldom.tostring(part_list.to_xml())



    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.POST

class PutBucketRequest(AbstractRequest):
  def __init__(self, bucket_name):
    super(PutBucketRequest, self).__init__()
    self.bucket_name = bucket_name



    self.path = '/' + bucket_name
    self.http_verb = HttpVerb.PUT

class PutMultiPartUploadPartRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name, part_number, request_payload, upload_id):
    super(PutMultiPartUploadPartRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name
    self.query_params['part_number'] = part_number
    self.query_params['upload_id'] = upload_id

    self.body = request_payload



    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.PUT

class PutObjectRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name, headers=None, job=None, offset=None, real_file_name=None, stream=None):
    super(PutObjectRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name

    if headers is not None:
      for key, val in headers.iteritems():
        if val:
          self.headers[key] = val
    self.object_name = typeCheckString(object_name)
    object_data = None
    if stream:
      object_data = stream
    else:
      effectiveFileName = self.object_name
      if real_file_name:
        effectiveFileName = typeCheckString(real_file_name)
      object_data = open(effectiveFileName, "rb")
    if offset:
      object_data.seek(offset, 0)
    self.body = object_data


    if job is not None:
      self.query_params['job'] = job
    if offset is not None:
      self.query_params['offset'] = offset

    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.PUT

class DeleteBucketRequest(AbstractRequest):
  def __init__(self, bucket_name):
    super(DeleteBucketRequest, self).__init__()
    self.bucket_name = bucket_name



    self.path = '/' + bucket_name
    self.http_verb = HttpVerb.DELETE

class DeleteObjectRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name, replicate=None, roll_back=None):
    super(DeleteObjectRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name


    if replicate is not None:
      self.query_params['replicate'] = replicate
    if roll_back is not None:
      self.query_params['roll_back'] = roll_back

    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.DELETE

class DeleteObjectsRequest(AbstractRequest):
  def __init__(self, bucket_name, object_list, replicate=None, roll_back=None):
    super(DeleteObjectsRequest, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['delete'] = None

    if object_list is not None:
      if not isinstance(object_list, DeleteObjectList):
        raise TypeError('DeleteObjectsRequest should have request payload of type: DeleteObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if replicate is not None:
      self.query_params['replicate'] = replicate
    if roll_back is not None:
      self.query_params['roll_back'] = roll_back

    self.path = '/' + bucket_name
    self.http_verb = HttpVerb.POST

class GetBucketRequest(AbstractRequest):
  def __init__(self, bucket_name, delimiter=None, marker=None, max_keys=None, prefix=None):
    super(GetBucketRequest, self).__init__()
    self.bucket_name = bucket_name


    if delimiter is not None:
      self.query_params['delimiter'] = delimiter
    if marker is not None:
      self.query_params['marker'] = marker
    if max_keys is not None:
      self.query_params['max_keys'] = max_keys
    if prefix is not None:
      self.query_params['prefix'] = prefix

    self.path = '/' + bucket_name
    self.http_verb = HttpVerb.GET

class GetServiceRequest(AbstractRequest):
  def __init__(self):
    super(GetServiceRequest, self).__init__()



    self.path = '/'
    self.http_verb = HttpVerb.GET

class GetObjectRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name, job=None, offset=None, real_file_name=None, stream=None):
    super(GetObjectRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name

    self.offset = offset
    self.stream = stream
    if real_file_name:
      self.effective_file_name = typeCheckString(real_file_name)
    else:
      self.effective_file_name = typeCheckString(object_name)


    if job is not None:
      self.query_params['job'] = job
    if offset is not None:
      self.query_params['offset'] = offset

    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.GET

class HeadBucketRequest(AbstractRequest):
  def __init__(self, bucket_name):
    super(HeadBucketRequest, self).__init__()
    self.bucket_name = bucket_name



    self.path = '/' + bucket_name
    self.http_verb = HttpVerb.HEAD

class HeadObjectRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name):
    super(HeadObjectRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name



    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.HEAD

class InitiateMultiPartUploadRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name):
    super(InitiateMultiPartUploadRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name
    self.query_params['uploads'] = None



    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.POST

class ListMultiPartUploadPartsRequest(AbstractRequest):
  def __init__(self, bucket_name, object_name, upload_id, max_parts=None, part_number_marker=None):
    super(ListMultiPartUploadPartsRequest, self).__init__()
    self.bucket_name = bucket_name
    self.object_name = object_name
    self.query_params['upload_id'] = upload_id


    if max_parts is not None:
      self.query_params['max_parts'] = max_parts
    if part_number_marker is not None:
      self.query_params['part_number_marker'] = part_number_marker

    self.path = '/' + bucket_name + '/' + object_name
    self.http_verb = HttpVerb.GET

class ListMultiPartUploadsRequest(AbstractRequest):
  def __init__(self, bucket_name, delimiter=None, key_marker=None, max_uploads=None, prefix=None, upload_id_marker=None):
    super(ListMultiPartUploadsRequest, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['uploads'] = None


    if delimiter is not None:
      self.query_params['delimiter'] = delimiter
    if key_marker is not None:
      self.query_params['key_marker'] = key_marker
    if max_uploads is not None:
      self.query_params['max_uploads'] = max_uploads
    if prefix is not None:
      self.query_params['prefix'] = prefix
    if upload_id_marker is not None:
      self.query_params['upload_id_marker'] = upload_id_marker

    self.path = '/' + bucket_name
    self.http_verb = HttpVerb.GET

class PutBucketAclForGroupSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id, group_id, permission):
    super(PutBucketAclForGroupSpectraS3Request, self).__init__()
    self.query_params['bucket_id'] = bucket_id
    self.query_params['group_id'] = group_id
    self.query_params['permission'] = permission



    self.path = '/_rest_/bucket_acl'
    self.http_verb = HttpVerb.POST

class PutBucketAclForUserSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id, permission, user_id):
    super(PutBucketAclForUserSpectraS3Request, self).__init__()
    self.query_params['bucket_id'] = bucket_id
    self.query_params['permission'] = permission
    self.query_params['user_id'] = user_id



    self.path = '/_rest_/bucket_acl'
    self.http_verb = HttpVerb.POST

class PutDataPolicyAclForGroupSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id, group_id):
    super(PutDataPolicyAclForGroupSpectraS3Request, self).__init__()
    self.query_params['data_policy_id'] = data_policy_id
    self.query_params['group_id'] = group_id



    self.path = '/_rest_/data_policy_acl'
    self.http_verb = HttpVerb.POST

class PutDataPolicyAclForUserSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id, user_id):
    super(PutDataPolicyAclForUserSpectraS3Request, self).__init__()
    self.query_params['data_policy_id'] = data_policy_id
    self.query_params['user_id'] = user_id



    self.path = '/_rest_/data_policy_acl'
    self.http_verb = HttpVerb.POST

class PutGlobalBucketAclForGroupSpectraS3Request(AbstractRequest):
  def __init__(self, group_id, permission):
    super(PutGlobalBucketAclForGroupSpectraS3Request, self).__init__()
    self.query_params['group_id'] = group_id
    self.query_params['permission'] = permission



    self.path = '/_rest_/bucket_acl'
    self.http_verb = HttpVerb.POST

class PutGlobalBucketAclForUserSpectraS3Request(AbstractRequest):
  def __init__(self, permission, user_id):
    super(PutGlobalBucketAclForUserSpectraS3Request, self).__init__()
    self.query_params['permission'] = permission
    self.query_params['user_id'] = user_id



    self.path = '/_rest_/bucket_acl'
    self.http_verb = HttpVerb.POST

class PutGlobalDataPolicyAclForGroupSpectraS3Request(AbstractRequest):
  def __init__(self, group_id):
    super(PutGlobalDataPolicyAclForGroupSpectraS3Request, self).__init__()
    self.query_params['group_id'] = group_id



    self.path = '/_rest_/data_policy_acl'
    self.http_verb = HttpVerb.POST

class PutGlobalDataPolicyAclForUserSpectraS3Request(AbstractRequest):
  def __init__(self, user_id):
    super(PutGlobalDataPolicyAclForUserSpectraS3Request, self).__init__()
    self.query_params['user_id'] = user_id



    self.path = '/_rest_/data_policy_acl'
    self.http_verb = HttpVerb.POST

class DeleteBucketAclSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_acl):
    super(DeleteBucketAclSpectraS3Request, self).__init__()
    self.bucket_acl = bucket_acl



    self.path = '/_rest_/bucket_acl/' + bucket_acl
    self.http_verb = HttpVerb.DELETE

class DeleteDataPolicyAclSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_acl):
    super(DeleteDataPolicyAclSpectraS3Request, self).__init__()
    self.data_policy_acl = data_policy_acl



    self.path = '/_rest_/data_policy_acl/' + data_policy_acl
    self.http_verb = HttpVerb.DELETE

class GetBucketAclSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_acl):
    super(GetBucketAclSpectraS3Request, self).__init__()
    self.bucket_acl = bucket_acl



    self.path = '/_rest_/bucket_acl/' + bucket_acl
    self.http_verb = HttpVerb.GET

class GetBucketAclsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, group_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, permission=None, user_id=None):
    super(GetBucketAclsSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if group_id is not None:
      self.query_params['group_id'] = group_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if permission is not None:
      self.query_params['permission'] = permission
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/bucket_acl'
    self.http_verb = HttpVerb.GET

class GetDataPolicyAclSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_acl):
    super(GetDataPolicyAclSpectraS3Request, self).__init__()
    self.data_policy_acl = data_policy_acl



    self.path = '/_rest_/data_policy_acl/' + data_policy_acl
    self.http_verb = HttpVerb.GET

class GetDataPolicyAclsSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id=None, group_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetDataPolicyAclsSpectraS3Request, self).__init__()


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if group_id is not None:
      self.query_params['group_id'] = group_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/data_policy_acl'
    self.http_verb = HttpVerb.GET

class PutBucketSpectraS3Request(AbstractRequest):
  def __init__(self, name, data_policy_id=None, id=None, user_id=None):
    super(PutBucketSpectraS3Request, self).__init__()
    self.query_params['name'] = name


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if id is not None:
      self.query_params['id'] = id
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/bucket'
    self.http_verb = HttpVerb.POST

class DeleteBucketSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, force=None, replicate=None):
    super(DeleteBucketSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name


    if force is not None:
      self.query_params['force'] = force
    if replicate is not None:
      self.query_params['replicate'] = replicate

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.DELETE

class GetBucketSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name):
    super(GetBucketSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name



    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.GET

class GetBucketsSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetBucketsSpectraS3Request, self).__init__()


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/bucket'
    self.http_verb = HttpVerb.GET

class ModifyBucketSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, data_policy_id=None, user_id=None):
    super(ModifyBucketSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.PUT

class ForceFullCacheReclaimSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(ForceFullCacheReclaimSpectraS3Request, self).__init__()
    self.query_params['reclaim'] = None



    self.path = '/_rest_/cache_filesystem'
    self.http_verb = HttpVerb.PUT

class GetCacheFilesystemSpectraS3Request(AbstractRequest):
  def __init__(self, cache_filesystem):
    super(GetCacheFilesystemSpectraS3Request, self).__init__()
    self.cache_filesystem = cache_filesystem



    self.path = '/_rest_/cache_filesystem/' + cache_filesystem
    self.http_verb = HttpVerb.GET

class GetCacheFilesystemsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, node_id=None, page_length=None, page_offset=None, page_start_marker=None):
    super(GetCacheFilesystemsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if node_id is not None:
      self.query_params['node_id'] = node_id
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker

    self.path = '/_rest_/cache_filesystem'
    self.http_verb = HttpVerb.GET

class GetCacheStateSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(GetCacheStateSpectraS3Request, self).__init__()



    self.path = '/_rest_/cache_state'
    self.http_verb = HttpVerb.GET

class ModifyCacheFilesystemSpectraS3Request(AbstractRequest):
  def __init__(self, cache_filesystem, auto_reclaim_initiate_threshold=None, auto_reclaim_terminate_threshold=None, burst_threshold=None, max_capacity_in_bytes=None):
    super(ModifyCacheFilesystemSpectraS3Request, self).__init__()
    self.cache_filesystem = cache_filesystem


    if auto_reclaim_initiate_threshold is not None:
      self.query_params['auto_reclaim_initiate_threshold'] = auto_reclaim_initiate_threshold
    if auto_reclaim_terminate_threshold is not None:
      self.query_params['auto_reclaim_terminate_threshold'] = auto_reclaim_terminate_threshold
    if burst_threshold is not None:
      self.query_params['burst_threshold'] = burst_threshold
    if max_capacity_in_bytes is not None:
      self.query_params['max_capacity_in_bytes'] = max_capacity_in_bytes

    self.path = '/_rest_/cache_filesystem/' + cache_filesystem
    self.http_verb = HttpVerb.PUT

class GetBucketCapacitySummarySpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id, storage_domain_id, pool_health=None, pool_state=None, pool_type=None, tape_state=None, tape_type=None):
    super(GetBucketCapacitySummarySpectraS3Request, self).__init__()
    self.query_params['bucket_id'] = bucket_id
    self.query_params['storage_domain_id'] = storage_domain_id


    if pool_health is not None:
      self.query_params['pool_health'] = pool_health
    if pool_state is not None:
      self.query_params['pool_state'] = pool_state
    if pool_type is not None:
      self.query_params['pool_type'] = pool_type
    if tape_state is not None:
      self.query_params['tape_state'] = tape_state
    if tape_type is not None:
      self.query_params['tape_type'] = tape_type

    self.path = '/_rest_/capacity_summary'
    self.http_verb = HttpVerb.GET

class GetStorageDomainCapacitySummarySpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain_id, pool_health=None, pool_state=None, pool_type=None, tape_state=None, tape_type=None):
    super(GetStorageDomainCapacitySummarySpectraS3Request, self).__init__()
    self.query_params['storage_domain_id'] = storage_domain_id


    if pool_health is not None:
      self.query_params['pool_health'] = pool_health
    if pool_state is not None:
      self.query_params['pool_state'] = pool_state
    if pool_type is not None:
      self.query_params['pool_type'] = pool_type
    if tape_state is not None:
      self.query_params['tape_state'] = tape_state
    if tape_type is not None:
      self.query_params['tape_type'] = tape_type

    self.path = '/_rest_/capacity_summary'
    self.http_verb = HttpVerb.GET

class GetSystemCapacitySummarySpectraS3Request(AbstractRequest):
  def __init__(self, pool_health=None, pool_state=None, pool_type=None, tape_state=None, tape_type=None):
    super(GetSystemCapacitySummarySpectraS3Request, self).__init__()


    if pool_health is not None:
      self.query_params['pool_health'] = pool_health
    if pool_state is not None:
      self.query_params['pool_state'] = pool_state
    if pool_type is not None:
      self.query_params['pool_type'] = pool_type
    if tape_state is not None:
      self.query_params['tape_state'] = tape_state
    if tape_type is not None:
      self.query_params['tape_type'] = tape_type

    self.path = '/_rest_/capacity_summary'
    self.http_verb = HttpVerb.GET

class GetDataPathBackendSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(GetDataPathBackendSpectraS3Request, self).__init__()



    self.path = '/_rest_/data_path_backend'
    self.http_verb = HttpVerb.GET

class GetDataPlannerBlobStoreTasksSpectraS3Request(AbstractRequest):
  def __init__(self, full_details=None):
    super(GetDataPlannerBlobStoreTasksSpectraS3Request, self).__init__()


    if full_details is not None:
      self.query_params['full_details'] = full_details

    self.path = '/_rest_/blob_store_task'
    self.http_verb = HttpVerb.GET

class ModifyDataPathBackendSpectraS3Request(AbstractRequest):
  def __init__(self, activated=None, auto_activate_timeout_in_mins=None, auto_inspect=None, default_import_conflict_resolution_mode=None, partially_verify_last_percent_of_tapes=None, unavailable_media_policy=None, unavailable_pool_max_job_retry_in_mins=None, unavailable_tape_partition_max_job_retry_in_mins=None):
    super(ModifyDataPathBackendSpectraS3Request, self).__init__()


    if activated is not None:
      self.query_params['activated'] = activated
    if auto_activate_timeout_in_mins is not None:
      self.query_params['auto_activate_timeout_in_mins'] = auto_activate_timeout_in_mins
    if auto_inspect is not None:
      self.query_params['auto_inspect'] = auto_inspect
    if default_import_conflict_resolution_mode is not None:
      self.query_params['default_import_conflict_resolution_mode'] = default_import_conflict_resolution_mode
    if partially_verify_last_percent_of_tapes is not None:
      self.query_params['partially_verify_last_percent_of_tapes'] = partially_verify_last_percent_of_tapes
    if unavailable_media_policy is not None:
      self.query_params['unavailable_media_policy'] = unavailable_media_policy
    if unavailable_pool_max_job_retry_in_mins is not None:
      self.query_params['unavailable_pool_max_job_retry_in_mins'] = unavailable_pool_max_job_retry_in_mins
    if unavailable_tape_partition_max_job_retry_in_mins is not None:
      self.query_params['unavailable_tape_partition_max_job_retry_in_mins'] = unavailable_tape_partition_max_job_retry_in_mins

    self.path = '/_rest_/data_path_backend'
    self.http_verb = HttpVerb.PUT

class PutDataPersistenceRuleSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id, isolation_level, storage_domain_id, type, minimum_days_to_retain=None):
    super(PutDataPersistenceRuleSpectraS3Request, self).__init__()
    self.query_params['data_policy_id'] = data_policy_id
    self.query_params['isolation_level'] = isolation_level
    self.query_params['storage_domain_id'] = storage_domain_id
    self.query_params['type'] = type


    if minimum_days_to_retain is not None:
      self.query_params['minimum_days_to_retain'] = minimum_days_to_retain

    self.path = '/_rest_/data_persistence_rule'
    self.http_verb = HttpVerb.POST

class PutDataPolicySpectraS3Request(AbstractRequest):
  def __init__(self, name, always_force_put_job_creation=None, always_minimize_spanning_across_media=None, always_replicate_deletes=None, blobbing_enabled=None, checksum_type=None, default_blob_size=None, default_get_job_priority=None, default_put_job_priority=None, default_verify_job_priority=None, end_to_end_crc_required=None, rebuild_priority=None, versioning=None):
    super(PutDataPolicySpectraS3Request, self).__init__()
    self.query_params['name'] = name


    if always_force_put_job_creation is not None:
      self.query_params['always_force_put_job_creation'] = always_force_put_job_creation
    if always_minimize_spanning_across_media is not None:
      self.query_params['always_minimize_spanning_across_media'] = always_minimize_spanning_across_media
    if always_replicate_deletes is not None:
      self.query_params['always_replicate_deletes'] = always_replicate_deletes
    if blobbing_enabled is not None:
      self.query_params['blobbing_enabled'] = blobbing_enabled
    if checksum_type is not None:
      self.query_params['checksum_type'] = checksum_type
    if default_blob_size is not None:
      self.query_params['default_blob_size'] = default_blob_size
    if default_get_job_priority is not None:
      self.query_params['default_get_job_priority'] = default_get_job_priority
    if default_put_job_priority is not None:
      self.query_params['default_put_job_priority'] = default_put_job_priority
    if default_verify_job_priority is not None:
      self.query_params['default_verify_job_priority'] = default_verify_job_priority
    if end_to_end_crc_required is not None:
      self.query_params['end_to_end_crc_required'] = end_to_end_crc_required
    if rebuild_priority is not None:
      self.query_params['rebuild_priority'] = rebuild_priority
    if versioning is not None:
      self.query_params['versioning'] = versioning

    self.path = '/_rest_/data_policy'
    self.http_verb = HttpVerb.POST

class PutDataReplicationRuleSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id, ds3_target_id, type, ds3_target_data_policy=None):
    super(PutDataReplicationRuleSpectraS3Request, self).__init__()
    self.query_params['data_policy_id'] = data_policy_id
    self.query_params['ds3_target_id'] = ds3_target_id
    self.query_params['type'] = type


    if ds3_target_data_policy is not None:
      self.query_params['ds3_target_data_policy'] = ds3_target_data_policy

    self.path = '/_rest_/data_replication_rule'
    self.http_verb = HttpVerb.POST

class DeleteDataPersistenceRuleSpectraS3Request(AbstractRequest):
  def __init__(self, data_persistence_rule):
    super(DeleteDataPersistenceRuleSpectraS3Request, self).__init__()
    self.data_persistence_rule = data_persistence_rule



    self.path = '/_rest_/data_persistence_rule/' + data_persistence_rule
    self.http_verb = HttpVerb.DELETE

class DeleteDataPolicySpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id):
    super(DeleteDataPolicySpectraS3Request, self).__init__()
    self.data_policy_id = data_policy_id



    self.path = '/_rest_/data_policy/' + data_policy_id
    self.http_verb = HttpVerb.DELETE

class DeleteDataReplicationRuleSpectraS3Request(AbstractRequest):
  def __init__(self, data_replication_rule):
    super(DeleteDataReplicationRuleSpectraS3Request, self).__init__()
    self.data_replication_rule = data_replication_rule



    self.path = '/_rest_/data_replication_rule/' + data_replication_rule
    self.http_verb = HttpVerb.DELETE

class GetDataPersistenceRuleSpectraS3Request(AbstractRequest):
  def __init__(self, data_persistence_rule):
    super(GetDataPersistenceRuleSpectraS3Request, self).__init__()
    self.data_persistence_rule = data_persistence_rule



    self.path = '/_rest_/data_persistence_rule/' + data_persistence_rule
    self.http_verb = HttpVerb.GET

class GetDataPersistenceRulesSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id=None, isolation_level=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, state=None, storage_domain_id=None, type=None):
    super(GetDataPersistenceRulesSpectraS3Request, self).__init__()


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if isolation_level is not None:
      self.query_params['isolation_level'] = isolation_level
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if state is not None:
      self.query_params['state'] = state
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/data_persistence_rule'
    self.http_verb = HttpVerb.GET

class GetDataPoliciesSpectraS3Request(AbstractRequest):
  def __init__(self, always_force_put_job_creation=None, always_minimize_spanning_across_media=None, always_replicate_deletes=None, checksum_type=None, end_to_end_crc_required=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None):
    super(GetDataPoliciesSpectraS3Request, self).__init__()


    if always_force_put_job_creation is not None:
      self.query_params['always_force_put_job_creation'] = always_force_put_job_creation
    if always_minimize_spanning_across_media is not None:
      self.query_params['always_minimize_spanning_across_media'] = always_minimize_spanning_across_media
    if always_replicate_deletes is not None:
      self.query_params['always_replicate_deletes'] = always_replicate_deletes
    if checksum_type is not None:
      self.query_params['checksum_type'] = checksum_type
    if end_to_end_crc_required is not None:
      self.query_params['end_to_end_crc_required'] = end_to_end_crc_required
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker

    self.path = '/_rest_/data_policy'
    self.http_verb = HttpVerb.GET

class GetDataPolicySpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id):
    super(GetDataPolicySpectraS3Request, self).__init__()
    self.data_policy_id = data_policy_id



    self.path = '/_rest_/data_policy/' + data_policy_id
    self.http_verb = HttpVerb.GET

class GetDataReplicationRuleSpectraS3Request(AbstractRequest):
  def __init__(self, data_replication_rule):
    super(GetDataReplicationRuleSpectraS3Request, self).__init__()
    self.data_replication_rule = data_replication_rule



    self.path = '/_rest_/data_replication_rule/' + data_replication_rule
    self.http_verb = HttpVerb.GET

class GetDataReplicationRulesSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id=None, ds3_target_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, state=None, type=None):
    super(GetDataReplicationRulesSpectraS3Request, self).__init__()


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if ds3_target_id is not None:
      self.query_params['ds3_target_id'] = ds3_target_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if state is not None:
      self.query_params['state'] = state
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/data_replication_rule'
    self.http_verb = HttpVerb.GET

class ModifyDataPersistenceRuleSpectraS3Request(AbstractRequest):
  def __init__(self, data_persistence_rule, isolation_level=None, minimum_days_to_retain=None, type=None):
    super(ModifyDataPersistenceRuleSpectraS3Request, self).__init__()
    self.data_persistence_rule = data_persistence_rule


    if isolation_level is not None:
      self.query_params['isolation_level'] = isolation_level
    if minimum_days_to_retain is not None:
      self.query_params['minimum_days_to_retain'] = minimum_days_to_retain
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/data_persistence_rule/' + data_persistence_rule
    self.http_verb = HttpVerb.PUT

class ModifyDataPolicySpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id, always_force_put_job_creation=None, always_minimize_spanning_across_media=None, always_replicate_deletes=None, blobbing_enabled=None, checksum_type=None, default_blob_size=None, default_get_job_priority=None, default_put_job_priority=None, default_verify_job_priority=None, end_to_end_crc_required=None, name=None, rebuild_priority=None, versioning=None):
    super(ModifyDataPolicySpectraS3Request, self).__init__()
    self.data_policy_id = data_policy_id


    if always_force_put_job_creation is not None:
      self.query_params['always_force_put_job_creation'] = always_force_put_job_creation
    if always_minimize_spanning_across_media is not None:
      self.query_params['always_minimize_spanning_across_media'] = always_minimize_spanning_across_media
    if always_replicate_deletes is not None:
      self.query_params['always_replicate_deletes'] = always_replicate_deletes
    if blobbing_enabled is not None:
      self.query_params['blobbing_enabled'] = blobbing_enabled
    if checksum_type is not None:
      self.query_params['checksum_type'] = checksum_type
    if default_blob_size is not None:
      self.query_params['default_blob_size'] = default_blob_size
    if default_get_job_priority is not None:
      self.query_params['default_get_job_priority'] = default_get_job_priority
    if default_put_job_priority is not None:
      self.query_params['default_put_job_priority'] = default_put_job_priority
    if default_verify_job_priority is not None:
      self.query_params['default_verify_job_priority'] = default_verify_job_priority
    if end_to_end_crc_required is not None:
      self.query_params['end_to_end_crc_required'] = end_to_end_crc_required
    if name is not None:
      self.query_params['name'] = name
    if rebuild_priority is not None:
      self.query_params['rebuild_priority'] = rebuild_priority
    if versioning is not None:
      self.query_params['versioning'] = versioning

    self.path = '/_rest_/data_policy/' + data_policy_id
    self.http_verb = HttpVerb.PUT

class ModifyDataReplicationRuleSpectraS3Request(AbstractRequest):
  def __init__(self, data_replication_rule, ds3_target_data_policy=None, type=None):
    super(ModifyDataReplicationRuleSpectraS3Request, self).__init__()
    self.data_replication_rule = data_replication_rule


    if ds3_target_data_policy is not None:
      self.query_params['ds3_target_data_policy'] = ds3_target_data_policy
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/data_replication_rule/' + data_replication_rule
    self.http_verb = HttpVerb.PUT

class ClearSuspectBlobPoolsSpectraS3Request(AbstractRequest):
  def __init__(self, force=None):
    super(ClearSuspectBlobPoolsSpectraS3Request, self).__init__()


    if force is not None:
      self.query_params['force'] = force

    self.path = '/_rest_/suspect_blob_pool'
    self.http_verb = HttpVerb.DELETE

class ClearSuspectBlobTapesSpectraS3Request(AbstractRequest):
  def __init__(self, force=None):
    super(ClearSuspectBlobTapesSpectraS3Request, self).__init__()


    if force is not None:
      self.query_params['force'] = force

    self.path = '/_rest_/suspect_blob_tape'
    self.http_verb = HttpVerb.DELETE

class ClearSuspectBlobTargetsSpectraS3Request(AbstractRequest):
  def __init__(self, force=None):
    super(ClearSuspectBlobTargetsSpectraS3Request, self).__init__()


    if force is not None:
      self.query_params['force'] = force

    self.path = '/_rest_/suspect_blob_target'
    self.http_verb = HttpVerb.DELETE

class GetDegradedBlobsSpectraS3Request(AbstractRequest):
  def __init__(self, blob_id=None, bucket_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, persistence_rule_id=None, replication_rule_id=None):
    super(GetDegradedBlobsSpectraS3Request, self).__init__()


    if blob_id is not None:
      self.query_params['blob_id'] = blob_id
    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if persistence_rule_id is not None:
      self.query_params['persistence_rule_id'] = persistence_rule_id
    if replication_rule_id is not None:
      self.query_params['replication_rule_id'] = replication_rule_id

    self.path = '/_rest_/degraded_blob'
    self.http_verb = HttpVerb.GET

class GetDegradedBucketsSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetDegradedBucketsSpectraS3Request, self).__init__()


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/degraded_bucket'
    self.http_verb = HttpVerb.GET

class GetDegradedDataPersistenceRulesSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id=None, isolation_level=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, state=None, storage_domain_id=None, type=None):
    super(GetDegradedDataPersistenceRulesSpectraS3Request, self).__init__()


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if isolation_level is not None:
      self.query_params['isolation_level'] = isolation_level
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if state is not None:
      self.query_params['state'] = state
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/degraded_data_persistence_rule'
    self.http_verb = HttpVerb.GET

class GetDegradedDataReplicationRulesSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id=None, ds3_target_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, state=None, type=None):
    super(GetDegradedDataReplicationRulesSpectraS3Request, self).__init__()


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if ds3_target_id is not None:
      self.query_params['ds3_target_id'] = ds3_target_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if state is not None:
      self.query_params['state'] = state
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/degraded_data_replication_rule'
    self.http_verb = HttpVerb.GET

class GetSuspectBlobPoolsSpectraS3Request(AbstractRequest):
  def __init__(self, blob_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, pool_id=None):
    super(GetSuspectBlobPoolsSpectraS3Request, self).__init__()


    if blob_id is not None:
      self.query_params['blob_id'] = blob_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if pool_id is not None:
      self.query_params['pool_id'] = pool_id

    self.path = '/_rest_/suspect_blob_pool'
    self.http_verb = HttpVerb.GET

class GetSuspectBlobTapesSpectraS3Request(AbstractRequest):
  def __init__(self, blob_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, tape_id=None):
    super(GetSuspectBlobTapesSpectraS3Request, self).__init__()


    if blob_id is not None:
      self.query_params['blob_id'] = blob_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if tape_id is not None:
      self.query_params['tape_id'] = tape_id

    self.path = '/_rest_/suspect_blob_tape'
    self.http_verb = HttpVerb.GET

class GetSuspectBlobTargetsSpectraS3Request(AbstractRequest):
  def __init__(self, blob_id=None, ds3_target_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None):
    super(GetSuspectBlobTargetsSpectraS3Request, self).__init__()


    if blob_id is not None:
      self.query_params['blob_id'] = blob_id
    if ds3_target_id is not None:
      self.query_params['ds3_target_id'] = ds3_target_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker

    self.path = '/_rest_/suspect_blob_target'
    self.http_verb = HttpVerb.GET

class GetSuspectBucketsSpectraS3Request(AbstractRequest):
  def __init__(self, data_policy_id=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetSuspectBucketsSpectraS3Request, self).__init__()


    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/suspect_bucket'
    self.http_verb = HttpVerb.GET

class GetSuspectObjectsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, storage_domain_id=None):
    super(GetSuspectObjectsSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id

    self.path = '/_rest_/suspect_object'
    self.http_verb = HttpVerb.GET

class GetSuspectObjectsWithFullDetailsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, storage_domain_id=None):
    super(GetSuspectObjectsWithFullDetailsSpectraS3Request, self).__init__()
    self.query_params['full_details'] = None


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id

    self.path = '/_rest_/suspect_object'
    self.http_verb = HttpVerb.GET

class MarkSuspectBlobPoolsAsDegradedSpectraS3Request(AbstractRequest):
  def __init__(self, force=None):
    super(MarkSuspectBlobPoolsAsDegradedSpectraS3Request, self).__init__()


    if force is not None:
      self.query_params['force'] = force

    self.path = '/_rest_/suspect_blob_pool'
    self.http_verb = HttpVerb.PUT

class MarkSuspectBlobTapesAsDegradedSpectraS3Request(AbstractRequest):
  def __init__(self, force=None):
    super(MarkSuspectBlobTapesAsDegradedSpectraS3Request, self).__init__()


    if force is not None:
      self.query_params['force'] = force

    self.path = '/_rest_/suspect_blob_tape'
    self.http_verb = HttpVerb.PUT

class MarkSuspectBlobTargetsAsDegradedSpectraS3Request(AbstractRequest):
  def __init__(self, force=None):
    super(MarkSuspectBlobTargetsAsDegradedSpectraS3Request, self).__init__()


    if force is not None:
      self.query_params['force'] = force

    self.path = '/_rest_/suspect_blob_target'
    self.http_verb = HttpVerb.PUT

class PutGroupGroupMemberSpectraS3Request(AbstractRequest):
  def __init__(self, group_id, member_group_id):
    super(PutGroupGroupMemberSpectraS3Request, self).__init__()
    self.query_params['group_id'] = group_id
    self.query_params['member_group_id'] = member_group_id



    self.path = '/_rest_/group_member'
    self.http_verb = HttpVerb.POST

class PutGroupSpectraS3Request(AbstractRequest):
  def __init__(self, name):
    super(PutGroupSpectraS3Request, self).__init__()
    self.query_params['name'] = name



    self.path = '/_rest_/group'
    self.http_verb = HttpVerb.POST

class PutUserGroupMemberSpectraS3Request(AbstractRequest):
  def __init__(self, group_id, member_user_id):
    super(PutUserGroupMemberSpectraS3Request, self).__init__()
    self.query_params['group_id'] = group_id
    self.query_params['member_user_id'] = member_user_id



    self.path = '/_rest_/group_member'
    self.http_verb = HttpVerb.POST

class DeleteGroupMemberSpectraS3Request(AbstractRequest):
  def __init__(self, group_member):
    super(DeleteGroupMemberSpectraS3Request, self).__init__()
    self.group_member = group_member



    self.path = '/_rest_/group_member/' + group_member
    self.http_verb = HttpVerb.DELETE

class DeleteGroupSpectraS3Request(AbstractRequest):
  def __init__(self, group):
    super(DeleteGroupSpectraS3Request, self).__init__()
    self.group = group



    self.path = '/_rest_/group/' + group
    self.http_verb = HttpVerb.DELETE

class GetGroupMemberSpectraS3Request(AbstractRequest):
  def __init__(self, group_member):
    super(GetGroupMemberSpectraS3Request, self).__init__()
    self.group_member = group_member



    self.path = '/_rest_/group_member/' + group_member
    self.http_verb = HttpVerb.GET

class GetGroupMembersSpectraS3Request(AbstractRequest):
  def __init__(self, group_id=None, last_page=None, member_group_id=None, member_user_id=None, page_length=None, page_offset=None, page_start_marker=None):
    super(GetGroupMembersSpectraS3Request, self).__init__()


    if group_id is not None:
      self.query_params['group_id'] = group_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if member_group_id is not None:
      self.query_params['member_group_id'] = member_group_id
    if member_user_id is not None:
      self.query_params['member_user_id'] = member_user_id
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker

    self.path = '/_rest_/group_member'
    self.http_verb = HttpVerb.GET

class GetGroupSpectraS3Request(AbstractRequest):
  def __init__(self, group):
    super(GetGroupSpectraS3Request, self).__init__()
    self.group = group



    self.path = '/_rest_/group/' + group
    self.http_verb = HttpVerb.GET

class GetGroupsSpectraS3Request(AbstractRequest):
  def __init__(self, built_in=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None):
    super(GetGroupsSpectraS3Request, self).__init__()


    if built_in is not None:
      self.query_params['built_in'] = built_in
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker

    self.path = '/_rest_/group'
    self.http_verb = HttpVerb.GET

class ModifyGroupSpectraS3Request(AbstractRequest):
  def __init__(self, group, name=None):
    super(ModifyGroupSpectraS3Request, self).__init__()
    self.group = group


    if name is not None:
      self.query_params['name'] = name

    self.path = '/_rest_/group/' + group
    self.http_verb = HttpVerb.PUT

class VerifyUserIsMemberOfGroupSpectraS3Request(AbstractRequest):
  def __init__(self, group, user_id=None):
    super(VerifyUserIsMemberOfGroupSpectraS3Request, self).__init__()
    self.group = group
    self.query_params['operation'] = 'verify'


    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/group/' + group
    self.http_verb = HttpVerb.PUT

class AllocateJobChunkSpectraS3Request(AbstractRequest):
  def __init__(self, job_chunk_id):
    super(AllocateJobChunkSpectraS3Request, self).__init__()
    self.job_chunk_id = job_chunk_id
    self.query_params['operation'] = 'allocate'



    self.path = '/_rest_/job_chunk/' + job_chunk_id
    self.http_verb = HttpVerb.PUT

class CancelActiveJobSpectraS3Request(AbstractRequest):
  def __init__(self, active_job_id):
    super(CancelActiveJobSpectraS3Request, self).__init__()
    self.active_job_id = active_job_id
    self.query_params['force'] = None



    self.path = '/_rest_/active_job/' + active_job_id
    self.http_verb = HttpVerb.DELETE

class CancelAllActiveJobsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, request_type=None):
    super(CancelAllActiveJobsSpectraS3Request, self).__init__()
    self.query_params['force'] = None


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if request_type is not None:
      self.query_params['request_type'] = request_type

    self.path = '/_rest_/active_job'
    self.http_verb = HttpVerb.DELETE

class CancelAllJobsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, request_type=None):
    super(CancelAllJobsSpectraS3Request, self).__init__()
    self.query_params['force'] = None


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if request_type is not None:
      self.query_params['request_type'] = request_type

    self.path = '/_rest_/job'
    self.http_verb = HttpVerb.DELETE

class CancelJobSpectraS3Request(AbstractRequest):
  def __init__(self, job_id):
    super(CancelJobSpectraS3Request, self).__init__()
    self.job_id = job_id
    self.query_params['force'] = None



    self.path = '/_rest_/job/' + job_id
    self.http_verb = HttpVerb.DELETE

class ClearAllCanceledJobsSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(ClearAllCanceledJobsSpectraS3Request, self).__init__()



    self.path = '/_rest_/canceled_job'
    self.http_verb = HttpVerb.DELETE

class ClearAllCompletedJobsSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(ClearAllCompletedJobsSpectraS3Request, self).__init__()



    self.path = '/_rest_/completed_job'
    self.http_verb = HttpVerb.DELETE

class GetBulkJobSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, object_list, aggregating=None, chunk_client_processing_order_guarantee=None, name=None, priority=None):
    super(GetBulkJobSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'start_bulk_get'

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('GetBulkJobSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if aggregating is not None:
      self.query_params['aggregating'] = aggregating
    if chunk_client_processing_order_guarantee is not None:
      self.query_params['chunk_client_processing_order_guarantee'] = chunk_client_processing_order_guarantee
    if name is not None:
      self.query_params['name'] = name
    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.PUT

class PutBulkJobSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, object_list, aggregating=None, force=None, ignore_naming_conflicts=None, max_upload_size=None, minimize_spanning_across_media=None, name=None, priority=None):
    super(PutBulkJobSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'start_bulk_put'

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('PutBulkJobSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if aggregating is not None:
      self.query_params['aggregating'] = aggregating
    if force is not None:
      self.query_params['force'] = force
    if ignore_naming_conflicts is not None:
      self.query_params['ignore_naming_conflicts'] = ignore_naming_conflicts
    if max_upload_size is not None:
      self.query_params['max_upload_size'] = max_upload_size
    if minimize_spanning_across_media is not None:
      self.query_params['minimize_spanning_across_media'] = minimize_spanning_across_media
    if name is not None:
      self.query_params['name'] = name
    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.PUT

class VerifyBulkJobSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, object_list, aggregating=None, name=None, priority=None):
    super(VerifyBulkJobSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'start_bulk_verify'

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('VerifyBulkJobSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if aggregating is not None:
      self.query_params['aggregating'] = aggregating
    if name is not None:
      self.query_params['name'] = name
    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.PUT

class GetActiveJobSpectraS3Request(AbstractRequest):
  def __init__(self, active_job_id):
    super(GetActiveJobSpectraS3Request, self).__init__()
    self.active_job_id = active_job_id



    self.path = '/_rest_/active_job/' + active_job_id
    self.http_verb = HttpVerb.GET

class GetActiveJobsSpectraS3Request(AbstractRequest):
  def __init__(self, aggregating=None, bucket_id=None, chunk_client_processing_order_guarantee=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, priority=None, rechunked=None, request_type=None, truncated=None, user_id=None):
    super(GetActiveJobsSpectraS3Request, self).__init__()


    if aggregating is not None:
      self.query_params['aggregating'] = aggregating
    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if chunk_client_processing_order_guarantee is not None:
      self.query_params['chunk_client_processing_order_guarantee'] = chunk_client_processing_order_guarantee
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if priority is not None:
      self.query_params['priority'] = priority
    if rechunked is not None:
      self.query_params['rechunked'] = rechunked
    if request_type is not None:
      self.query_params['request_type'] = request_type
    if truncated is not None:
      self.query_params['truncated'] = truncated
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/active_job'
    self.http_verb = HttpVerb.GET

class GetCanceledJobSpectraS3Request(AbstractRequest):
  def __init__(self, canceled_job):
    super(GetCanceledJobSpectraS3Request, self).__init__()
    self.canceled_job = canceled_job



    self.path = '/_rest_/canceled_job/' + canceled_job
    self.http_verb = HttpVerb.GET

class GetCanceledJobsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, canceled_due_to_timeout=None, chunk_client_processing_order_guarantee=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, priority=None, rechunked=None, request_type=None, truncated=None, user_id=None):
    super(GetCanceledJobsSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if canceled_due_to_timeout is not None:
      self.query_params['canceled_due_to_timeout'] = canceled_due_to_timeout
    if chunk_client_processing_order_guarantee is not None:
      self.query_params['chunk_client_processing_order_guarantee'] = chunk_client_processing_order_guarantee
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if priority is not None:
      self.query_params['priority'] = priority
    if rechunked is not None:
      self.query_params['rechunked'] = rechunked
    if request_type is not None:
      self.query_params['request_type'] = request_type
    if truncated is not None:
      self.query_params['truncated'] = truncated
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/canceled_job'
    self.http_verb = HttpVerb.GET

class GetCompletedJobSpectraS3Request(AbstractRequest):
  def __init__(self, completed_job):
    super(GetCompletedJobSpectraS3Request, self).__init__()
    self.completed_job = completed_job



    self.path = '/_rest_/completed_job/' + completed_job
    self.http_verb = HttpVerb.GET

class GetCompletedJobsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, chunk_client_processing_order_guarantee=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, priority=None, rechunked=None, request_type=None, truncated=None, user_id=None):
    super(GetCompletedJobsSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if chunk_client_processing_order_guarantee is not None:
      self.query_params['chunk_client_processing_order_guarantee'] = chunk_client_processing_order_guarantee
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if priority is not None:
      self.query_params['priority'] = priority
    if rechunked is not None:
      self.query_params['rechunked'] = rechunked
    if request_type is not None:
      self.query_params['request_type'] = request_type
    if truncated is not None:
      self.query_params['truncated'] = truncated
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/completed_job'
    self.http_verb = HttpVerb.GET

class GetJobChunkDaoSpectraS3Request(AbstractRequest):
  def __init__(self, job_chunk_dao):
    super(GetJobChunkDaoSpectraS3Request, self).__init__()
    self.job_chunk_dao = job_chunk_dao



    self.path = '/_rest_/job_chunk_dao/' + job_chunk_dao
    self.http_verb = HttpVerb.GET

class GetJobChunkSpectraS3Request(AbstractRequest):
  def __init__(self, job_chunk_id):
    super(GetJobChunkSpectraS3Request, self).__init__()
    self.job_chunk_id = job_chunk_id



    self.path = '/_rest_/job_chunk/' + job_chunk_id
    self.http_verb = HttpVerb.GET

class GetJobChunksReadyForClientProcessingSpectraS3Request(AbstractRequest):
  def __init__(self, job, job_chunk=None, preferred_number_of_chunks=None):
    super(GetJobChunksReadyForClientProcessingSpectraS3Request, self).__init__()
    self.query_params['job'] = job


    if job_chunk is not None:
      self.query_params['job_chunk'] = job_chunk
    if preferred_number_of_chunks is not None:
      self.query_params['preferred_number_of_chunks'] = preferred_number_of_chunks

    self.path = '/_rest_/job_chunk'
    self.http_verb = HttpVerb.GET

class GetJobSpectraS3Request(AbstractRequest):
  def __init__(self, job_id):
    super(GetJobSpectraS3Request, self).__init__()
    self.job_id = job_id



    self.path = '/_rest_/job/' + job_id
    self.http_verb = HttpVerb.GET

class GetJobToReplicateSpectraS3Request(AbstractRequest):
  def __init__(self, job_id):
    super(GetJobToReplicateSpectraS3Request, self).__init__()
    self.job_id = job_id
    self.query_params['replicate'] = None



    self.path = '/_rest_/job/' + job_id
    self.http_verb = HttpVerb.GET

class GetJobsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, full_details=None):
    super(GetJobsSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if full_details is not None:
      self.query_params['full_details'] = full_details

    self.path = '/_rest_/job'
    self.http_verb = HttpVerb.GET

class ModifyActiveJobSpectraS3Request(AbstractRequest):
  def __init__(self, active_job_id, created_at=None, name=None, priority=None):
    super(ModifyActiveJobSpectraS3Request, self).__init__()
    self.active_job_id = active_job_id


    if created_at is not None:
      self.query_params['created_at'] = created_at
    if name is not None:
      self.query_params['name'] = name
    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/active_job/' + active_job_id
    self.http_verb = HttpVerb.PUT

class ModifyJobSpectraS3Request(AbstractRequest):
  def __init__(self, job_id, created_at=None, name=None, priority=None):
    super(ModifyJobSpectraS3Request, self).__init__()
    self.job_id = job_id


    if created_at is not None:
      self.query_params['created_at'] = created_at
    if name is not None:
      self.query_params['name'] = name
    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/job/' + job_id
    self.http_verb = HttpVerb.PUT

class ReplicatePutJobSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, request_payload, priority=None):
    super(ReplicatePutJobSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'start_bulk_put'
    self.query_params['replicate'] = None

    self.body = request_payload


    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.PUT

class TruncateActiveJobSpectraS3Request(AbstractRequest):
  def __init__(self, active_job_id):
    super(TruncateActiveJobSpectraS3Request, self).__init__()
    self.active_job_id = active_job_id



    self.path = '/_rest_/active_job/' + active_job_id
    self.http_verb = HttpVerb.DELETE

class TruncateAllActiveJobsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, request_type=None):
    super(TruncateAllActiveJobsSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if request_type is not None:
      self.query_params['request_type'] = request_type

    self.path = '/_rest_/active_job'
    self.http_verb = HttpVerb.DELETE

class TruncateAllJobsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, request_type=None):
    super(TruncateAllJobsSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if request_type is not None:
      self.query_params['request_type'] = request_type

    self.path = '/_rest_/job'
    self.http_verb = HttpVerb.DELETE

class TruncateJobSpectraS3Request(AbstractRequest):
  def __init__(self, job_id):
    super(TruncateJobSpectraS3Request, self).__init__()
    self.job_id = job_id



    self.path = '/_rest_/job/' + job_id
    self.http_verb = HttpVerb.DELETE

class VerifySafeToCreatePutJobSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name):
    super(VerifySafeToCreatePutJobSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'verify_safe_to_start_bulk_put'



    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.PUT

class GetNodeSpectraS3Request(AbstractRequest):
  def __init__(self, node):
    super(GetNodeSpectraS3Request, self).__init__()
    self.node = node



    self.path = '/_rest_/node/' + node
    self.http_verb = HttpVerb.GET

class GetNodesSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None):
    super(GetNodesSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker

    self.path = '/_rest_/node'
    self.http_verb = HttpVerb.GET

class ModifyNodeSpectraS3Request(AbstractRequest):
  def __init__(self, node, dns_name=None, name=None):
    super(ModifyNodeSpectraS3Request, self).__init__()
    self.node = node


    if dns_name is not None:
      self.query_params['dns_name'] = dns_name
    if name is not None:
      self.query_params['name'] = name

    self.path = '/_rest_/node/' + node
    self.http_verb = HttpVerb.PUT

class PutDs3TargetFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutDs3TargetFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/ds3_target_failure_notification_registration'
    self.http_verb = HttpVerb.POST

class PutJobCompletedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, job_id=None, naming_convention=None, notification_http_method=None):
    super(PutJobCompletedNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if job_id is not None:
      self.query_params['job_id'] = job_id
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/job_completed_notification_registration'
    self.http_verb = HttpVerb.POST

class PutJobCreatedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutJobCreatedNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/job_created_notification_registration'
    self.http_verb = HttpVerb.POST

class PutJobCreationFailedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutJobCreationFailedNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/job_creation_failed_notification_registration'
    self.http_verb = HttpVerb.POST

class PutObjectCachedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, job_id=None, naming_convention=None, notification_http_method=None):
    super(PutObjectCachedNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if job_id is not None:
      self.query_params['job_id'] = job_id
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/object_cached_notification_registration'
    self.http_verb = HttpVerb.POST

class PutObjectLostNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutObjectLostNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/object_lost_notification_registration'
    self.http_verb = HttpVerb.POST

class PutObjectPersistedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, job_id=None, naming_convention=None, notification_http_method=None):
    super(PutObjectPersistedNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if job_id is not None:
      self.query_params['job_id'] = job_id
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/object_persisted_notification_registration'
    self.http_verb = HttpVerb.POST

class PutPoolFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutPoolFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/pool_failure_notification_registration'
    self.http_verb = HttpVerb.POST

class PutStorageDomainFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutStorageDomainFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/storage_domain_failure_notification_registration'
    self.http_verb = HttpVerb.POST

class PutSystemFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutSystemFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/system_failure_notification_registration'
    self.http_verb = HttpVerb.POST

class PutTapeFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutTapeFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/tape_failure_notification_registration'
    self.http_verb = HttpVerb.POST

class PutTapePartitionFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_end_point, format=None, naming_convention=None, notification_http_method=None):
    super(PutTapePartitionFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.query_params['notification_end_point'] = notification_end_point


    if format is not None:
      self.query_params['format'] = format
    if naming_convention is not None:
      self.query_params['naming_convention'] = naming_convention
    if notification_http_method is not None:
      self.query_params['notification_http_method'] = notification_http_method

    self.path = '/_rest_/tape_partition_failure_notification_registration'
    self.http_verb = HttpVerb.POST

class DeleteDs3TargetFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteDs3TargetFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/ds3_target_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteJobCompletedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteJobCompletedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/job_completed_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteJobCreatedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteJobCreatedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/job_created_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteJobCreationFailedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteJobCreationFailedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/job_creation_failed_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteObjectCachedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteObjectCachedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/object_cached_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteObjectLostNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteObjectLostNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/object_lost_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteObjectPersistedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteObjectPersistedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/object_persisted_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeletePoolFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeletePoolFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/pool_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteStorageDomainFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteStorageDomainFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/storage_domain_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteSystemFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteSystemFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/system_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteTapeFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteTapeFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/tape_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class DeleteTapePartitionFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(DeleteTapePartitionFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/tape_partition_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.DELETE

class GetDs3TargetFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetDs3TargetFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/ds3_target_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetDs3TargetFailureNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetDs3TargetFailureNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/ds3_target_failure_notification_registration'
    self.http_verb = HttpVerb.GET

class GetJobCompletedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetJobCompletedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/job_completed_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetJobCompletedNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetJobCompletedNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/job_completed_notification_registration'
    self.http_verb = HttpVerb.GET

class GetJobCreatedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetJobCreatedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/job_created_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetJobCreatedNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetJobCreatedNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/job_created_notification_registration'
    self.http_verb = HttpVerb.GET

class GetJobCreationFailedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetJobCreationFailedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/job_creation_failed_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetJobCreationFailedNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetJobCreationFailedNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/job_creation_failed_notification_registration'
    self.http_verb = HttpVerb.GET

class GetObjectCachedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetObjectCachedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/object_cached_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetObjectCachedNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetObjectCachedNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/object_cached_notification_registration'
    self.http_verb = HttpVerb.GET

class GetObjectLostNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetObjectLostNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/object_lost_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetObjectLostNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetObjectLostNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/object_lost_notification_registration'
    self.http_verb = HttpVerb.GET

class GetObjectPersistedNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetObjectPersistedNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/object_persisted_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetObjectPersistedNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetObjectPersistedNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/object_persisted_notification_registration'
    self.http_verb = HttpVerb.GET

class GetPoolFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetPoolFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/pool_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetPoolFailureNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetPoolFailureNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/pool_failure_notification_registration'
    self.http_verb = HttpVerb.GET

class GetStorageDomainFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetStorageDomainFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/storage_domain_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetStorageDomainFailureNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetStorageDomainFailureNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/storage_domain_failure_notification_registration'
    self.http_verb = HttpVerb.GET

class GetSystemFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetSystemFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/system_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetSystemFailureNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetSystemFailureNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/system_failure_notification_registration'
    self.http_verb = HttpVerb.GET

class GetTapeFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetTapeFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/tape_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetTapeFailureNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetTapeFailureNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/tape_failure_notification_registration'
    self.http_verb = HttpVerb.GET

class GetTapePartitionFailureNotificationRegistrationSpectraS3Request(AbstractRequest):
  def __init__(self, notification_id):
    super(GetTapePartitionFailureNotificationRegistrationSpectraS3Request, self).__init__()
    self.notification_id = notification_id



    self.path = '/_rest_/tape_partition_failure_notification_registration/' + notification_id
    self.http_verb = HttpVerb.GET

class GetTapePartitionFailureNotificationRegistrationsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, user_id=None):
    super(GetTapePartitionFailureNotificationRegistrationsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if user_id is not None:
      self.query_params['user_id'] = user_id

    self.path = '/_rest_/tape_partition_failure_notification_registration'
    self.http_verb = HttpVerb.GET

class DeleteFolderRecursivelySpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id, folder, replicate=None, roll_back=None):
    super(DeleteFolderRecursivelySpectraS3Request, self).__init__()
    self.folder = folder
    self.query_params['bucket_id'] = bucket_id
    self.query_params['recursive'] = None


    if replicate is not None:
      self.query_params['replicate'] = replicate
    if roll_back is not None:
      self.query_params['roll_back'] = roll_back

    self.path = '/_rest_/folder/' + folder
    self.http_verb = HttpVerb.DELETE

class GetBlobPersistenceSpectraS3Request(AbstractRequest):
  def __init__(self, request_payload):
    super(GetBlobPersistenceSpectraS3Request, self).__init__()

    self.body = request_payload



    self.path = '/_rest_/blob_persistence'
    self.http_verb = HttpVerb.GET

class GetObjectDetailsSpectraS3Request(AbstractRequest):
  def __init__(self, object_name, bucket_id):
    super(GetObjectDetailsSpectraS3Request, self).__init__()
    self.object_name = object_name
    self.query_params['bucket_id'] = bucket_id



    self.path = '/_rest_/object/' + object_name
    self.http_verb = HttpVerb.GET

class GetObjectsDetailsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, folder=None, last_page=None, latest=None, name=None, page_length=None, page_offset=None, page_start_marker=None, type=None, version=None):
    super(GetObjectsDetailsSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if folder is not None:
      self.query_params['folder'] = folder
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if latest is not None:
      self.query_params['latest'] = latest
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if type is not None:
      self.query_params['type'] = type
    if version is not None:
      self.query_params['version'] = version

    self.path = '/_rest_/object'
    self.http_verb = HttpVerb.GET

class GetObjectsWithFullDetailsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, folder=None, include_physical_placement=None, last_page=None, latest=None, name=None, page_length=None, page_offset=None, page_start_marker=None, type=None, version=None):
    super(GetObjectsWithFullDetailsSpectraS3Request, self).__init__()
    self.query_params['full_details'] = None


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if folder is not None:
      self.query_params['folder'] = folder
    if include_physical_placement is not None:
      self.query_params['include_physical_placement'] = include_physical_placement
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if latest is not None:
      self.query_params['latest'] = latest
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if type is not None:
      self.query_params['type'] = type
    if version is not None:
      self.query_params['version'] = version

    self.path = '/_rest_/object'
    self.http_verb = HttpVerb.GET

class GetPhysicalPlacementForObjectsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, object_list, storage_domain_id=None):
    super(GetPhysicalPlacementForObjectsSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'get_physical_placement'

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('GetPhysicalPlacementForObjectsSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.PUT

class GetPhysicalPlacementForObjectsWithFullDetailsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, object_list, storage_domain_id=None):
    super(GetPhysicalPlacementForObjectsWithFullDetailsSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'get_physical_placement'
    self.query_params['full_details'] = None

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('GetPhysicalPlacementForObjectsWithFullDetailsSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.PUT

class VerifyPhysicalPlacementForObjectsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, object_list, storage_domain_id=None):
    super(VerifyPhysicalPlacementForObjectsSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'verify_physical_placement'

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('VerifyPhysicalPlacementForObjectsSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.GET

class VerifyPhysicalPlacementForObjectsWithFullDetailsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_name, object_list, storage_domain_id=None):
    super(VerifyPhysicalPlacementForObjectsWithFullDetailsSpectraS3Request, self).__init__()
    self.bucket_name = bucket_name
    self.query_params['operation'] = 'verify_physical_placement'
    self.query_params['full_details'] = None

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('VerifyPhysicalPlacementForObjectsWithFullDetailsSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id

    self.path = '/_rest_/bucket/' + bucket_name
    self.http_verb = HttpVerb.GET

class CancelImportOnAllPoolsSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(CancelImportOnAllPoolsSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'cancel_import'



    self.path = '/_rest_/pool'
    self.http_verb = HttpVerb.PUT

class CancelImportPoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool):
    super(CancelImportPoolSpectraS3Request, self).__init__()
    self.pool = pool
    self.query_params['operation'] = 'cancel_import'



    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.PUT

class CompactAllPoolsSpectraS3Request(AbstractRequest):
  def __init__(self, priority=None):
    super(CompactAllPoolsSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'compact'


    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/pool'
    self.http_verb = HttpVerb.PUT

class CompactPoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool, priority=None):
    super(CompactPoolSpectraS3Request, self).__init__()
    self.pool = pool
    self.query_params['operation'] = 'compact'


    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.PUT

class PutPoolPartitionSpectraS3Request(AbstractRequest):
  def __init__(self, name, type):
    super(PutPoolPartitionSpectraS3Request, self).__init__()
    self.query_params['name'] = name
    self.query_params['type'] = type



    self.path = '/_rest_/pool_partition'
    self.http_verb = HttpVerb.POST

class DeallocatePoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool):
    super(DeallocatePoolSpectraS3Request, self).__init__()
    self.pool = pool
    self.query_params['operation'] = 'deallocate'



    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.PUT

class DeletePermanentlyLostPoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool):
    super(DeletePermanentlyLostPoolSpectraS3Request, self).__init__()
    self.pool = pool



    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.DELETE

class DeletePoolFailureSpectraS3Request(AbstractRequest):
  def __init__(self, pool_failure):
    super(DeletePoolFailureSpectraS3Request, self).__init__()
    self.pool_failure = pool_failure



    self.path = '/_rest_/pool_failure/' + pool_failure
    self.http_verb = HttpVerb.DELETE

class DeletePoolPartitionSpectraS3Request(AbstractRequest):
  def __init__(self, pool_partition):
    super(DeletePoolPartitionSpectraS3Request, self).__init__()
    self.pool_partition = pool_partition



    self.path = '/_rest_/pool_partition/' + pool_partition
    self.http_verb = HttpVerb.DELETE

class ForcePoolEnvironmentRefreshSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(ForcePoolEnvironmentRefreshSpectraS3Request, self).__init__()



    self.path = '/_rest_/pool_environment'
    self.http_verb = HttpVerb.PUT

class FormatAllForeignPoolsSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(FormatAllForeignPoolsSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'format'



    self.path = '/_rest_/pool'
    self.http_verb = HttpVerb.PUT

class FormatForeignPoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool):
    super(FormatForeignPoolSpectraS3Request, self).__init__()
    self.pool = pool
    self.query_params['operation'] = 'format'



    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.PUT

class GetBlobsOnPoolSpectraS3Request(AbstractRequest):
  def __init__(self, object_list, pool):
    super(GetBlobsOnPoolSpectraS3Request, self).__init__()
    self.pool = pool
    self.query_params['operation'] = 'get_physical_placement'

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('GetBlobsOnPoolSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())



    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.GET

class GetPoolFailuresSpectraS3Request(AbstractRequest):
  def __init__(self, error_message=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, pool_id=None, type=None):
    super(GetPoolFailuresSpectraS3Request, self).__init__()


    if error_message is not None:
      self.query_params['error_message'] = error_message
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if pool_id is not None:
      self.query_params['pool_id'] = pool_id
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/pool_failure'
    self.http_verb = HttpVerb.GET

class GetPoolPartitionSpectraS3Request(AbstractRequest):
  def __init__(self, pool_partition):
    super(GetPoolPartitionSpectraS3Request, self).__init__()
    self.pool_partition = pool_partition



    self.path = '/_rest_/pool_partition/' + pool_partition
    self.http_verb = HttpVerb.GET

class GetPoolPartitionsSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, type=None):
    super(GetPoolPartitionsSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/pool_partition'
    self.http_verb = HttpVerb.GET

class GetPoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool):
    super(GetPoolSpectraS3Request, self).__init__()
    self.pool = pool



    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.GET

class GetPoolsSpectraS3Request(AbstractRequest):
  def __init__(self, assigned_to_storage_domain=None, bucket_id=None, health=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, partition_id=None, powered_on=None, state=None, storage_domain_id=None, type=None):
    super(GetPoolsSpectraS3Request, self).__init__()


    if assigned_to_storage_domain is not None:
      self.query_params['assigned_to_storage_domain'] = assigned_to_storage_domain
    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if health is not None:
      self.query_params['health'] = health
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if partition_id is not None:
      self.query_params['partition_id'] = partition_id
    if powered_on is not None:
      self.query_params['powered_on'] = powered_on
    if state is not None:
      self.query_params['state'] = state
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/pool'
    self.http_verb = HttpVerb.GET

class ImportAllPoolsSpectraS3Request(AbstractRequest):
  def __init__(self, conflict_resolution_mode=None, data_policy_id=None, priority=None, storage_domain_id=None, user_id=None, verify_data_after_import=None, verify_data_prior_to_import=None):
    super(ImportAllPoolsSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'import'


    if conflict_resolution_mode is not None:
      self.query_params['conflict_resolution_mode'] = conflict_resolution_mode
    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if priority is not None:
      self.query_params['priority'] = priority
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if user_id is not None:
      self.query_params['user_id'] = user_id
    if verify_data_after_import is not None:
      self.query_params['verify_data_after_import'] = verify_data_after_import
    if verify_data_prior_to_import is not None:
      self.query_params['verify_data_prior_to_import'] = verify_data_prior_to_import

    self.path = '/_rest_/pool'
    self.http_verb = HttpVerb.PUT

class ImportPoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool, conflict_resolution_mode=None, data_policy_id=None, priority=None, storage_domain_id=None, user_id=None, verify_data_after_import=None, verify_data_prior_to_import=None):
    super(ImportPoolSpectraS3Request, self).__init__()
    self.pool = pool
    self.query_params['operation'] = 'import'


    if conflict_resolution_mode is not None:
      self.query_params['conflict_resolution_mode'] = conflict_resolution_mode
    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if priority is not None:
      self.query_params['priority'] = priority
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if user_id is not None:
      self.query_params['user_id'] = user_id
    if verify_data_after_import is not None:
      self.query_params['verify_data_after_import'] = verify_data_after_import
    if verify_data_prior_to_import is not None:
      self.query_params['verify_data_prior_to_import'] = verify_data_prior_to_import

    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.PUT

class ModifyAllPoolsSpectraS3Request(AbstractRequest):
  def __init__(self, quiesced):
    super(ModifyAllPoolsSpectraS3Request, self).__init__()
    self.query_params['quiesced'] = quiesced



    self.path = '/_rest_/pool'
    self.http_verb = HttpVerb.PUT

class ModifyPoolPartitionSpectraS3Request(AbstractRequest):
  def __init__(self, pool_partition, name=None):
    super(ModifyPoolPartitionSpectraS3Request, self).__init__()
    self.pool_partition = pool_partition


    if name is not None:
      self.query_params['name'] = name

    self.path = '/_rest_/pool_partition/' + pool_partition
    self.http_verb = HttpVerb.PUT

class ModifyPoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool, partition_id=None, quiesced=None):
    super(ModifyPoolSpectraS3Request, self).__init__()
    self.pool = pool


    if partition_id is not None:
      self.query_params['partition_id'] = partition_id
    if quiesced is not None:
      self.query_params['quiesced'] = quiesced

    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.PUT

class VerifyAllPoolsSpectraS3Request(AbstractRequest):
  def __init__(self, priority=None):
    super(VerifyAllPoolsSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'verify'


    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/pool'
    self.http_verb = HttpVerb.PUT

class VerifyPoolSpectraS3Request(AbstractRequest):
  def __init__(self, pool, priority=None):
    super(VerifyPoolSpectraS3Request, self).__init__()
    self.pool = pool
    self.query_params['operation'] = 'verify'


    if priority is not None:
      self.query_params['priority'] = priority

    self.path = '/_rest_/pool/' + pool
    self.http_verb = HttpVerb.PUT

class ConvertStorageDomainToDs3TargetSpectraS3Request(AbstractRequest):
  def __init__(self, convert_to_ds3_target, storage_domain):
    super(ConvertStorageDomainToDs3TargetSpectraS3Request, self).__init__()
    self.storage_domain = storage_domain
    self.query_params['convert_to_ds3_target'] = convert_to_ds3_target



    self.path = '/_rest_/storage_domain/' + storage_domain
    self.http_verb = HttpVerb.PUT

class PutPoolStorageDomainMemberSpectraS3Request(AbstractRequest):
  def __init__(self, pool_partition_id, storage_domain_id, write_preference=None):
    super(PutPoolStorageDomainMemberSpectraS3Request, self).__init__()
    self.query_params['pool_partition_id'] = pool_partition_id
    self.query_params['storage_domain_id'] = storage_domain_id


    if write_preference is not None:
      self.query_params['write_preference'] = write_preference

    self.path = '/_rest_/storage_domain_member'
    self.http_verb = HttpVerb.POST

class PutStorageDomainSpectraS3Request(AbstractRequest):
  def __init__(self, name, auto_eject_media_full_threshold=None, auto_eject_upon_cron=None, auto_eject_upon_job_cancellation=None, auto_eject_upon_job_completion=None, auto_eject_upon_media_full=None, ltfs_file_naming=None, maximum_auto_verification_frequency_in_days=None, max_tape_fragmentation_percent=None, media_ejection_allowed=None, secure_media_allocation=None, verify_prior_to_auto_eject=None, write_optimization=None):
    super(PutStorageDomainSpectraS3Request, self).__init__()
    self.query_params['name'] = name


    if auto_eject_media_full_threshold is not None:
      self.query_params['auto_eject_media_full_threshold'] = auto_eject_media_full_threshold
    if auto_eject_upon_cron is not None:
      self.query_params['auto_eject_upon_cron'] = auto_eject_upon_cron
    if auto_eject_upon_job_cancellation is not None:
      self.query_params['auto_eject_upon_job_cancellation'] = auto_eject_upon_job_cancellation
    if auto_eject_upon_job_completion is not None:
      self.query_params['auto_eject_upon_job_completion'] = auto_eject_upon_job_completion
    if auto_eject_upon_media_full is not None:
      self.query_params['auto_eject_upon_media_full'] = auto_eject_upon_media_full
    if ltfs_file_naming is not None:
      self.query_params['ltfs_file_naming'] = ltfs_file_naming
    if max_tape_fragmentation_percent is not None:
      self.query_params['max_tape_fragmentation_percent'] = max_tape_fragmentation_percent
    if maximum_auto_verification_frequency_in_days is not None:
      self.query_params['maximum_auto_verification_frequency_in_days'] = maximum_auto_verification_frequency_in_days
    if media_ejection_allowed is not None:
      self.query_params['media_ejection_allowed'] = media_ejection_allowed
    if secure_media_allocation is not None:
      self.query_params['secure_media_allocation'] = secure_media_allocation
    if verify_prior_to_auto_eject is not None:
      self.query_params['verify_prior_to_auto_eject'] = verify_prior_to_auto_eject
    if write_optimization is not None:
      self.query_params['write_optimization'] = write_optimization

    self.path = '/_rest_/storage_domain'
    self.http_verb = HttpVerb.POST

class PutTapeStorageDomainMemberSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain_id, tape_partition_id, tape_type, write_preference=None):
    super(PutTapeStorageDomainMemberSpectraS3Request, self).__init__()
    self.query_params['storage_domain_id'] = storage_domain_id
    self.query_params['tape_partition_id'] = tape_partition_id
    self.query_params['tape_type'] = tape_type


    if write_preference is not None:
      self.query_params['write_preference'] = write_preference

    self.path = '/_rest_/storage_domain_member'
    self.http_verb = HttpVerb.POST

class DeleteStorageDomainFailureSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain_failure):
    super(DeleteStorageDomainFailureSpectraS3Request, self).__init__()
    self.storage_domain_failure = storage_domain_failure



    self.path = '/_rest_/storage_domain_failure/' + storage_domain_failure
    self.http_verb = HttpVerb.DELETE

class DeleteStorageDomainMemberSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain_member):
    super(DeleteStorageDomainMemberSpectraS3Request, self).__init__()
    self.storage_domain_member = storage_domain_member



    self.path = '/_rest_/storage_domain_member/' + storage_domain_member
    self.http_verb = HttpVerb.DELETE

class DeleteStorageDomainSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain):
    super(DeleteStorageDomainSpectraS3Request, self).__init__()
    self.storage_domain = storage_domain



    self.path = '/_rest_/storage_domain/' + storage_domain
    self.http_verb = HttpVerb.DELETE

class GetStorageDomainFailuresSpectraS3Request(AbstractRequest):
  def __init__(self, error_message=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, storage_domain_id=None, type=None):
    super(GetStorageDomainFailuresSpectraS3Request, self).__init__()


    if error_message is not None:
      self.query_params['error_message'] = error_message
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/storage_domain_failure'
    self.http_verb = HttpVerb.GET

class GetStorageDomainMemberSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain_member):
    super(GetStorageDomainMemberSpectraS3Request, self).__init__()
    self.storage_domain_member = storage_domain_member



    self.path = '/_rest_/storage_domain_member/' + storage_domain_member
    self.http_verb = HttpVerb.GET

class GetStorageDomainMembersSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, pool_partition_id=None, state=None, storage_domain_id=None, tape_partition_id=None, tape_type=None, write_preference=None):
    super(GetStorageDomainMembersSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if pool_partition_id is not None:
      self.query_params['pool_partition_id'] = pool_partition_id
    if state is not None:
      self.query_params['state'] = state
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if tape_partition_id is not None:
      self.query_params['tape_partition_id'] = tape_partition_id
    if tape_type is not None:
      self.query_params['tape_type'] = tape_type
    if write_preference is not None:
      self.query_params['write_preference'] = write_preference

    self.path = '/_rest_/storage_domain_member'
    self.http_verb = HttpVerb.GET

class GetStorageDomainSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain):
    super(GetStorageDomainSpectraS3Request, self).__init__()
    self.storage_domain = storage_domain



    self.path = '/_rest_/storage_domain/' + storage_domain
    self.http_verb = HttpVerb.GET

class GetStorageDomainsSpectraS3Request(AbstractRequest):
  def __init__(self, auto_eject_upon_cron=None, auto_eject_upon_job_cancellation=None, auto_eject_upon_job_completion=None, auto_eject_upon_media_full=None, last_page=None, media_ejection_allowed=None, name=None, page_length=None, page_offset=None, page_start_marker=None, secure_media_allocation=None, write_optimization=None):
    super(GetStorageDomainsSpectraS3Request, self).__init__()


    if auto_eject_upon_cron is not None:
      self.query_params['auto_eject_upon_cron'] = auto_eject_upon_cron
    if auto_eject_upon_job_cancellation is not None:
      self.query_params['auto_eject_upon_job_cancellation'] = auto_eject_upon_job_cancellation
    if auto_eject_upon_job_completion is not None:
      self.query_params['auto_eject_upon_job_completion'] = auto_eject_upon_job_completion
    if auto_eject_upon_media_full is not None:
      self.query_params['auto_eject_upon_media_full'] = auto_eject_upon_media_full
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if media_ejection_allowed is not None:
      self.query_params['media_ejection_allowed'] = media_ejection_allowed
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if secure_media_allocation is not None:
      self.query_params['secure_media_allocation'] = secure_media_allocation
    if write_optimization is not None:
      self.query_params['write_optimization'] = write_optimization

    self.path = '/_rest_/storage_domain'
    self.http_verb = HttpVerb.GET

class ModifyStorageDomainMemberSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain_member, write_preference=None):
    super(ModifyStorageDomainMemberSpectraS3Request, self).__init__()
    self.storage_domain_member = storage_domain_member


    if write_preference is not None:
      self.query_params['write_preference'] = write_preference

    self.path = '/_rest_/storage_domain_member/' + storage_domain_member
    self.http_verb = HttpVerb.PUT

class ModifyStorageDomainSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain, auto_eject_media_full_threshold=None, auto_eject_upon_cron=None, auto_eject_upon_job_cancellation=None, auto_eject_upon_job_completion=None, auto_eject_upon_media_full=None, ltfs_file_naming=None, maximum_auto_verification_frequency_in_days=None, max_tape_fragmentation_percent=None, media_ejection_allowed=None, name=None, secure_media_allocation=None, verify_prior_to_auto_eject=None, write_optimization=None):
    super(ModifyStorageDomainSpectraS3Request, self).__init__()
    self.storage_domain = storage_domain


    if auto_eject_media_full_threshold is not None:
      self.query_params['auto_eject_media_full_threshold'] = auto_eject_media_full_threshold
    if auto_eject_upon_cron is not None:
      self.query_params['auto_eject_upon_cron'] = auto_eject_upon_cron
    if auto_eject_upon_job_cancellation is not None:
      self.query_params['auto_eject_upon_job_cancellation'] = auto_eject_upon_job_cancellation
    if auto_eject_upon_job_completion is not None:
      self.query_params['auto_eject_upon_job_completion'] = auto_eject_upon_job_completion
    if auto_eject_upon_media_full is not None:
      self.query_params['auto_eject_upon_media_full'] = auto_eject_upon_media_full
    if ltfs_file_naming is not None:
      self.query_params['ltfs_file_naming'] = ltfs_file_naming
    if max_tape_fragmentation_percent is not None:
      self.query_params['max_tape_fragmentation_percent'] = max_tape_fragmentation_percent
    if maximum_auto_verification_frequency_in_days is not None:
      self.query_params['maximum_auto_verification_frequency_in_days'] = maximum_auto_verification_frequency_in_days
    if media_ejection_allowed is not None:
      self.query_params['media_ejection_allowed'] = media_ejection_allowed
    if name is not None:
      self.query_params['name'] = name
    if secure_media_allocation is not None:
      self.query_params['secure_media_allocation'] = secure_media_allocation
    if verify_prior_to_auto_eject is not None:
      self.query_params['verify_prior_to_auto_eject'] = verify_prior_to_auto_eject
    if write_optimization is not None:
      self.query_params['write_optimization'] = write_optimization

    self.path = '/_rest_/storage_domain/' + storage_domain
    self.http_verb = HttpVerb.PUT

class GetSystemFailuresSpectraS3Request(AbstractRequest):
  def __init__(self, error_message=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, type=None):
    super(GetSystemFailuresSpectraS3Request, self).__init__()


    if error_message is not None:
      self.query_params['error_message'] = error_message
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/system_failure'
    self.http_verb = HttpVerb.GET

class GetSystemInformationSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(GetSystemInformationSpectraS3Request, self).__init__()



    self.path = '/_rest_/system_information'
    self.http_verb = HttpVerb.GET

class ResetInstanceIdentifierSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(ResetInstanceIdentifierSpectraS3Request, self).__init__()



    self.path = '/_rest_/instance_identifier'
    self.http_verb = HttpVerb.PUT

class VerifySystemHealthSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(VerifySystemHealthSpectraS3Request, self).__init__()



    self.path = '/_rest_/system_health'
    self.http_verb = HttpVerb.GET

class CancelEjectOnAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(CancelEjectOnAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'cancel_eject'



    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class CancelEjectTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id):
    super(CancelEjectTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'cancel_eject'



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class CancelFormatOnAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(CancelFormatOnAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'cancel_format'



    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class CancelFormatTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id):
    super(CancelFormatTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'cancel_format'



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class CancelImportOnAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(CancelImportOnAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'cancel_import'



    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class CancelImportTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id):
    super(CancelImportTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'cancel_import'



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class CancelOnlineOnAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(CancelOnlineOnAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'cancel_online'



    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class CancelOnlineTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id):
    super(CancelOnlineTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'cancel_online'



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class CancelVerifyOnAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(CancelVerifyOnAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'cancel_verify'



    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class CancelVerifyTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id):
    super(CancelVerifyTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'cancel_verify'



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class CleanTapeDriveSpectraS3Request(AbstractRequest):
  def __init__(self, tape_drive_id):
    super(CleanTapeDriveSpectraS3Request, self).__init__()
    self.tape_drive_id = tape_drive_id
    self.query_params['operation'] = 'clean'



    self.path = '/_rest_/tape_drive/' + tape_drive_id
    self.http_verb = HttpVerb.PUT

class PutTapeDensityDirectiveSpectraS3Request(AbstractRequest):
  def __init__(self, density, partition_id, tape_type):
    super(PutTapeDensityDirectiveSpectraS3Request, self).__init__()
    self.query_params['density'] = density
    self.query_params['partition_id'] = partition_id
    self.query_params['tape_type'] = tape_type



    self.path = '/_rest_/tape_density_directive'
    self.http_verb = HttpVerb.POST

class DeletePermanentlyLostTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id):
    super(DeletePermanentlyLostTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.DELETE

class DeleteTapeDensityDirectiveSpectraS3Request(AbstractRequest):
  def __init__(self, tape_density_directive):
    super(DeleteTapeDensityDirectiveSpectraS3Request, self).__init__()
    self.tape_density_directive = tape_density_directive



    self.path = '/_rest_/tape_density_directive/' + tape_density_directive
    self.http_verb = HttpVerb.DELETE

class DeleteTapeDriveSpectraS3Request(AbstractRequest):
  def __init__(self, tape_drive_id):
    super(DeleteTapeDriveSpectraS3Request, self).__init__()
    self.tape_drive_id = tape_drive_id



    self.path = '/_rest_/tape_drive/' + tape_drive_id
    self.http_verb = HttpVerb.DELETE

class DeleteTapeFailureSpectraS3Request(AbstractRequest):
  def __init__(self, tape_failure):
    super(DeleteTapeFailureSpectraS3Request, self).__init__()
    self.tape_failure = tape_failure



    self.path = '/_rest_/tape_failure/' + tape_failure
    self.http_verb = HttpVerb.DELETE

class DeleteTapePartitionFailureSpectraS3Request(AbstractRequest):
  def __init__(self, tape_partition_failure):
    super(DeleteTapePartitionFailureSpectraS3Request, self).__init__()
    self.tape_partition_failure = tape_partition_failure



    self.path = '/_rest_/tape_partition_failure/' + tape_partition_failure
    self.http_verb = HttpVerb.DELETE

class DeleteTapePartitionSpectraS3Request(AbstractRequest):
  def __init__(self, tape_partition):
    super(DeleteTapePartitionSpectraS3Request, self).__init__()
    self.tape_partition = tape_partition



    self.path = '/_rest_/tape_partition/' + tape_partition
    self.http_verb = HttpVerb.DELETE

class EjectAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self, eject_label=None, eject_location=None):
    super(EjectAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'eject'


    if eject_label is not None:
      self.query_params['eject_label'] = eject_label
    if eject_location is not None:
      self.query_params['eject_location'] = eject_location

    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class EjectStorageDomainBlobsSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id, storage_domain_id, eject_label=None, eject_location=None, object_list=None):
    super(EjectStorageDomainBlobsSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'eject'
    self.query_params['blobs'] = None
    self.query_params['bucket_id'] = bucket_id
    self.query_params['storage_domain_id'] = storage_domain_id

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('EjectStorageDomainBlobsSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if eject_label is not None:
      self.query_params['eject_label'] = eject_label
    if eject_location is not None:
      self.query_params['eject_location'] = eject_location

    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class EjectStorageDomainSpectraS3Request(AbstractRequest):
  def __init__(self, storage_domain_id, bucket_id=None, eject_label=None, eject_location=None, object_list=None):
    super(EjectStorageDomainSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'eject'
    self.query_params['storage_domain_id'] = storage_domain_id

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('EjectStorageDomainSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if eject_label is not None:
      self.query_params['eject_label'] = eject_label
    if eject_location is not None:
      self.query_params['eject_location'] = eject_location

    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class EjectTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id, eject_label=None, eject_location=None):
    super(EjectTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'eject'


    if eject_label is not None:
      self.query_params['eject_label'] = eject_label
    if eject_location is not None:
      self.query_params['eject_location'] = eject_location

    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class ForceTapeEnvironmentRefreshSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(ForceTapeEnvironmentRefreshSpectraS3Request, self).__init__()



    self.path = '/_rest_/tape_environment'
    self.http_verb = HttpVerb.PUT

class FormatAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self, force=None):
    super(FormatAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'format'


    if force is not None:
      self.query_params['force'] = force

    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class FormatTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id, force=None):
    super(FormatTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'format'


    if force is not None:
      self.query_params['force'] = force

    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class GetBlobsOnTapeSpectraS3Request(AbstractRequest):
  def __init__(self, object_list, tape_id):
    super(GetBlobsOnTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'get_physical_placement'

    if object_list is not None:
      if not isinstance(object_list, FileObjectList):
        raise TypeError('GetBlobsOnTapeSpectraS3Request should have request payload of type: FileObjectList')
      self.body = xmldom.tostring(object_list.to_xml())



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.GET

class GetTapeDensityDirectiveSpectraS3Request(AbstractRequest):
  def __init__(self, tape_density_directive):
    super(GetTapeDensityDirectiveSpectraS3Request, self).__init__()
    self.tape_density_directive = tape_density_directive



    self.path = '/_rest_/tape_density_directive/' + tape_density_directive
    self.http_verb = HttpVerb.GET

class GetTapeDensityDirectivesSpectraS3Request(AbstractRequest):
  def __init__(self, density=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, partition_id=None, tape_type=None):
    super(GetTapeDensityDirectivesSpectraS3Request, self).__init__()


    if density is not None:
      self.query_params['density'] = density
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if partition_id is not None:
      self.query_params['partition_id'] = partition_id
    if tape_type is not None:
      self.query_params['tape_type'] = tape_type

    self.path = '/_rest_/tape_density_directive'
    self.http_verb = HttpVerb.GET

class GetTapeDriveSpectraS3Request(AbstractRequest):
  def __init__(self, tape_drive_id):
    super(GetTapeDriveSpectraS3Request, self).__init__()
    self.tape_drive_id = tape_drive_id



    self.path = '/_rest_/tape_drive/' + tape_drive_id
    self.http_verb = HttpVerb.GET

class GetTapeDrivesSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, page_length=None, page_offset=None, page_start_marker=None, partition_id=None, serial_number=None, state=None, type=None):
    super(GetTapeDrivesSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if partition_id is not None:
      self.query_params['partition_id'] = partition_id
    if serial_number is not None:
      self.query_params['serial_number'] = serial_number
    if state is not None:
      self.query_params['state'] = state
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/tape_drive'
    self.http_verb = HttpVerb.GET

class GetTapeFailuresSpectraS3Request(AbstractRequest):
  def __init__(self, error_message=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, tape_drive_id=None, tape_id=None, type=None):
    super(GetTapeFailuresSpectraS3Request, self).__init__()


    if error_message is not None:
      self.query_params['error_message'] = error_message
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if tape_drive_id is not None:
      self.query_params['tape_drive_id'] = tape_drive_id
    if tape_id is not None:
      self.query_params['tape_id'] = tape_id
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/tape_failure'
    self.http_verb = HttpVerb.GET

class GetTapeLibrariesSpectraS3Request(AbstractRequest):
  def __init__(self, last_page=None, management_url=None, name=None, page_length=None, page_offset=None, page_start_marker=None, serial_number=None):
    super(GetTapeLibrariesSpectraS3Request, self).__init__()


    if last_page is not None:
      self.query_params['last_page'] = last_page
    if management_url is not None:
      self.query_params['management_url'] = management_url
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if serial_number is not None:
      self.query_params['serial_number'] = serial_number

    self.path = '/_rest_/tape_library'
    self.http_verb = HttpVerb.GET

class GetTapeLibrarySpectraS3Request(AbstractRequest):
  def __init__(self, tape_library_id):
    super(GetTapeLibrarySpectraS3Request, self).__init__()
    self.tape_library_id = tape_library_id



    self.path = '/_rest_/tape_library/' + tape_library_id
    self.http_verb = HttpVerb.GET

class GetTapePartitionFailuresSpectraS3Request(AbstractRequest):
  def __init__(self, error_message=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, partition_id=None, type=None):
    super(GetTapePartitionFailuresSpectraS3Request, self).__init__()


    if error_message is not None:
      self.query_params['error_message'] = error_message
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if partition_id is not None:
      self.query_params['partition_id'] = partition_id
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/tape_partition_failure'
    self.http_verb = HttpVerb.GET

class GetTapePartitionSpectraS3Request(AbstractRequest):
  def __init__(self, tape_partition):
    super(GetTapePartitionSpectraS3Request, self).__init__()
    self.tape_partition = tape_partition



    self.path = '/_rest_/tape_partition/' + tape_partition
    self.http_verb = HttpVerb.GET

class GetTapePartitionWithFullDetailsSpectraS3Request(AbstractRequest):
  def __init__(self, tape_partition):
    super(GetTapePartitionWithFullDetailsSpectraS3Request, self).__init__()
    self.tape_partition = tape_partition
    self.query_params['full_details'] = None



    self.path = '/_rest_/tape_partition/' + tape_partition
    self.http_verb = HttpVerb.GET

class GetTapePartitionsSpectraS3Request(AbstractRequest):
  def __init__(self, import_export_configuration=None, last_page=None, library_id=None, name=None, page_length=None, page_offset=None, page_start_marker=None, quiesced=None, serial_number=None, state=None):
    super(GetTapePartitionsSpectraS3Request, self).__init__()


    if import_export_configuration is not None:
      self.query_params['import_export_configuration'] = import_export_configuration
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if library_id is not None:
      self.query_params['library_id'] = library_id
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if quiesced is not None:
      self.query_params['quiesced'] = quiesced
    if serial_number is not None:
      self.query_params['serial_number'] = serial_number
    if state is not None:
      self.query_params['state'] = state

    self.path = '/_rest_/tape_partition'
    self.http_verb = HttpVerb.GET

class GetTapePartitionsWithFullDetailsSpectraS3Request(AbstractRequest):
  def __init__(self, import_export_configuration=None, last_page=None, library_id=None, name=None, page_length=None, page_offset=None, page_start_marker=None, quiesced=None, serial_number=None, state=None):
    super(GetTapePartitionsWithFullDetailsSpectraS3Request, self).__init__()
    self.query_params['full_details'] = None


    if import_export_configuration is not None:
      self.query_params['import_export_configuration'] = import_export_configuration
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if library_id is not None:
      self.query_params['library_id'] = library_id
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if quiesced is not None:
      self.query_params['quiesced'] = quiesced
    if serial_number is not None:
      self.query_params['serial_number'] = serial_number
    if state is not None:
      self.query_params['state'] = state

    self.path = '/_rest_/tape_partition'
    self.http_verb = HttpVerb.GET

class GetTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id):
    super(GetTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.GET

class GetTapesSpectraS3Request(AbstractRequest):
  def __init__(self, assigned_to_storage_domain=None, bar_code=None, bucket_id=None, eject_label=None, eject_location=None, full_of_data=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, partially_verified_end_of_tape=None, partition_id=None, previous_state=None, serial_number=None, state=None, storage_domain_id=None, type=None, write_protected=None):
    super(GetTapesSpectraS3Request, self).__init__()


    if assigned_to_storage_domain is not None:
      self.query_params['assigned_to_storage_domain'] = assigned_to_storage_domain
    if bar_code is not None:
      self.query_params['bar_code'] = bar_code
    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if eject_label is not None:
      self.query_params['eject_label'] = eject_label
    if eject_location is not None:
      self.query_params['eject_location'] = eject_location
    if full_of_data is not None:
      self.query_params['full_of_data'] = full_of_data
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if partially_verified_end_of_tape is not None:
      self.query_params['partially_verified_end_of_tape'] = partially_verified_end_of_tape
    if partition_id is not None:
      self.query_params['partition_id'] = partition_id
    if previous_state is not None:
      self.query_params['previous_state'] = previous_state
    if serial_number is not None:
      self.query_params['serial_number'] = serial_number
    if state is not None:
      self.query_params['state'] = state
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if type is not None:
      self.query_params['type'] = type
    if write_protected is not None:
      self.query_params['write_protected'] = write_protected

    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.GET

class ImportAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self, conflict_resolution_mode=None, data_policy_id=None, priority=None, storage_domain_id=None, user_id=None, verify_data_after_import=None, verify_data_prior_to_import=None):
    super(ImportAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'import'


    if conflict_resolution_mode is not None:
      self.query_params['conflict_resolution_mode'] = conflict_resolution_mode
    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if priority is not None:
      self.query_params['priority'] = priority
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if user_id is not None:
      self.query_params['user_id'] = user_id
    if verify_data_after_import is not None:
      self.query_params['verify_data_after_import'] = verify_data_after_import
    if verify_data_prior_to_import is not None:
      self.query_params['verify_data_prior_to_import'] = verify_data_prior_to_import

    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class ImportTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id, conflict_resolution_mode=None, data_policy_id=None, priority=None, storage_domain_id=None, user_id=None, verify_data_after_import=None, verify_data_prior_to_import=None):
    super(ImportTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'import'


    if conflict_resolution_mode is not None:
      self.query_params['conflict_resolution_mode'] = conflict_resolution_mode
    if data_policy_id is not None:
      self.query_params['data_policy_id'] = data_policy_id
    if priority is not None:
      self.query_params['priority'] = priority
    if storage_domain_id is not None:
      self.query_params['storage_domain_id'] = storage_domain_id
    if user_id is not None:
      self.query_params['user_id'] = user_id
    if verify_data_after_import is not None:
      self.query_params['verify_data_after_import'] = verify_data_after_import
    if verify_data_prior_to_import is not None:
      self.query_params['verify_data_prior_to_import'] = verify_data_prior_to_import

    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class InspectAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self, task_priority=None):
    super(InspectAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'inspect'


    if task_priority is not None:
      self.query_params['task_priority'] = task_priority

    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class InspectTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id, task_priority=None):
    super(InspectTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'inspect'


    if task_priority is not None:
      self.query_params['task_priority'] = task_priority

    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class ModifyAllTapePartitionsSpectraS3Request(AbstractRequest):
  def __init__(self, quiesced):
    super(ModifyAllTapePartitionsSpectraS3Request, self).__init__()
    self.query_params['quiesced'] = quiesced



    self.path = '/_rest_/tape_partition'
    self.http_verb = HttpVerb.PUT

class ModifyTapePartitionSpectraS3Request(AbstractRequest):
  def __init__(self, tape_partition, quiesced=None):
    super(ModifyTapePartitionSpectraS3Request, self).__init__()
    self.tape_partition = tape_partition


    if quiesced is not None:
      self.query_params['quiesced'] = quiesced

    self.path = '/_rest_/tape_partition/' + tape_partition
    self.http_verb = HttpVerb.PUT

class ModifyTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id, eject_label=None, eject_location=None, state=None):
    super(ModifyTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id


    if eject_label is not None:
      self.query_params['eject_label'] = eject_label
    if eject_location is not None:
      self.query_params['eject_location'] = eject_location
    if state is not None:
      self.query_params['state'] = state

    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class OnlineAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(OnlineAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'online'



    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class OnlineTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id):
    super(OnlineTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'online'



    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class VerifyAllTapesSpectraS3Request(AbstractRequest):
  def __init__(self, task_priority=None):
    super(VerifyAllTapesSpectraS3Request, self).__init__()
    self.query_params['operation'] = 'verify'


    if task_priority is not None:
      self.query_params['task_priority'] = task_priority

    self.path = '/_rest_/tape'
    self.http_verb = HttpVerb.PUT

class VerifyTapeSpectraS3Request(AbstractRequest):
  def __init__(self, tape_id, task_priority=None):
    super(VerifyTapeSpectraS3Request, self).__init__()
    self.tape_id = tape_id
    self.query_params['operation'] = 'verify'


    if task_priority is not None:
      self.query_params['task_priority'] = task_priority

    self.path = '/_rest_/tape/' + tape_id
    self.http_verb = HttpVerb.PUT

class PutDs3TargetReadPreferenceSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id, read_preference, target_id):
    super(PutDs3TargetReadPreferenceSpectraS3Request, self).__init__()
    self.query_params['bucket_id'] = bucket_id
    self.query_params['read_preference'] = read_preference
    self.query_params['target_id'] = target_id



    self.path = '/_rest_/ds3_target_read_preference'
    self.http_verb = HttpVerb.POST

class DeleteDs3TargetFailureSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target_failure):
    super(DeleteDs3TargetFailureSpectraS3Request, self).__init__()
    self.ds3_target_failure = ds3_target_failure



    self.path = '/_rest_/ds3_target_failure/' + ds3_target_failure
    self.http_verb = HttpVerb.DELETE

class DeleteDs3TargetReadPreferenceSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target_read_preference):
    super(DeleteDs3TargetReadPreferenceSpectraS3Request, self).__init__()
    self.ds3_target_read_preference = ds3_target_read_preference



    self.path = '/_rest_/ds3_target_read_preference/' + ds3_target_read_preference
    self.http_verb = HttpVerb.DELETE

class DeleteDs3TargetSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target):
    super(DeleteDs3TargetSpectraS3Request, self).__init__()
    self.ds3_target = ds3_target



    self.path = '/_rest_/ds3_target/' + ds3_target
    self.http_verb = HttpVerb.DELETE

class ForceTargetEnvironmentRefreshSpectraS3Request(AbstractRequest):
  def __init__(self):
    super(ForceTargetEnvironmentRefreshSpectraS3Request, self).__init__()



    self.path = '/_rest_/target_environment'
    self.http_verb = HttpVerb.PUT

class GetDs3TargetDataPoliciesSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target_data_policies):
    super(GetDs3TargetDataPoliciesSpectraS3Request, self).__init__()
    self.ds3_target_data_policies = ds3_target_data_policies



    self.path = '/_rest_/ds3_target_data_policies/' + ds3_target_data_policies
    self.http_verb = HttpVerb.GET

class GetDs3TargetFailuresSpectraS3Request(AbstractRequest):
  def __init__(self, error_message=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, target_id=None, type=None):
    super(GetDs3TargetFailuresSpectraS3Request, self).__init__()


    if error_message is not None:
      self.query_params['error_message'] = error_message
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if target_id is not None:
      self.query_params['target_id'] = target_id
    if type is not None:
      self.query_params['type'] = type

    self.path = '/_rest_/ds3_target_failure'
    self.http_verb = HttpVerb.GET

class GetDs3TargetReadPreferenceSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target_read_preference):
    super(GetDs3TargetReadPreferenceSpectraS3Request, self).__init__()
    self.ds3_target_read_preference = ds3_target_read_preference



    self.path = '/_rest_/ds3_target_read_preference/' + ds3_target_read_preference
    self.http_verb = HttpVerb.GET

class GetDs3TargetReadPreferencesSpectraS3Request(AbstractRequest):
  def __init__(self, bucket_id=None, last_page=None, page_length=None, page_offset=None, page_start_marker=None, read_preference=None, target_id=None):
    super(GetDs3TargetReadPreferencesSpectraS3Request, self).__init__()


    if bucket_id is not None:
      self.query_params['bucket_id'] = bucket_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if read_preference is not None:
      self.query_params['read_preference'] = read_preference
    if target_id is not None:
      self.query_params['target_id'] = target_id

    self.path = '/_rest_/ds3_target_read_preference'
    self.http_verb = HttpVerb.GET

class GetDs3TargetSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target):
    super(GetDs3TargetSpectraS3Request, self).__init__()
    self.ds3_target = ds3_target



    self.path = '/_rest_/ds3_target/' + ds3_target
    self.http_verb = HttpVerb.GET

class GetDs3TargetsSpectraS3Request(AbstractRequest):
  def __init__(self, admin_auth_id=None, data_path_end_point=None, data_path_https=None, data_path_port=None, data_path_proxy=None, data_path_verify_certificate=None, default_read_preference=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None, permit_going_out_of_sync=None, quiesced=None, state=None):
    super(GetDs3TargetsSpectraS3Request, self).__init__()


    if admin_auth_id is not None:
      self.query_params['admin_auth_id'] = admin_auth_id
    if data_path_end_point is not None:
      self.query_params['data_path_end_point'] = data_path_end_point
    if data_path_https is not None:
      self.query_params['data_path_https'] = data_path_https
    if data_path_port is not None:
      self.query_params['data_path_port'] = data_path_port
    if data_path_proxy is not None:
      self.query_params['data_path_proxy'] = data_path_proxy
    if data_path_verify_certificate is not None:
      self.query_params['data_path_verify_certificate'] = data_path_verify_certificate
    if default_read_preference is not None:
      self.query_params['default_read_preference'] = default_read_preference
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker
    if permit_going_out_of_sync is not None:
      self.query_params['permit_going_out_of_sync'] = permit_going_out_of_sync
    if quiesced is not None:
      self.query_params['quiesced'] = quiesced
    if state is not None:
      self.query_params['state'] = state

    self.path = '/_rest_/ds3_target'
    self.http_verb = HttpVerb.GET

class ModifyAllDs3TargetsSpectraS3Request(AbstractRequest):
  def __init__(self, quiesced):
    super(ModifyAllDs3TargetsSpectraS3Request, self).__init__()
    self.query_params['quiesced'] = quiesced



    self.path = '/_rest_/ds3_target'
    self.http_verb = HttpVerb.PUT

class ModifyDs3TargetSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target, access_control_replication=None, admin_auth_id=None, admin_secret_key=None, data_path_end_point=None, data_path_https=None, data_path_port=None, data_path_proxy=None, data_path_verify_certificate=None, default_read_preference=None, name=None, permit_going_out_of_sync=None, quiesced=None, replicated_user_default_data_policy=None):
    super(ModifyDs3TargetSpectraS3Request, self).__init__()
    self.ds3_target = ds3_target


    if access_control_replication is not None:
      self.query_params['access_control_replication'] = access_control_replication
    if admin_auth_id is not None:
      self.query_params['admin_auth_id'] = admin_auth_id
    if admin_secret_key is not None:
      self.query_params['admin_secret_key'] = admin_secret_key
    if data_path_end_point is not None:
      self.query_params['data_path_end_point'] = data_path_end_point
    if data_path_https is not None:
      self.query_params['data_path_https'] = data_path_https
    if data_path_port is not None:
      self.query_params['data_path_port'] = data_path_port
    if data_path_proxy is not None:
      self.query_params['data_path_proxy'] = data_path_proxy
    if data_path_verify_certificate is not None:
      self.query_params['data_path_verify_certificate'] = data_path_verify_certificate
    if default_read_preference is not None:
      self.query_params['default_read_preference'] = default_read_preference
    if name is not None:
      self.query_params['name'] = name
    if permit_going_out_of_sync is not None:
      self.query_params['permit_going_out_of_sync'] = permit_going_out_of_sync
    if quiesced is not None:
      self.query_params['quiesced'] = quiesced
    if replicated_user_default_data_policy is not None:
      self.query_params['replicated_user_default_data_policy'] = replicated_user_default_data_policy

    self.path = '/_rest_/ds3_target/' + ds3_target
    self.http_verb = HttpVerb.PUT

class PairBackRegisteredDs3TargetSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target, access_control_replication=None, admin_auth_id=None, admin_secret_key=None, data_path_end_point=None, data_path_https=None, data_path_port=None, data_path_proxy=None, data_path_verify_certificate=None, default_read_preference=None, name=None, permit_going_out_of_sync=None, replicated_user_default_data_policy=None):
    super(PairBackRegisteredDs3TargetSpectraS3Request, self).__init__()
    self.ds3_target = ds3_target
    self.query_params['operation'] = 'pair_back'


    if access_control_replication is not None:
      self.query_params['access_control_replication'] = access_control_replication
    if admin_auth_id is not None:
      self.query_params['admin_auth_id'] = admin_auth_id
    if admin_secret_key is not None:
      self.query_params['admin_secret_key'] = admin_secret_key
    if data_path_end_point is not None:
      self.query_params['data_path_end_point'] = data_path_end_point
    if data_path_https is not None:
      self.query_params['data_path_https'] = data_path_https
    if data_path_port is not None:
      self.query_params['data_path_port'] = data_path_port
    if data_path_proxy is not None:
      self.query_params['data_path_proxy'] = data_path_proxy
    if data_path_verify_certificate is not None:
      self.query_params['data_path_verify_certificate'] = data_path_verify_certificate
    if default_read_preference is not None:
      self.query_params['default_read_preference'] = default_read_preference
    if name is not None:
      self.query_params['name'] = name
    if permit_going_out_of_sync is not None:
      self.query_params['permit_going_out_of_sync'] = permit_going_out_of_sync
    if replicated_user_default_data_policy is not None:
      self.query_params['replicated_user_default_data_policy'] = replicated_user_default_data_policy

    self.path = '/_rest_/ds3_target/' + ds3_target
    self.http_verb = HttpVerb.PUT

class RegisterDs3TargetSpectraS3Request(AbstractRequest):
  def __init__(self, admin_auth_id, admin_secret_key, data_path_end_point, name, access_control_replication=None, data_path_https=None, data_path_port=None, data_path_proxy=None, data_path_verify_certificate=None, default_read_preference=None, permit_going_out_of_sync=None, replicated_user_default_data_policy=None):
    super(RegisterDs3TargetSpectraS3Request, self).__init__()
    self.query_params['admin_auth_id'] = admin_auth_id
    self.query_params['admin_secret_key'] = admin_secret_key
    self.query_params['data_path_end_point'] = data_path_end_point
    self.query_params['name'] = name


    if access_control_replication is not None:
      self.query_params['access_control_replication'] = access_control_replication
    if data_path_https is not None:
      self.query_params['data_path_https'] = data_path_https
    if data_path_port is not None:
      self.query_params['data_path_port'] = data_path_port
    if data_path_proxy is not None:
      self.query_params['data_path_proxy'] = data_path_proxy
    if data_path_verify_certificate is not None:
      self.query_params['data_path_verify_certificate'] = data_path_verify_certificate
    if default_read_preference is not None:
      self.query_params['default_read_preference'] = default_read_preference
    if permit_going_out_of_sync is not None:
      self.query_params['permit_going_out_of_sync'] = permit_going_out_of_sync
    if replicated_user_default_data_policy is not None:
      self.query_params['replicated_user_default_data_policy'] = replicated_user_default_data_policy

    self.path = '/_rest_/ds3_target'
    self.http_verb = HttpVerb.POST

class VerifyDs3TargetSpectraS3Request(AbstractRequest):
  def __init__(self, ds3_target, full_details=None):
    super(VerifyDs3TargetSpectraS3Request, self).__init__()
    self.ds3_target = ds3_target
    self.query_params['operation'] = 'verify'


    if full_details is not None:
      self.query_params['full_details'] = full_details

    self.path = '/_rest_/ds3_target/' + ds3_target
    self.http_verb = HttpVerb.PUT

class DelegateCreateUserSpectraS3Request(AbstractRequest):
  def __init__(self, name, id=None, secret_key=None):
    super(DelegateCreateUserSpectraS3Request, self).__init__()
    self.query_params['name'] = name


    if id is not None:
      self.query_params['id'] = id
    if secret_key is not None:
      self.query_params['secret_key'] = secret_key

    self.path = '/_rest_/user'
    self.http_verb = HttpVerb.POST

class DelegateDeleteUserSpectraS3Request(AbstractRequest):
  def __init__(self, user_id):
    super(DelegateDeleteUserSpectraS3Request, self).__init__()
    self.user_id = user_id



    self.path = '/_rest_/user/' + user_id
    self.http_verb = HttpVerb.DELETE

class GetUserSpectraS3Request(AbstractRequest):
  def __init__(self, user_id):
    super(GetUserSpectraS3Request, self).__init__()
    self.user_id = user_id



    self.path = '/_rest_/user/' + user_id
    self.http_verb = HttpVerb.GET

class GetUsersSpectraS3Request(AbstractRequest):
  def __init__(self, auth_id=None, default_data_policy_id=None, last_page=None, name=None, page_length=None, page_offset=None, page_start_marker=None):
    super(GetUsersSpectraS3Request, self).__init__()


    if auth_id is not None:
      self.query_params['auth_id'] = auth_id
    if default_data_policy_id is not None:
      self.query_params['default_data_policy_id'] = default_data_policy_id
    if last_page is not None:
      self.query_params['last_page'] = last_page
    if name is not None:
      self.query_params['name'] = name
    if page_length is not None:
      self.query_params['page_length'] = page_length
    if page_offset is not None:
      self.query_params['page_offset'] = page_offset
    if page_start_marker is not None:
      self.query_params['page_start_marker'] = page_start_marker

    self.path = '/_rest_/user'
    self.http_verb = HttpVerb.GET

class ModifyUserSpectraS3Request(AbstractRequest):
  def __init__(self, user_id, default_data_policy_id=None, name=None, secret_key=None):
    super(ModifyUserSpectraS3Request, self).__init__()
    self.user_id = user_id


    if default_data_policy_id is not None:
      self.query_params['default_data_policy_id'] = default_data_policy_id
    if name is not None:
      self.query_params['name'] = name
    if secret_key is not None:
      self.query_params['secret_key'] = secret_key

    self.path = '/_rest_/user/' + user_id
    self.http_verb = HttpVerb.PUT

class RegenerateUserSecretKeySpectraS3Request(AbstractRequest):
  def __init__(self, user_id):
    super(RegenerateUserSecretKeySpectraS3Request, self).__init__()
    self.user_id = user_id
    self.query_params['operation'] = 'regenerate_secret_key'



    self.path = '/_rest_/user/' + user_id
    self.http_verb = HttpVerb.PUT


# Response Handlers

class AbstractResponse(object):
  __metaclass__ = ABCMeta
  def __init__(self, response, request):
    self.request = request
    self.response = response
    self.result = None
    self.meta_data = None
    self.process_response(response)
    self.process_meta_data(response)

  def process_meta_data(self, response):
    headers = response.getheaders()
    if not headers:
      return
    meta_data = {}
    for header in headers:
      if header[0].startswith('x-amz-meta-'):
        values = header[1].split(',')
        meta_data[header[0][11:]] = values
    self.meta_data = meta_data

  def process_response(self, response):
    # this method must be implemented
    raise NotImplementedError("Request Implemented")

  def __check_status_codes__(self, expected_codes):
    if self.response.status not in expected_codes:
      err = "Return Code: Expected %s - Received %s" % (expected_codes, self.response.status)
      ds3_error = XmlSerializer().to_ds3error(self.response.read(), self.response.status, self.response.reason)
      raise RequestFailed(err, ds3_error)

  def parse_int_header(self, key, headers):
    if not headers:
      return None
    for header in headers:
      if header[0] == key:
        return int(header[1])
    return None

class AbortMultiPartUploadResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class CompleteMultiPartUploadResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CompleteMultipartUploadResult())

class PutBucketResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    

class PutMultiPartUploadPartResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    

class PutObjectResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    

class DeleteBucketResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteObjectResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteObjectsResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DeleteResult())

class GetBucketResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), ListBucketResult())

class GetServiceResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), ListAllMyBucketsResult())

class GetObjectResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200, 206])
    localFile = None
    if self.request.stream:
      localFile = self.request.stream
    else:
      localFile = open(self.request.effective_file_name, "wb")
    if self.request.offset:
      localFile.seek(self.request.offset, 0)
    localFile.write(response.read())
    localFile.close()


class HeadBucketResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200, 403, 404])
    self.status_code = self.response.status
    if self.response.status == 200:
      self.result = HeadRequestStatus.EXISTS
    elif self.response.status == 403:
      self.result = HeadRequestStatus.NOTAUTHORIZED
    elif self.response.status == 404:
      self.result = HeadRequestStatus.DOESNTEXIST
    else:
      self.result = HeadRequestStatus.UNKNOWN

class HeadObjectResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200, 403, 404])
    self.status_code = self.response.status
    if self.response.status == 200:
      self.result = HeadRequestStatus.EXISTS
    elif self.response.status == 403:
      self.result = HeadRequestStatus.NOTAUTHORIZED
    elif self.response.status == 404:
      self.result = HeadRequestStatus.DOESNTEXIST
    else:
      self.result = HeadRequestStatus.UNKNOWN

class InitiateMultiPartUploadResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), InitiateMultipartUploadResult())

class ListMultiPartUploadPartsResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), ListPartsResult())

class ListMultiPartUploadsResponse(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), ListMultiPartUploadsResult())

class PutBucketAclForGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketAcl())

class PutBucketAclForUserSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketAcl())

class PutDataPolicyAclForGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicyAcl())

class PutDataPolicyAclForUserSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicyAcl())

class PutGlobalBucketAclForGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketAcl())

class PutGlobalBucketAclForUserSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketAcl())

class PutGlobalDataPolicyAclForGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicyAcl())

class PutGlobalDataPolicyAclForUserSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicyAcl())

class DeleteBucketAclSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteDataPolicyAclSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetBucketAclSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketAcl())

class GetBucketAclsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketAclList())

class GetDataPolicyAclSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicyAcl())

class GetDataPolicyAclsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicyAclList())

class PutBucketSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), Bucket())

class DeleteBucketSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetBucketSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Bucket())

class GetBucketsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketList())

class ModifyBucketSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Bucket())

class ForceFullCacheReclaimSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetCacheFilesystemSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CacheFilesystem())

class GetCacheFilesystemsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CacheFilesystemList())

class GetCacheStateSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CacheInformation())

class ModifyCacheFilesystemSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CacheFilesystem())

class GetBucketCapacitySummarySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CapacitySummaryContainer())

class GetStorageDomainCapacitySummarySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CapacitySummaryContainer())

class GetSystemCapacitySummarySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CapacitySummaryContainer())

class GetDataPathBackendSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPathBackend())

class GetDataPlannerBlobStoreTasksSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BlobStoreTasksInformation())

class ModifyDataPathBackendSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPathBackend())

class PutDataPersistenceRuleSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPersistenceRule())

class PutDataPolicySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicy())

class PutDataReplicationRuleSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), DataReplicationRule())

class DeleteDataPersistenceRuleSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteDataPolicySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteDataReplicationRuleSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetDataPersistenceRuleSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPersistenceRule())

class GetDataPersistenceRulesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPersistenceRuleList())

class GetDataPoliciesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicyList())

class GetDataPolicySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicy())

class GetDataReplicationRuleSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataReplicationRule())

class GetDataReplicationRulesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataReplicationRuleList())

class ModifyDataPersistenceRuleSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPersistenceRule())

class ModifyDataPolicySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicy())

class ModifyDataReplicationRuleSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataReplicationRule())

class ClearSuspectBlobPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ClearSuspectBlobTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ClearSuspectBlobTargetsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetDegradedBlobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DegradedBlobList())

class GetDegradedBucketsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketList())

class GetDegradedDataPersistenceRulesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPersistenceRuleList())

class GetDegradedDataReplicationRulesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataReplicationRuleList())

class GetSuspectBlobPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SuspectBlobPoolList())

class GetSuspectBlobTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SuspectBlobTapeList())

class GetSuspectBlobTargetsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SuspectBlobTargetList())

class GetSuspectBucketsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BucketList())

class GetSuspectObjectsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PhysicalPlacement())

class GetSuspectObjectsWithFullDetailsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BulkObjectList())

class MarkSuspectBlobPoolsAsDegradedSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class MarkSuspectBlobTapesAsDegradedSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class MarkSuspectBlobTargetsAsDegradedSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class PutGroupGroupMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), GroupMember())

class PutGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), Group())

class PutUserGroupMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), GroupMember())

class DeleteGroupMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetGroupMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), GroupMember())

class GetGroupMembersSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), GroupMemberList())

class GetGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Group())

class GetGroupsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), GroupList())

class ModifyGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Group())

class VerifyUserIsMemberOfGroupSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200, 204])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Group())

class AllocateJobChunkSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Objects())

class CancelActiveJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class CancelAllActiveJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class CancelAllJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class CancelJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ClearAllCanceledJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ClearAllCompletedJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetBulkJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), MasterObjectList())

class PutBulkJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), MasterObjectList())

class VerifyBulkJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), MasterObjectList())

class GetActiveJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), ActiveJob())

class GetActiveJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), ActiveJobList())

class GetCanceledJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CanceledJob())

class GetCanceledJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CanceledJobList())

class GetCompletedJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CompletedJob())

class GetCompletedJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), CompletedJobList())

class GetJobChunkDaoSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), JobChunk())

class GetJobChunkSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Objects())

class GetJobChunksReadyForClientProcessingSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), MasterObjectList())

class GetJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), MasterObjectList())

class GetJobToReplicateSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), String())

class GetJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), JobList())

class ModifyActiveJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), MasterObjectList())

class ModifyJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), MasterObjectList())

class ReplicatePutJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200, 204])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), MasterObjectList())

class TruncateActiveJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class TruncateAllActiveJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class TruncateAllJobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class TruncateJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class VerifySafeToCreatePutJobSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    

class GetNodeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Node())

class GetNodesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), NodeList())

class ModifyNodeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Node())

class PutDs3TargetFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3TargetFailureNotificationRegistration())

class PutJobCompletedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCompletedNotificationRegistration())

class PutJobCreatedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCreatedNotificationRegistration())

class PutJobCreationFailedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCreationFailedNotificationRegistration())

class PutObjectCachedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectCachedNotificationRegistration())

class PutObjectLostNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectLostNotificationRegistration())

class PutObjectPersistedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectPersistedNotificationRegistration())

class PutPoolFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolFailureNotificationRegistration())

class PutStorageDomainFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainFailureNotificationRegistration())

class PutSystemFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), SystemFailureNotificationRegistration())

class PutTapeFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureNotificationRegistration())

class PutTapePartitionFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), TapePartitionFailureNotificationRegistration())

class DeleteDs3TargetFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteJobCompletedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteJobCreatedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteJobCreationFailedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteObjectCachedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteObjectLostNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteObjectPersistedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeletePoolFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteStorageDomainFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteSystemFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteTapeFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteTapePartitionFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetDs3TargetFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3TargetFailureNotificationRegistration())

class GetDs3TargetFailureNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3TargetFailureNotificationRegistrationList())

class GetJobCompletedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCompletedNotificationRegistration())

class GetJobCompletedNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCompletedNotificationRegistrationList())

class GetJobCreatedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCreatedNotificationRegistration())

class GetJobCreatedNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCreatedNotificationRegistrationList())

class GetJobCreationFailedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCreationFailedNotificationRegistration())

class GetJobCreationFailedNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), JobCreationFailedNotificationRegistrationList())

class GetObjectCachedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectCachedNotificationRegistration())

class GetObjectCachedNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectCachedNotificationRegistrationList())

class GetObjectLostNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectLostNotificationRegistration())

class GetObjectLostNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectLostNotificationRegistrationList())

class GetObjectPersistedNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectPersistedNotificationRegistration())

class GetObjectPersistedNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectPersistedNotificationRegistrationList())

class GetPoolFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolFailureNotificationRegistration())

class GetPoolFailureNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolFailureNotificationRegistrationList())

class GetStorageDomainFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainFailureNotificationRegistration())

class GetStorageDomainFailureNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainFailureNotificationRegistrationList())

class GetSystemFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SystemFailureNotificationRegistration())

class GetSystemFailureNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SystemFailureNotificationRegistrationList())

class GetTapeFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureNotificationRegistration())

class GetTapeFailureNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureNotificationRegistrationList())

class GetTapePartitionFailureNotificationRegistrationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapePartitionFailureNotificationRegistration())

class GetTapePartitionFailureNotificationRegistrationsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapePartitionFailureNotificationRegistrationList())

class DeleteFolderRecursivelySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetBlobPersistenceSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), String())

class GetObjectDetailsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), S3Object())

class GetObjectsDetailsSpectraS3Response(AbstractResponse):
  def __init__(self, response, request):
    self.paging_truncated = None
    self.paging_total_result_count = None
    super(self.__class__, self).__init__(response, request)

  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), S3ObjectList())
      self.paging_truncated = self.parse_int_header('page-truncated', response.getheaders())
      self.paging_total_result_count = self.parse_int_header('total-result-count', response.getheaders())

class GetObjectsWithFullDetailsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DetailedS3ObjectList())

class GetPhysicalPlacementForObjectsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PhysicalPlacement())

class GetPhysicalPlacementForObjectsWithFullDetailsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BulkObjectList())

class VerifyPhysicalPlacementForObjectsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PhysicalPlacement())

class VerifyPhysicalPlacementForObjectsWithFullDetailsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BulkObjectList())

class CancelImportOnAllPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class CancelImportPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Pool())

class CompactAllPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class CompactPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Pool())

class PutPoolPartitionSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolPartition())

class DeallocatePoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeletePermanentlyLostPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeletePoolFailureSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeletePoolPartitionSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ForcePoolEnvironmentRefreshSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class FormatAllForeignPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class FormatForeignPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Pool())

class GetBlobsOnPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BulkObjectList())

class GetPoolFailuresSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolFailureList())

class GetPoolPartitionSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolPartition())

class GetPoolPartitionsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolPartitionList())

class GetPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Pool())

class GetPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolList())

class ImportAllPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ImportPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Pool())

class ModifyAllPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ModifyPoolPartitionSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), PoolPartition())

class ModifyPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Pool())

class VerifyAllPoolsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class VerifyPoolSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Pool())

class ConvertStorageDomainToDs3TargetSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class PutPoolStorageDomainMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainMember())

class PutStorageDomainSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomain())

class PutTapeStorageDomainMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainMember())

class DeleteStorageDomainFailureSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteStorageDomainMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteStorageDomainSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetStorageDomainFailuresSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainFailureList())

class GetStorageDomainMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainMember())

class GetStorageDomainMembersSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainMemberList())

class GetStorageDomainSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomain())

class GetStorageDomainsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainList())

class ModifyStorageDomainMemberSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomainMember())

class ModifyStorageDomainSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), StorageDomain())

class GetSystemFailuresSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SystemFailureList())

class GetSystemInformationSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SystemInformation())

class ResetInstanceIdentifierSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPathBackend())

class VerifySystemHealthSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), HealthVerificationResult())

class CancelEjectOnAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class CancelEjectTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class CancelFormatOnAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class CancelFormatTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class CancelImportOnAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class CancelImportTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class CancelOnlineOnAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class CancelOnlineTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class CancelVerifyOnAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class CancelVerifyTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class CleanTapeDriveSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeDrive())

class PutTapeDensityDirectiveSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeDensityDirective())

class DeletePermanentlyLostTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteTapeDensityDirectiveSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteTapeDriveSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteTapeFailureSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteTapePartitionFailureSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteTapePartitionSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class EjectAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class EjectStorageDomainBlobsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class EjectStorageDomainSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class EjectTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class ForceTapeEnvironmentRefreshSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class FormatAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class FormatTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class GetBlobsOnTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), BulkObjectList())

class GetTapeDensityDirectiveSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeDensityDirective())

class GetTapeDensityDirectivesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeDensityDirectiveList())

class GetTapeDriveSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeDrive())

class GetTapeDrivesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeDriveList())

class GetTapeFailuresSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DetailedTapeFailureList())

class GetTapeLibrariesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeLibraryList())

class GetTapeLibrarySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeLibrary())

class GetTapePartitionFailuresSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapePartitionFailureList())

class GetTapePartitionSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapePartition())

class GetTapePartitionWithFullDetailsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DetailedTapePartition())

class GetTapePartitionsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapePartitionList())

class GetTapePartitionsWithFullDetailsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), NamedDetailedTapePartitionList())

class GetTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class GetTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeList())

class ImportAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ImportTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class InspectAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class InspectTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class ModifyAllTapePartitionsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ModifyTapePartitionSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), TapePartition())

class ModifyTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class OnlineAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class OnlineTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class VerifyAllTapesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204, 207])
    if self.response.status == 207:
      self.result = parseModel(xmldom.fromstring(response.read()), TapeFailureList())

class VerifyTapeSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Tape())

class PutDs3TargetReadPreferenceSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3TargetReadPreference())

class DeleteDs3TargetFailureSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteDs3TargetReadPreferenceSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class DeleteDs3TargetSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ForceTargetEnvironmentRefreshSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetDs3TargetDataPoliciesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), DataPolicyList())

class GetDs3TargetFailuresSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3TargetFailureList())

class GetDs3TargetReadPreferenceSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3TargetReadPreference())

class GetDs3TargetReadPreferencesSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3TargetReadPreferenceList())

class GetDs3TargetSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3Target())

class GetDs3TargetsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3TargetList())

class ModifyAllDs3TargetsSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class ModifyDs3TargetSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3Target())

class PairBackRegisteredDs3TargetSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class RegisterDs3TargetSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3Target())

class VerifyDs3TargetSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), Ds3Target())

class DelegateCreateUserSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([201])
    if self.response.status == 201:
      self.result = parseModel(xmldom.fromstring(response.read()), SpectraUser())

class DelegateDeleteUserSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([204])
    

class GetUserSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SpectraUser())

class GetUsersSpectraS3Response(AbstractResponse):
  def __init__(self, response, request):
    self.paging_truncated = None
    self.paging_total_result_count = None
    super(self.__class__, self).__init__(response, request)

  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SpectraUserList())
      self.paging_truncated = self.parse_int_header('page-truncated', response.getheaders())
      self.paging_total_result_count = self.parse_int_header('total-result-count', response.getheaders())

class ModifyUserSpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SpectraUser())

class RegenerateUserSecretKeySpectraS3Response(AbstractResponse):
  
  def process_response(self, response):
    self.__check_status_codes__([200])
    if self.response.status == 200:
      self.result = parseModel(xmldom.fromstring(response.read()), SpectraUser())


class Client(object):
  def __init__(self, endpoint, credentials, proxy=None):
    self.net_client = NetworkClient(endpoint, credentials)
    if proxy is not None:
      self.net_client = self.net_client.with_proxy(proxy)

  def get_net_client(self):
    return self.net_client

  def abort_multi_part_upload(self, request):
    return AbortMultiPartUploadResponse(self.net_client.get_response(request), request)

  def complete_multi_part_upload(self, request):
    return CompleteMultiPartUploadResponse(self.net_client.get_response(request), request)

  def put_bucket(self, request):
    return PutBucketResponse(self.net_client.get_response(request), request)

  def put_multi_part_upload_part(self, request):
    return PutMultiPartUploadPartResponse(self.net_client.get_response(request), request)

  def put_object(self, request):
    return PutObjectResponse(self.net_client.get_response(request), request)

  def delete_bucket(self, request):
    return DeleteBucketResponse(self.net_client.get_response(request), request)

  def delete_object(self, request):
    return DeleteObjectResponse(self.net_client.get_response(request), request)

  def delete_objects(self, request):
    return DeleteObjectsResponse(self.net_client.get_response(request), request)

  def get_bucket(self, request):
    return GetBucketResponse(self.net_client.get_response(request), request)

  def get_service(self, request):
    return GetServiceResponse(self.net_client.get_response(request), request)

  def get_object(self, request):
    return GetObjectResponse(self.net_client.get_response(request), request)

  def head_bucket(self, request):
    return HeadBucketResponse(self.net_client.get_response(request), request)

  def head_object(self, request):
    return HeadObjectResponse(self.net_client.get_response(request), request)

  def initiate_multi_part_upload(self, request):
    return InitiateMultiPartUploadResponse(self.net_client.get_response(request), request)

  def list_multi_part_upload_parts(self, request):
    return ListMultiPartUploadPartsResponse(self.net_client.get_response(request), request)

  def list_multi_part_uploads(self, request):
    return ListMultiPartUploadsResponse(self.net_client.get_response(request), request)

  def put_bucket_acl_for_group_spectra_s3(self, request):
    return PutBucketAclForGroupSpectraS3Response(self.net_client.get_response(request), request)

  def put_bucket_acl_for_user_spectra_s3(self, request):
    return PutBucketAclForUserSpectraS3Response(self.net_client.get_response(request), request)

  def put_data_policy_acl_for_group_spectra_s3(self, request):
    return PutDataPolicyAclForGroupSpectraS3Response(self.net_client.get_response(request), request)

  def put_data_policy_acl_for_user_spectra_s3(self, request):
    return PutDataPolicyAclForUserSpectraS3Response(self.net_client.get_response(request), request)

  def put_global_bucket_acl_for_group_spectra_s3(self, request):
    return PutGlobalBucketAclForGroupSpectraS3Response(self.net_client.get_response(request), request)

  def put_global_bucket_acl_for_user_spectra_s3(self, request):
    return PutGlobalBucketAclForUserSpectraS3Response(self.net_client.get_response(request), request)

  def put_global_data_policy_acl_for_group_spectra_s3(self, request):
    return PutGlobalDataPolicyAclForGroupSpectraS3Response(self.net_client.get_response(request), request)

  def put_global_data_policy_acl_for_user_spectra_s3(self, request):
    return PutGlobalDataPolicyAclForUserSpectraS3Response(self.net_client.get_response(request), request)

  def delete_bucket_acl_spectra_s3(self, request):
    return DeleteBucketAclSpectraS3Response(self.net_client.get_response(request), request)

  def delete_data_policy_acl_spectra_s3(self, request):
    return DeleteDataPolicyAclSpectraS3Response(self.net_client.get_response(request), request)

  def get_bucket_acl_spectra_s3(self, request):
    return GetBucketAclSpectraS3Response(self.net_client.get_response(request), request)

  def get_bucket_acls_spectra_s3(self, request):
    return GetBucketAclsSpectraS3Response(self.net_client.get_response(request), request)

  def get_data_policy_acl_spectra_s3(self, request):
    return GetDataPolicyAclSpectraS3Response(self.net_client.get_response(request), request)

  def get_data_policy_acls_spectra_s3(self, request):
    return GetDataPolicyAclsSpectraS3Response(self.net_client.get_response(request), request)

  def put_bucket_spectra_s3(self, request):
    return PutBucketSpectraS3Response(self.net_client.get_response(request), request)

  def delete_bucket_spectra_s3(self, request):
    return DeleteBucketSpectraS3Response(self.net_client.get_response(request), request)

  def get_bucket_spectra_s3(self, request):
    return GetBucketSpectraS3Response(self.net_client.get_response(request), request)

  def get_buckets_spectra_s3(self, request):
    return GetBucketsSpectraS3Response(self.net_client.get_response(request), request)

  def modify_bucket_spectra_s3(self, request):
    return ModifyBucketSpectraS3Response(self.net_client.get_response(request), request)

  def force_full_cache_reclaim_spectra_s3(self, request):
    return ForceFullCacheReclaimSpectraS3Response(self.net_client.get_response(request), request)

  def get_cache_filesystem_spectra_s3(self, request):
    return GetCacheFilesystemSpectraS3Response(self.net_client.get_response(request), request)

  def get_cache_filesystems_spectra_s3(self, request):
    return GetCacheFilesystemsSpectraS3Response(self.net_client.get_response(request), request)

  def get_cache_state_spectra_s3(self, request):
    return GetCacheStateSpectraS3Response(self.net_client.get_response(request), request)

  def modify_cache_filesystem_spectra_s3(self, request):
    return ModifyCacheFilesystemSpectraS3Response(self.net_client.get_response(request), request)

  def get_bucket_capacity_summary_spectra_s3(self, request):
    return GetBucketCapacitySummarySpectraS3Response(self.net_client.get_response(request), request)

  def get_storage_domain_capacity_summary_spectra_s3(self, request):
    return GetStorageDomainCapacitySummarySpectraS3Response(self.net_client.get_response(request), request)

  def get_system_capacity_summary_spectra_s3(self, request):
    return GetSystemCapacitySummarySpectraS3Response(self.net_client.get_response(request), request)

  def get_data_path_backend_spectra_s3(self, request):
    return GetDataPathBackendSpectraS3Response(self.net_client.get_response(request), request)

  def get_data_planner_blob_store_tasks_spectra_s3(self, request):
    return GetDataPlannerBlobStoreTasksSpectraS3Response(self.net_client.get_response(request), request)

  def modify_data_path_backend_spectra_s3(self, request):
    return ModifyDataPathBackendSpectraS3Response(self.net_client.get_response(request), request)

  def put_data_persistence_rule_spectra_s3(self, request):
    return PutDataPersistenceRuleSpectraS3Response(self.net_client.get_response(request), request)

  def put_data_policy_spectra_s3(self, request):
    return PutDataPolicySpectraS3Response(self.net_client.get_response(request), request)

  def put_data_replication_rule_spectra_s3(self, request):
    return PutDataReplicationRuleSpectraS3Response(self.net_client.get_response(request), request)

  def delete_data_persistence_rule_spectra_s3(self, request):
    return DeleteDataPersistenceRuleSpectraS3Response(self.net_client.get_response(request), request)

  def delete_data_policy_spectra_s3(self, request):
    return DeleteDataPolicySpectraS3Response(self.net_client.get_response(request), request)

  def delete_data_replication_rule_spectra_s3(self, request):
    return DeleteDataReplicationRuleSpectraS3Response(self.net_client.get_response(request), request)

  def get_data_persistence_rule_spectra_s3(self, request):
    return GetDataPersistenceRuleSpectraS3Response(self.net_client.get_response(request), request)

  def get_data_persistence_rules_spectra_s3(self, request):
    return GetDataPersistenceRulesSpectraS3Response(self.net_client.get_response(request), request)

  def get_data_policies_spectra_s3(self, request):
    return GetDataPoliciesSpectraS3Response(self.net_client.get_response(request), request)

  def get_data_policy_spectra_s3(self, request):
    return GetDataPolicySpectraS3Response(self.net_client.get_response(request), request)

  def get_data_replication_rule_spectra_s3(self, request):
    return GetDataReplicationRuleSpectraS3Response(self.net_client.get_response(request), request)

  def get_data_replication_rules_spectra_s3(self, request):
    return GetDataReplicationRulesSpectraS3Response(self.net_client.get_response(request), request)

  def modify_data_persistence_rule_spectra_s3(self, request):
    return ModifyDataPersistenceRuleSpectraS3Response(self.net_client.get_response(request), request)

  def modify_data_policy_spectra_s3(self, request):
    return ModifyDataPolicySpectraS3Response(self.net_client.get_response(request), request)

  def modify_data_replication_rule_spectra_s3(self, request):
    return ModifyDataReplicationRuleSpectraS3Response(self.net_client.get_response(request), request)

  def clear_suspect_blob_pools_spectra_s3(self, request):
    return ClearSuspectBlobPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def clear_suspect_blob_tapes_spectra_s3(self, request):
    return ClearSuspectBlobTapesSpectraS3Response(self.net_client.get_response(request), request)

  def clear_suspect_blob_targets_spectra_s3(self, request):
    return ClearSuspectBlobTargetsSpectraS3Response(self.net_client.get_response(request), request)

  def get_degraded_blobs_spectra_s3(self, request):
    return GetDegradedBlobsSpectraS3Response(self.net_client.get_response(request), request)

  def get_degraded_buckets_spectra_s3(self, request):
    return GetDegradedBucketsSpectraS3Response(self.net_client.get_response(request), request)

  def get_degraded_data_persistence_rules_spectra_s3(self, request):
    return GetDegradedDataPersistenceRulesSpectraS3Response(self.net_client.get_response(request), request)

  def get_degraded_data_replication_rules_spectra_s3(self, request):
    return GetDegradedDataReplicationRulesSpectraS3Response(self.net_client.get_response(request), request)

  def get_suspect_blob_pools_spectra_s3(self, request):
    return GetSuspectBlobPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def get_suspect_blob_tapes_spectra_s3(self, request):
    return GetSuspectBlobTapesSpectraS3Response(self.net_client.get_response(request), request)

  def get_suspect_blob_targets_spectra_s3(self, request):
    return GetSuspectBlobTargetsSpectraS3Response(self.net_client.get_response(request), request)

  def get_suspect_buckets_spectra_s3(self, request):
    return GetSuspectBucketsSpectraS3Response(self.net_client.get_response(request), request)

  def get_suspect_objects_spectra_s3(self, request):
    return GetSuspectObjectsSpectraS3Response(self.net_client.get_response(request), request)

  def get_suspect_objects_with_full_details_spectra_s3(self, request):
    return GetSuspectObjectsWithFullDetailsSpectraS3Response(self.net_client.get_response(request), request)

  def mark_suspect_blob_pools_as_degraded_spectra_s3(self, request):
    return MarkSuspectBlobPoolsAsDegradedSpectraS3Response(self.net_client.get_response(request), request)

  def mark_suspect_blob_tapes_as_degraded_spectra_s3(self, request):
    return MarkSuspectBlobTapesAsDegradedSpectraS3Response(self.net_client.get_response(request), request)

  def mark_suspect_blob_targets_as_degraded_spectra_s3(self, request):
    return MarkSuspectBlobTargetsAsDegradedSpectraS3Response(self.net_client.get_response(request), request)

  def put_group_group_member_spectra_s3(self, request):
    return PutGroupGroupMemberSpectraS3Response(self.net_client.get_response(request), request)

  def put_group_spectra_s3(self, request):
    return PutGroupSpectraS3Response(self.net_client.get_response(request), request)

  def put_user_group_member_spectra_s3(self, request):
    return PutUserGroupMemberSpectraS3Response(self.net_client.get_response(request), request)

  def delete_group_member_spectra_s3(self, request):
    return DeleteGroupMemberSpectraS3Response(self.net_client.get_response(request), request)

  def delete_group_spectra_s3(self, request):
    return DeleteGroupSpectraS3Response(self.net_client.get_response(request), request)

  def get_group_member_spectra_s3(self, request):
    return GetGroupMemberSpectraS3Response(self.net_client.get_response(request), request)

  def get_group_members_spectra_s3(self, request):
    return GetGroupMembersSpectraS3Response(self.net_client.get_response(request), request)

  def get_group_spectra_s3(self, request):
    return GetGroupSpectraS3Response(self.net_client.get_response(request), request)

  def get_groups_spectra_s3(self, request):
    return GetGroupsSpectraS3Response(self.net_client.get_response(request), request)

  def modify_group_spectra_s3(self, request):
    return ModifyGroupSpectraS3Response(self.net_client.get_response(request), request)

  def verify_user_is_member_of_group_spectra_s3(self, request):
    return VerifyUserIsMemberOfGroupSpectraS3Response(self.net_client.get_response(request), request)

  def allocate_job_chunk_spectra_s3(self, request):
    return AllocateJobChunkSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_active_job_spectra_s3(self, request):
    return CancelActiveJobSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_all_active_jobs_spectra_s3(self, request):
    return CancelAllActiveJobsSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_all_jobs_spectra_s3(self, request):
    return CancelAllJobsSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_job_spectra_s3(self, request):
    return CancelJobSpectraS3Response(self.net_client.get_response(request), request)

  def clear_all_canceled_jobs_spectra_s3(self, request):
    return ClearAllCanceledJobsSpectraS3Response(self.net_client.get_response(request), request)

  def clear_all_completed_jobs_spectra_s3(self, request):
    return ClearAllCompletedJobsSpectraS3Response(self.net_client.get_response(request), request)

  def get_bulk_job_spectra_s3(self, request):
    return GetBulkJobSpectraS3Response(self.net_client.get_response(request), request)

  def put_bulk_job_spectra_s3(self, request):
    return PutBulkJobSpectraS3Response(self.net_client.get_response(request), request)

  def verify_bulk_job_spectra_s3(self, request):
    return VerifyBulkJobSpectraS3Response(self.net_client.get_response(request), request)

  def get_active_job_spectra_s3(self, request):
    return GetActiveJobSpectraS3Response(self.net_client.get_response(request), request)

  def get_active_jobs_spectra_s3(self, request):
    return GetActiveJobsSpectraS3Response(self.net_client.get_response(request), request)

  def get_canceled_job_spectra_s3(self, request):
    return GetCanceledJobSpectraS3Response(self.net_client.get_response(request), request)

  def get_canceled_jobs_spectra_s3(self, request):
    return GetCanceledJobsSpectraS3Response(self.net_client.get_response(request), request)

  def get_completed_job_spectra_s3(self, request):
    return GetCompletedJobSpectraS3Response(self.net_client.get_response(request), request)

  def get_completed_jobs_spectra_s3(self, request):
    return GetCompletedJobsSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_chunk_dao_spectra_s3(self, request):
    return GetJobChunkDaoSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_chunk_spectra_s3(self, request):
    return GetJobChunkSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_chunks_ready_for_client_processing_spectra_s3(self, request):
    return GetJobChunksReadyForClientProcessingSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_spectra_s3(self, request):
    return GetJobSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_to_replicate_spectra_s3(self, request):
    return GetJobToReplicateSpectraS3Response(self.net_client.get_response(request), request)

  def get_jobs_spectra_s3(self, request):
    return GetJobsSpectraS3Response(self.net_client.get_response(request), request)

  def modify_active_job_spectra_s3(self, request):
    return ModifyActiveJobSpectraS3Response(self.net_client.get_response(request), request)

  def modify_job_spectra_s3(self, request):
    return ModifyJobSpectraS3Response(self.net_client.get_response(request), request)

  def replicate_put_job_spectra_s3(self, request):
    return ReplicatePutJobSpectraS3Response(self.net_client.get_response(request), request)

  def truncate_active_job_spectra_s3(self, request):
    return TruncateActiveJobSpectraS3Response(self.net_client.get_response(request), request)

  def truncate_all_active_jobs_spectra_s3(self, request):
    return TruncateAllActiveJobsSpectraS3Response(self.net_client.get_response(request), request)

  def truncate_all_jobs_spectra_s3(self, request):
    return TruncateAllJobsSpectraS3Response(self.net_client.get_response(request), request)

  def truncate_job_spectra_s3(self, request):
    return TruncateJobSpectraS3Response(self.net_client.get_response(request), request)

  def verify_safe_to_create_put_job_spectra_s3(self, request):
    return VerifySafeToCreatePutJobSpectraS3Response(self.net_client.get_response(request), request)

  def get_node_spectra_s3(self, request):
    return GetNodeSpectraS3Response(self.net_client.get_response(request), request)

  def get_nodes_spectra_s3(self, request):
    return GetNodesSpectraS3Response(self.net_client.get_response(request), request)

  def modify_node_spectra_s3(self, request):
    return ModifyNodeSpectraS3Response(self.net_client.get_response(request), request)

  def put_ds3_target_failure_notification_registration_spectra_s3(self, request):
    return PutDs3TargetFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_job_completed_notification_registration_spectra_s3(self, request):
    return PutJobCompletedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_job_created_notification_registration_spectra_s3(self, request):
    return PutJobCreatedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_job_creation_failed_notification_registration_spectra_s3(self, request):
    return PutJobCreationFailedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_object_cached_notification_registration_spectra_s3(self, request):
    return PutObjectCachedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_object_lost_notification_registration_spectra_s3(self, request):
    return PutObjectLostNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_object_persisted_notification_registration_spectra_s3(self, request):
    return PutObjectPersistedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_pool_failure_notification_registration_spectra_s3(self, request):
    return PutPoolFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_storage_domain_failure_notification_registration_spectra_s3(self, request):
    return PutStorageDomainFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_system_failure_notification_registration_spectra_s3(self, request):
    return PutSystemFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_tape_failure_notification_registration_spectra_s3(self, request):
    return PutTapeFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def put_tape_partition_failure_notification_registration_spectra_s3(self, request):
    return PutTapePartitionFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_ds3_target_failure_notification_registration_spectra_s3(self, request):
    return DeleteDs3TargetFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_job_completed_notification_registration_spectra_s3(self, request):
    return DeleteJobCompletedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_job_created_notification_registration_spectra_s3(self, request):
    return DeleteJobCreatedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_job_creation_failed_notification_registration_spectra_s3(self, request):
    return DeleteJobCreationFailedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_object_cached_notification_registration_spectra_s3(self, request):
    return DeleteObjectCachedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_object_lost_notification_registration_spectra_s3(self, request):
    return DeleteObjectLostNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_object_persisted_notification_registration_spectra_s3(self, request):
    return DeleteObjectPersistedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_pool_failure_notification_registration_spectra_s3(self, request):
    return DeletePoolFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_storage_domain_failure_notification_registration_spectra_s3(self, request):
    return DeleteStorageDomainFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_system_failure_notification_registration_spectra_s3(self, request):
    return DeleteSystemFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_tape_failure_notification_registration_spectra_s3(self, request):
    return DeleteTapeFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def delete_tape_partition_failure_notification_registration_spectra_s3(self, request):
    return DeleteTapePartitionFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_ds3_target_failure_notification_registration_spectra_s3(self, request):
    return GetDs3TargetFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_ds3_target_failure_notification_registrations_spectra_s3(self, request):
    return GetDs3TargetFailureNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_completed_notification_registration_spectra_s3(self, request):
    return GetJobCompletedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_completed_notification_registrations_spectra_s3(self, request):
    return GetJobCompletedNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_created_notification_registration_spectra_s3(self, request):
    return GetJobCreatedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_created_notification_registrations_spectra_s3(self, request):
    return GetJobCreatedNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_creation_failed_notification_registration_spectra_s3(self, request):
    return GetJobCreationFailedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_job_creation_failed_notification_registrations_spectra_s3(self, request):
    return GetJobCreationFailedNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_object_cached_notification_registration_spectra_s3(self, request):
    return GetObjectCachedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_object_cached_notification_registrations_spectra_s3(self, request):
    return GetObjectCachedNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_object_lost_notification_registration_spectra_s3(self, request):
    return GetObjectLostNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_object_lost_notification_registrations_spectra_s3(self, request):
    return GetObjectLostNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_object_persisted_notification_registration_spectra_s3(self, request):
    return GetObjectPersistedNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_object_persisted_notification_registrations_spectra_s3(self, request):
    return GetObjectPersistedNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_pool_failure_notification_registration_spectra_s3(self, request):
    return GetPoolFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_pool_failure_notification_registrations_spectra_s3(self, request):
    return GetPoolFailureNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_storage_domain_failure_notification_registration_spectra_s3(self, request):
    return GetStorageDomainFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_storage_domain_failure_notification_registrations_spectra_s3(self, request):
    return GetStorageDomainFailureNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_system_failure_notification_registration_spectra_s3(self, request):
    return GetSystemFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_system_failure_notification_registrations_spectra_s3(self, request):
    return GetSystemFailureNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_failure_notification_registration_spectra_s3(self, request):
    return GetTapeFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_failure_notification_registrations_spectra_s3(self, request):
    return GetTapeFailureNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_partition_failure_notification_registration_spectra_s3(self, request):
    return GetTapePartitionFailureNotificationRegistrationSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_partition_failure_notification_registrations_spectra_s3(self, request):
    return GetTapePartitionFailureNotificationRegistrationsSpectraS3Response(self.net_client.get_response(request), request)

  def delete_folder_recursively_spectra_s3(self, request):
    return DeleteFolderRecursivelySpectraS3Response(self.net_client.get_response(request), request)

  def get_blob_persistence_spectra_s3(self, request):
    return GetBlobPersistenceSpectraS3Response(self.net_client.get_response(request), request)

  def get_object_details_spectra_s3(self, request):
    return GetObjectDetailsSpectraS3Response(self.net_client.get_response(request), request)

  def get_objects_details_spectra_s3(self, request):
    return GetObjectsDetailsSpectraS3Response(self.net_client.get_response(request), request)

  def get_objects_with_full_details_spectra_s3(self, request):
    return GetObjectsWithFullDetailsSpectraS3Response(self.net_client.get_response(request), request)

  def get_physical_placement_for_objects_spectra_s3(self, request):
    return GetPhysicalPlacementForObjectsSpectraS3Response(self.net_client.get_response(request), request)

  def get_physical_placement_for_objects_with_full_details_spectra_s3(self, request):
    return GetPhysicalPlacementForObjectsWithFullDetailsSpectraS3Response(self.net_client.get_response(request), request)

  def verify_physical_placement_for_objects_spectra_s3(self, request):
    return VerifyPhysicalPlacementForObjectsSpectraS3Response(self.net_client.get_response(request), request)

  def verify_physical_placement_for_objects_with_full_details_spectra_s3(self, request):
    return VerifyPhysicalPlacementForObjectsWithFullDetailsSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_import_on_all_pools_spectra_s3(self, request):
    return CancelImportOnAllPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_import_pool_spectra_s3(self, request):
    return CancelImportPoolSpectraS3Response(self.net_client.get_response(request), request)

  def compact_all_pools_spectra_s3(self, request):
    return CompactAllPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def compact_pool_spectra_s3(self, request):
    return CompactPoolSpectraS3Response(self.net_client.get_response(request), request)

  def put_pool_partition_spectra_s3(self, request):
    return PutPoolPartitionSpectraS3Response(self.net_client.get_response(request), request)

  def deallocate_pool_spectra_s3(self, request):
    return DeallocatePoolSpectraS3Response(self.net_client.get_response(request), request)

  def delete_permanently_lost_pool_spectra_s3(self, request):
    return DeletePermanentlyLostPoolSpectraS3Response(self.net_client.get_response(request), request)

  def delete_pool_failure_spectra_s3(self, request):
    return DeletePoolFailureSpectraS3Response(self.net_client.get_response(request), request)

  def delete_pool_partition_spectra_s3(self, request):
    return DeletePoolPartitionSpectraS3Response(self.net_client.get_response(request), request)

  def force_pool_environment_refresh_spectra_s3(self, request):
    return ForcePoolEnvironmentRefreshSpectraS3Response(self.net_client.get_response(request), request)

  def format_all_foreign_pools_spectra_s3(self, request):
    return FormatAllForeignPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def format_foreign_pool_spectra_s3(self, request):
    return FormatForeignPoolSpectraS3Response(self.net_client.get_response(request), request)

  def get_blobs_on_pool_spectra_s3(self, request):
    return GetBlobsOnPoolSpectraS3Response(self.net_client.get_response(request), request)

  def get_pool_failures_spectra_s3(self, request):
    return GetPoolFailuresSpectraS3Response(self.net_client.get_response(request), request)

  def get_pool_partition_spectra_s3(self, request):
    return GetPoolPartitionSpectraS3Response(self.net_client.get_response(request), request)

  def get_pool_partitions_spectra_s3(self, request):
    return GetPoolPartitionsSpectraS3Response(self.net_client.get_response(request), request)

  def get_pool_spectra_s3(self, request):
    return GetPoolSpectraS3Response(self.net_client.get_response(request), request)

  def get_pools_spectra_s3(self, request):
    return GetPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def import_all_pools_spectra_s3(self, request):
    return ImportAllPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def import_pool_spectra_s3(self, request):
    return ImportPoolSpectraS3Response(self.net_client.get_response(request), request)

  def modify_all_pools_spectra_s3(self, request):
    return ModifyAllPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def modify_pool_partition_spectra_s3(self, request):
    return ModifyPoolPartitionSpectraS3Response(self.net_client.get_response(request), request)

  def modify_pool_spectra_s3(self, request):
    return ModifyPoolSpectraS3Response(self.net_client.get_response(request), request)

  def verify_all_pools_spectra_s3(self, request):
    return VerifyAllPoolsSpectraS3Response(self.net_client.get_response(request), request)

  def verify_pool_spectra_s3(self, request):
    return VerifyPoolSpectraS3Response(self.net_client.get_response(request), request)

  def convert_storage_domain_to_ds3_target_spectra_s3(self, request):
    return ConvertStorageDomainToDs3TargetSpectraS3Response(self.net_client.get_response(request), request)

  def put_pool_storage_domain_member_spectra_s3(self, request):
    return PutPoolStorageDomainMemberSpectraS3Response(self.net_client.get_response(request), request)

  def put_storage_domain_spectra_s3(self, request):
    return PutStorageDomainSpectraS3Response(self.net_client.get_response(request), request)

  def put_tape_storage_domain_member_spectra_s3(self, request):
    return PutTapeStorageDomainMemberSpectraS3Response(self.net_client.get_response(request), request)

  def delete_storage_domain_failure_spectra_s3(self, request):
    return DeleteStorageDomainFailureSpectraS3Response(self.net_client.get_response(request), request)

  def delete_storage_domain_member_spectra_s3(self, request):
    return DeleteStorageDomainMemberSpectraS3Response(self.net_client.get_response(request), request)

  def delete_storage_domain_spectra_s3(self, request):
    return DeleteStorageDomainSpectraS3Response(self.net_client.get_response(request), request)

  def get_storage_domain_failures_spectra_s3(self, request):
    return GetStorageDomainFailuresSpectraS3Response(self.net_client.get_response(request), request)

  def get_storage_domain_member_spectra_s3(self, request):
    return GetStorageDomainMemberSpectraS3Response(self.net_client.get_response(request), request)

  def get_storage_domain_members_spectra_s3(self, request):
    return GetStorageDomainMembersSpectraS3Response(self.net_client.get_response(request), request)

  def get_storage_domain_spectra_s3(self, request):
    return GetStorageDomainSpectraS3Response(self.net_client.get_response(request), request)

  def get_storage_domains_spectra_s3(self, request):
    return GetStorageDomainsSpectraS3Response(self.net_client.get_response(request), request)

  def modify_storage_domain_member_spectra_s3(self, request):
    return ModifyStorageDomainMemberSpectraS3Response(self.net_client.get_response(request), request)

  def modify_storage_domain_spectra_s3(self, request):
    return ModifyStorageDomainSpectraS3Response(self.net_client.get_response(request), request)

  def get_system_failures_spectra_s3(self, request):
    return GetSystemFailuresSpectraS3Response(self.net_client.get_response(request), request)

  def get_system_information_spectra_s3(self, request):
    return GetSystemInformationSpectraS3Response(self.net_client.get_response(request), request)

  def reset_instance_identifier_spectra_s3(self, request):
    return ResetInstanceIdentifierSpectraS3Response(self.net_client.get_response(request), request)

  def verify_system_health_spectra_s3(self, request):
    return VerifySystemHealthSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_eject_on_all_tapes_spectra_s3(self, request):
    return CancelEjectOnAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_eject_tape_spectra_s3(self, request):
    return CancelEjectTapeSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_format_on_all_tapes_spectra_s3(self, request):
    return CancelFormatOnAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_format_tape_spectra_s3(self, request):
    return CancelFormatTapeSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_import_on_all_tapes_spectra_s3(self, request):
    return CancelImportOnAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_import_tape_spectra_s3(self, request):
    return CancelImportTapeSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_online_on_all_tapes_spectra_s3(self, request):
    return CancelOnlineOnAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_online_tape_spectra_s3(self, request):
    return CancelOnlineTapeSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_verify_on_all_tapes_spectra_s3(self, request):
    return CancelVerifyOnAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def cancel_verify_tape_spectra_s3(self, request):
    return CancelVerifyTapeSpectraS3Response(self.net_client.get_response(request), request)

  def clean_tape_drive_spectra_s3(self, request):
    return CleanTapeDriveSpectraS3Response(self.net_client.get_response(request), request)

  def put_tape_density_directive_spectra_s3(self, request):
    return PutTapeDensityDirectiveSpectraS3Response(self.net_client.get_response(request), request)

  def delete_permanently_lost_tape_spectra_s3(self, request):
    return DeletePermanentlyLostTapeSpectraS3Response(self.net_client.get_response(request), request)

  def delete_tape_density_directive_spectra_s3(self, request):
    return DeleteTapeDensityDirectiveSpectraS3Response(self.net_client.get_response(request), request)

  def delete_tape_drive_spectra_s3(self, request):
    return DeleteTapeDriveSpectraS3Response(self.net_client.get_response(request), request)

  def delete_tape_failure_spectra_s3(self, request):
    return DeleteTapeFailureSpectraS3Response(self.net_client.get_response(request), request)

  def delete_tape_partition_failure_spectra_s3(self, request):
    return DeleteTapePartitionFailureSpectraS3Response(self.net_client.get_response(request), request)

  def delete_tape_partition_spectra_s3(self, request):
    return DeleteTapePartitionSpectraS3Response(self.net_client.get_response(request), request)

  def eject_all_tapes_spectra_s3(self, request):
    return EjectAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def eject_storage_domain_blobs_spectra_s3(self, request):
    return EjectStorageDomainBlobsSpectraS3Response(self.net_client.get_response(request), request)

  def eject_storage_domain_spectra_s3(self, request):
    return EjectStorageDomainSpectraS3Response(self.net_client.get_response(request), request)

  def eject_tape_spectra_s3(self, request):
    return EjectTapeSpectraS3Response(self.net_client.get_response(request), request)

  def force_tape_environment_refresh_spectra_s3(self, request):
    return ForceTapeEnvironmentRefreshSpectraS3Response(self.net_client.get_response(request), request)

  def format_all_tapes_spectra_s3(self, request):
    return FormatAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def format_tape_spectra_s3(self, request):
    return FormatTapeSpectraS3Response(self.net_client.get_response(request), request)

  def get_blobs_on_tape_spectra_s3(self, request):
    return GetBlobsOnTapeSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_density_directive_spectra_s3(self, request):
    return GetTapeDensityDirectiveSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_density_directives_spectra_s3(self, request):
    return GetTapeDensityDirectivesSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_drive_spectra_s3(self, request):
    return GetTapeDriveSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_drives_spectra_s3(self, request):
    return GetTapeDrivesSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_failures_spectra_s3(self, request):
    return GetTapeFailuresSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_libraries_spectra_s3(self, request):
    return GetTapeLibrariesSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_library_spectra_s3(self, request):
    return GetTapeLibrarySpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_partition_failures_spectra_s3(self, request):
    return GetTapePartitionFailuresSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_partition_spectra_s3(self, request):
    return GetTapePartitionSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_partition_with_full_details_spectra_s3(self, request):
    return GetTapePartitionWithFullDetailsSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_partitions_spectra_s3(self, request):
    return GetTapePartitionsSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_partitions_with_full_details_spectra_s3(self, request):
    return GetTapePartitionsWithFullDetailsSpectraS3Response(self.net_client.get_response(request), request)

  def get_tape_spectra_s3(self, request):
    return GetTapeSpectraS3Response(self.net_client.get_response(request), request)

  def get_tapes_spectra_s3(self, request):
    return GetTapesSpectraS3Response(self.net_client.get_response(request), request)

  def import_all_tapes_spectra_s3(self, request):
    return ImportAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def import_tape_spectra_s3(self, request):
    return ImportTapeSpectraS3Response(self.net_client.get_response(request), request)

  def inspect_all_tapes_spectra_s3(self, request):
    return InspectAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def inspect_tape_spectra_s3(self, request):
    return InspectTapeSpectraS3Response(self.net_client.get_response(request), request)

  def modify_all_tape_partitions_spectra_s3(self, request):
    return ModifyAllTapePartitionsSpectraS3Response(self.net_client.get_response(request), request)

  def modify_tape_partition_spectra_s3(self, request):
    return ModifyTapePartitionSpectraS3Response(self.net_client.get_response(request), request)

  def modify_tape_spectra_s3(self, request):
    return ModifyTapeSpectraS3Response(self.net_client.get_response(request), request)

  def online_all_tapes_spectra_s3(self, request):
    return OnlineAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def online_tape_spectra_s3(self, request):
    return OnlineTapeSpectraS3Response(self.net_client.get_response(request), request)

  def verify_all_tapes_spectra_s3(self, request):
    return VerifyAllTapesSpectraS3Response(self.net_client.get_response(request), request)

  def verify_tape_spectra_s3(self, request):
    return VerifyTapeSpectraS3Response(self.net_client.get_response(request), request)

  def put_ds3_target_read_preference_spectra_s3(self, request):
    return PutDs3TargetReadPreferenceSpectraS3Response(self.net_client.get_response(request), request)

  def delete_ds3_target_failure_spectra_s3(self, request):
    return DeleteDs3TargetFailureSpectraS3Response(self.net_client.get_response(request), request)

  def delete_ds3_target_read_preference_spectra_s3(self, request):
    return DeleteDs3TargetReadPreferenceSpectraS3Response(self.net_client.get_response(request), request)

  def delete_ds3_target_spectra_s3(self, request):
    return DeleteDs3TargetSpectraS3Response(self.net_client.get_response(request), request)

  def force_target_environment_refresh_spectra_s3(self, request):
    return ForceTargetEnvironmentRefreshSpectraS3Response(self.net_client.get_response(request), request)

  def get_ds3_target_data_policies_spectra_s3(self, request):
    return GetDs3TargetDataPoliciesSpectraS3Response(self.net_client.get_response(request), request)

  def get_ds3_target_failures_spectra_s3(self, request):
    return GetDs3TargetFailuresSpectraS3Response(self.net_client.get_response(request), request)

  def get_ds3_target_read_preference_spectra_s3(self, request):
    return GetDs3TargetReadPreferenceSpectraS3Response(self.net_client.get_response(request), request)

  def get_ds3_target_read_preferences_spectra_s3(self, request):
    return GetDs3TargetReadPreferencesSpectraS3Response(self.net_client.get_response(request), request)

  def get_ds3_target_spectra_s3(self, request):
    return GetDs3TargetSpectraS3Response(self.net_client.get_response(request), request)

  def get_ds3_targets_spectra_s3(self, request):
    return GetDs3TargetsSpectraS3Response(self.net_client.get_response(request), request)

  def modify_all_ds3_targets_spectra_s3(self, request):
    return ModifyAllDs3TargetsSpectraS3Response(self.net_client.get_response(request), request)

  def modify_ds3_target_spectra_s3(self, request):
    return ModifyDs3TargetSpectraS3Response(self.net_client.get_response(request), request)

  def pair_back_registered_ds3_target_spectra_s3(self, request):
    return PairBackRegisteredDs3TargetSpectraS3Response(self.net_client.get_response(request), request)

  def register_ds3_target_spectra_s3(self, request):
    return RegisterDs3TargetSpectraS3Response(self.net_client.get_response(request), request)

  def verify_ds3_target_spectra_s3(self, request):
    return VerifyDs3TargetSpectraS3Response(self.net_client.get_response(request), request)

  def delegate_create_user_spectra_s3(self, request):
    return DelegateCreateUserSpectraS3Response(self.net_client.get_response(request), request)

  def delegate_delete_user_spectra_s3(self, request):
    return DelegateDeleteUserSpectraS3Response(self.net_client.get_response(request), request)

  def get_user_spectra_s3(self, request):
    return GetUserSpectraS3Response(self.net_client.get_response(request), request)

  def get_users_spectra_s3(self, request):
    return GetUsersSpectraS3Response(self.net_client.get_response(request), request)

  def modify_user_spectra_s3(self, request):
    return ModifyUserSpectraS3Response(self.net_client.get_response(request), request)

  def regenerate_user_secret_key_spectra_s3(self, request):
    return RegenerateUserSecretKeySpectraS3Response(self.net_client.get_response(request), request)

