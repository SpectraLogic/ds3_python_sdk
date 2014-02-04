# DS3 Python SDK

---

A SDK conforming to the DS3 specification.

## Installing

To install the SDK un-tar `ds3_python_sdk.tar`, cd into `ds3_python_sdk`, and execute `sudo python setup.py install`

You will now have the cli available from your path.  The name of the cli client is `ds3_cli` (See CLI bellow).  In addition to the CLI a ds3 python package is installed into the local python installation and is available for import (See SDK bellow).

## SDK

---

The SDK provides an interface for a user to add DS3 functionality to their existing or new python code.  In order to take advantage of the SDK you need to import the ds3 python package and module.  The following is an example that connects to a remote ds3 server and lists all the buckets that have been added.

```python

from ds3 import ds3 #1

ds3_connection = ds3.Client("hostname:8080", ds3.Credentials("access_id", "key")) #2

ds3.pretty_print_xml(ds3_connection.service_list()) #3

```

The above script imports the ds3 python sdk (line 1), creates a connection to the remote ds3 server (line 2), and then asks the remote ds3 server for a service list (lists all the buckets on the remote system) and formats the xml output so that its easier to read.

This is an example that you might see when running the above script:

```xml

<?xml version="1.0" ?>
<ListAllMyBucketsResult xmlns="http://doc.s3.amazonaws.com/2006-03-01">
	<Owner>
		<ID>user_name</ID>
		<DisplayName>user_name</DisplayName>
	</Owner>
	<Buckets>
		<Bucket>
			<Name>testBucket1</Name>
			<CreationDate>2014-01-27T11:35:36</CreationDate>
		</Bucket>
		<Bucket>
			<Name>testbucket2</Name>
			<CreationDate>2014-01-27T11:35:36</CreationDate>
		</Bucket>
	</Buckets>
</ListAllMyBucketsResult>

```

### DS3 Client Methods

Here is a full list of all the commands that the `ds3.Client` class supports:

* `service_list()`: Returns a list of all the buckets that have been added to the system
* `bucket_list(bucket_name)`: Returns a list of all the objects contained in `bucket_name`
* `create_bucket(bucket_name)`: Creates a bucket with the name `bucket_name`
* `delete_bucket(bucket_name)`: Deletes the bucket `bucket_name`. **Note:** All the objects in the bucket must be deleted first before the `delete_bucket` can be executed. 
* `get_object(bucket_name, object_name)`: Retrieves `object_name` from bucket `bucket_name`
* `put_object(bucket_name, object_name, object_data)`: Puts a new object `object_name` into bucket `bucket_name`.  `object_data` can be a string, or a file handle.
* `delete_object(bucket_name, object_name)`: Deletes `object_name` from bucket `bucket_name`
* `bulk_put(bucket_name, object_list)`: Primes DS3 for a bulk put into bucket `bucket_name`.  `object_list` is a list of `ds3.ObjectData(name,size)` objects where `name` is the name of the object being uploaded, and `size` is the total size of that file in bytes.  Both `name` and `size` are required for `bulk_put` 
* `bulk_get(bucket_name, object_list)`: Primes DS3 of a bulk get from bucket `bucket_name`.  `object_list` is a list of `ds3.ObjectData(name)` objects where `name` is the name of the object being requested

## CLI

---

In addition to providing a programming interface to DS3 this SDK also provides a CLI which exposes the DS3 interface from the command line.  This allows you to interrogate the remote DS3 endpoint from the CLI with minimal effort.

### Usage

```
ds3_cli -h
usage: ds3_cli [-h] --operation
               {service_list,bucket_list,get_object,put_object,create_bucket,delete_bucket,delete_object}
               [--bucket BUCKET] [--file TARGET_FILE] [--endpoint ENDPOINT]
               [--accessId ACCESS_ID] [--key KEY]

DS3 Command Line Interface

optional arguments:
  -h, --help            show this help message and exit
  --operation {service_list,bucket_list,get_object,put_object,create_bucket,delete_bucket,delete_object}
                        What operation to perform
  --bucket BUCKET       What bucket to target. Required for any operations
                        that target a bucket
  --file TARGET_FILE    The file to either get or put. Required for any file
                        specific operations
  --endpoint ENDPOINT   The DS3 endpoint. Optionally you can set the
                        environment variable "DS3_ENDPOINT"
  --accessId ACCESS_ID  The DS3 access id. Optionally you can set the
                        environment variable "DS3_ACCESS_KEY"
  --key KEY             The DS3 secret key. Optionally you can set the
                        environment variable "DS3_SECRET_KEY"

```

The `endpoint`, `accessId`, and `key` can all be specified with environment variables as well as from the CLI.

### Example CLI Usage

List all buckets (also called service list):

`ds3_cli --operation service_list`

Output:

```xml
<?xml version="1.0" ?>
<ListAllMyBucketsResult xmlns="http://doc.s3.amazonaws.com/2006-03-01">
	<Owner>
		<ID>user_name</ID>
		<DisplayName>user_name</DisplayName>
	</Owner>
	<Buckets>
		<Bucket>
			<Name>testBucket1</Name>
			<CreationDate>2014-01-27T11:35:36</CreationDate>
		</Bucket>
		<Bucket>
			<Name>testbucket2</Name>
			<CreationDate>2014-01-27T11:35:36</CreationDate>
		</Bucket>
	</Buckets>
</ListAllMyBucketsResult>

```

List all objects in a bucket (also called bucket list):

`ds3_cli --operation bucket_list --bucket testBucket`

Output:

```xml
<?xml version="1.0" ?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
	<Name>testBucket</Name>
	<Prefix/>
	<Marker/>
	<MaxKeys>1000</MaxKeys>
	<IsTruncated>false</IsTruncated>
	<Contents>
		<Key>testObject1</Key>
		<LastModified>2014-01-27T11:44:50.000Z</LastModified>
		<ETag>NOTRETURNED</ETag>
		<Size>256</Size>
		<StorageClass>STANDARD</StorageClass>
		<Owner>
			<ID>user_name</ID>
			<DisplayName>user_name</DisplayName>
		</Owner>
	</Contents>
	<Contents>
		<Key>testObject2</Key>
		<LastModified>2014-01-27T11:44:50.000Z</LastModified>
		<ETag>NOTRETURNED</ETag>
		<Size>1024</Size>
		<StorageClass>STANDARD</StorageClass>
		<Owner>
			<ID>user_name</ID>
			<DisplayName>user_name</DisplayName>
		</Owner>
	</Contents>
</ListBucketResult>

```

### Example RC File

```bash

export DS3_ACCESS_KEY="access_key"
export DS3_SECRET_KEY="secret_key"
export DS3_ENDPOINT="hostname:8080"

```

To use the rc file use `source my_rc_file.rc` which will export all of the environment variables into the current bash shell and will be picked up by the CLI.

## Proxy Support

The CLI client supports connecting to DS3 via a HTTP Proxy.  To automatically connect to the proxy from the cli set `http_proxy` as an environment variable and the `ds3_cli` will pick up the configuration.  The proxy setting it not required to be set, but if you work in an environment where a proxy is present and the `http_proxy` environment variable is already set, you should not have to do anything.
