# DS3 Python SDK
---

A SDK conforming to the DS3 specification.

## CLI
---

In additon to prodiving a programming interface to DS3 this SDK also provides a CLI which exposes the DS3 interface from the command line.  This allows you to interrogate the remote DS3 endpoint from the CLI with minimal effort.

### Usage

```
#python ./ds3.py -h
usage: ds3.py [-h] --operation
              {service_list,bucket_list,get_object,put_object,create_bucket}
              [--bucket BUCKET] [--file TARGET_FILE] [--endpoint ENDPOINT]
              [--accessId ACCESS_ID] [--key KEY]

DS3 Command Line Interface

optional arguments:
  -h, --help            show this help message and exit
  --operation {service_list,bucket_list,get_object,put_object,create_bucket}
                      What operation to perform
  --bucket BUCKET       What bucket to target. Required for any operations
                        that target a bucket
  --file TARGET_FILE    The file to either get or put. Required for any file
                        specfic operations
  --endpoint ENDPOINT   The DS3 endpoint. Optionally you can set the
                        enviornment variable "DS3_ENDPOINT"
  --accessId ACCESS_ID  The DS3 access id. Optionally you can set the
                        enviornment variable "DS3_ACCESS_KEY"
  --key KEY             The DS3 secret key. Optionally you can set the
                      environment variable "DS3_SECRET_KEY"

```

The `endpoint`, `accessId`, and `key` can all be specified with environment variables as well as from the CLI.

### Example Usage

List all buckets (also called service list):
```
#python ./ds3.py --operation service_list
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

List all objects in a bucket (also called bucket list)

```


```


### Example RC File

```bash

export DS3_ACCESS_KEY="access_key"
export DS3_SECRET_KEY="secret_key"
export DS3_ENDPOINT="hostname:8080"

```

To use the rc file use `source my_rc_file.rc` which will export all of the enviornment variables into the current bash shell and will be picked up by the CLI.
