Spectra S3 Python SDK
--------------

[![Apache V2 License](http://img.shields.io/badge/license-Apache%20V2-blue.svg)](https://github.com/SpectraLogic/ds3_python_sdk/blob/master/LICENSE.md)

An SDK conforming to the Spectra S3 [specification](https://developer.spectralogic.com/doc/ds3api/1.2/wwhelp/wwhimpl/js/html/wwhelp.htm) for Python 2.7

Contact Us
----------

Join us at our [Google Groups](https://groups.google.com/d/forum/spectralogicds3-sdks) forum to ask questions, or see frequently asked questions.

Installing
----------

To install the ds3_python_sdk, either clone the latest code, or download a release bundle from [Releases](http://github.com/SpectraLogic/ds3_python_sdk/releases).  Once the code has been download, cd into the bundle, and install it with `sudo python setup.py install`

Once `setup.py` completes the ds3_python_sdk should be installed and available to be imported into python scripts.

Documentation
-------------
The documentation for the SDK can be found at [http://spectralogic.github.io/ds3_python_sdk/sphinx/v1.0-0/](http://spectralogic.github.io/ds3_python_sdk/sphinx/v1.0-0/)

SDK
---

The SDK provides an interface for a user to add Spectra S3 functionality to their existing or new python application.  In order to take advantage of the SDK you need to import the `ds3` python package and module.  The following is an example that creates a Spectra S3 client from environment variables, creates a bucket, and lists all the buckets that are visible to the user.

```python

from ds3 import ds3

client = ds3.createClientFromEnv()

client.put_bucket(ds3.PutBucketRequest("TestBucket"))

getServiceResponse = client.get_service(ds3.GetServiceRequest())

for bucket in getServiceResponse.result['BucketList']:
    print bucket['Name']
```

Ds3Client
---------
In the ds3_python_sdk there are two ways that you can create a `Ds3Client` instance: environment variables, or manually.  `ds3.createClientFromEnv` will create a `Ds3Client` using the following environment variables:

* `DS3_ENDPOINT` - The URL to the DS3 Endpoint
* `DS3_ACCESS_KEY` - The DS3 access key
* `DS3_SECRET_KEY` - The DS3 secret key
* `http_proxy` - If set, the `Ds3Client` instance will proxy through this URL

The `Ds3Client` instance can also be created manually in code with:

```python

from ds3 import ds3

client = ds3.Ds3Client("endpoint", ds3.Credentials("access_key", "secret_key"))

```

The proxy URL can be passed in as the named parameter `proxy` to `Ds3Client()`.

Putting Data
------------

To put data to a Spectra S3 appliance you have to do it inside of the context of what is called a Bulk Job.  Bulk Jobs allow the Spectra S3 appliance to plan how data should land to cache, and subsequently get written/read to/from tape.  The basic flow of every job is:

* Generate the list of objects that will either be sent to or retrieved from Spectra S3
* Send a bulk put/get to Spectra S3 to plan the job
* The job will be split into multiple chunks.  An application must then get the available list of chunks that can be processed
* For each chunk that can be processed, sent the object (this step can be done in parallel)
* Repeat getting the list of available chunks until all chunks have been processed

[An example of the above using the Python SDK for putting data] (samples/puttingData.py)

[An example of getting data with the Python SDK] (samples/gettingData.py)

[An example of using getService and getBucket to list all accessible buckets and objects] (samples/listAll.py)

[An example of how give objects on the server a different name than what is on the filesystem, and how to delete objects by folder] (samples/renaming.py)
