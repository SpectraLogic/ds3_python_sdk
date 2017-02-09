#   Copyright 2014-2017 Spectra Logic Corporation. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License"). You may not use
#   this file except in compliance with the License. A copy of the License is located at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   or in the "license" file accompanying this file.
#   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied. See the License for the
#   specific language governing permissions and limitations under the License.

import os
import tempfile

from ds3 import ds3

client = ds3.createClientFromEnv()

# create a dictionary to map bucket names to object names
object_dict={}

# get a list of all the buckets on the server we have access to
bucketObjects = client.get_service(ds3.GetServiceRequest())
# the call to getService will return a list bucket objects, which have more information about the bucket, but in this case we only care about the name of the buckets
bucketNames = map(lambda bucket: bucket['Name'], bucketObjects.result['BucketList'])

# iterate over every bucket and get details about each of them
for bucketName in bucketNames:
    object_dict[bucketName]=[]
    bucketContents = client.get_bucket(ds3.GetBucketRequest(bucketName))

    # like getService, getBucket returns more information about the bucket than the contents, so we'll extract those
    objectNames = map(lambda bucket: bucket['Key'], bucketContents.result['ContentsList'])
    for name in objectNames:
    	object_dict[bucketName].append(name)

print(object_dict)
