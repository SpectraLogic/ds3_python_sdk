Spectra S3 API Python_SDK r1.x to r3.x Migration Guide
==============================

The Python SDK no longer wraps the C SDK, which removes the previous dependency on the C SDK.

Python target: 2.7 (unchanged)

All command names have changed. Spectra S3 commands are namespaced from AWS commands with `spectra_s3` for client commands, and `SpectraS3` for request and response names. See Table 1 for the r3.x commands that corresponds to the r1.x commands.

Commands with full details parameters have been separated into two commands, one with the full details parameter and one without. See Table 2 for a complete list of commands with the full details parameter.

The Client has been changed to use Request and Response handlers. Each call to a client command takes in the associated request handler, and returns the associated response handler. This changes the way in which commands are called. See Examples 1-4 for a comparative look at the difference between r1.x and r3.x Client command calls.

Client commands now return Response objects, which contain the following content:
* `meta_data` - Response headers contained within a dictionary object
* `request` - The request object used to initiate the Client command
* `response` - The `httplib.HTTPResponse` object returned from the server
* `result` - The Http Response data contained within a dictionary object

EXAMPLE 1: Get Service Command
==============================
r1.x:
`client.getService()`

r3.x:
`client.get_service(GetServiceRequest())`

EXAMPLE 2: Get Bucket Command
==============================
r1.x:
`client.getBucket(bucketName)`

r3.x:
`client.get_bucket(GetBucketRequest(bucketName))`

EXAMPLE 3: Put Object Command
==============================
r1.x:
`client.putObject(bucketName, objectName, objectOffset, objectLength, jobId, realFileName=realFileName, metadata=metadata)`

r3.x:
`put_object(PutObjectRequest(bucketName, objectName, headers=metadata, job=jobId, offset=offset, real_file_name=realFileName, stream=dataSourceStream))`

EXAMPLE 4: Get Object Command
==============================
r1.x:
`client.getObject(bucketName, objectName, objectOffset, jobId, realFileName=realFileName)`

r3.x:
`client.get_object(GetObjectRequest(bucketName, objectName, job=jobId, offset=offset, real_file_name=realFileName, stream=destinationStream))`

TABLE 1: API Client Commands
==============================
| r1.x Command Name | r3.x AWS Command Name | r3.x Spectra S3 Command Name |
|---|---|---|
| verifySystemHealth | NA | verify_system_health_spectra_s3 |
| getService | get_service | NA |
| getBucket | get_bucket | get_bucket_spectra_s3 |
| headObject | head_object | NA |
| headBucket | head_bucket | NA |
| deleteFolder | NA | delete_folder_recursively_spectra_s3 |
| getSystemInformation | NA | get_system_information_spectra_s3 |
| getObject | get_object | get_object_spectra_s3 |
| putBucket | put_bucket | put_bucket_spectra_s3 |
| putObject | put_object | NA |
| deleteObject | delete_object | NA |
| deleteObjects | delete_objects | NA |
| deleteBucket | delete_bucket | delete_bucket_spectra_s3 |
| putBulk | NA | put_bulk_job_spectra_s3 |
| getBulk | NA | get_bulk_job_spectra_s3 |
| getObjects | NA | get_objects_spectra_s3 and get_objects_with_full_details_spectra_s3 |
| allocateChunk | NA | allocate_job_chunk_spectra_s3 |
| getAvailableChunks | NA | get_job_chunks_ready_for_client_processing_spectra_s3 |
| getJob | NA | get_job_spectra_s3 |
| getJobs | NA | get_jobs_spectra_s3 |
| putJob | | |
| deleteJob | | |
| getPhysicalPlacement | NA | get_physical_placement_for_objects_spectra_s3 and get_physical_placement_for_objects_with_full_details_spectra_s3 |

TABLE 2: Commands With Parameter: Full Details
==============================
| Basic Command | Command with Full Details |
|---|---|
| get_objects_spectra_s3 | get_objects_with_full_details_spectra_s3 |
| get_physical_placement_for_objects_spectra_s3 | get_physical_placement_for_objects_with_full_details_spectra_s3 |
| verify_physical_placement_for_objects_spectra_s3 | verify_physical_placement_for_objects_with_full_details_spectra_s3 |
| get_tape_partition_spectra_s3 | get_tape_partition_with_full_details_spectra_s3 |
| get_tape_partitions_spectra_s3 | get_tape_partitions_with_full_details_spectra_s3 |
| get_tape_spectra_s3 | get_tape_with_full_details_spectra_s3 |
| get_tapes_spectra_s3 | get_tapes_with_full_details_spectra_s3 |

