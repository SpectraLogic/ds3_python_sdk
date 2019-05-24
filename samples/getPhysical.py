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

from ds3 import ds3

client = ds3.createClientFromEnv()

# this example assumes that a bucket named "books" and the following object exists on the server
# note: these are the same objects that are on the server if you run the bulk put example and comment out the delete lines
bucketName = "books"
fileList = ["beowulf.txt", "sherlock_holmes.txt", "tale_of_two_cities.txt", "ulysses.txt"]

objectList = list([ds3.Ds3GetObject(name=fileName) for fileName in fileList])
tapes = client.get_physical_placement_for_objects_spectra_s3(
               ds3.GetPhysicalPlacementForObjectsSpectraS3Request(bucketName, objectList))

for tape in tapes.result['TapeList']:
    print(tape)
