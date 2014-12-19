DS3 Python SDK
--------------

A SDK conforming to the DS3 specification.

Contact Us
----------

Join us at our [Google Groups](https://groups.google.com/d/forum/spectralogicds3-sdks) forum to ask questions, or see frequently asked questions.

Installing
----------

Follow the instructions for installing the [ds3_c_sdk](https://github.com/SpectraLogic/ds3_c_sdk) first.  The ds3_python_sdk uses the ds3_c_sdk to communicate with a DS3 endpoint, and will not function without it.

To install the ds3_python_sdk, either clone the latest code, or download a release bundle from [Releases](http://github.com/SpectraLogic/ds3_python_sdk/releases).  Once the code has been download, cd into the bundle, and install it with `sudo python setup.py install`

Once `setup.py` completes the ds3_python_sdk should be installed and available to be imported into python scripts.

SDK
---

The SDK provides an interface for a user to add DS3 functionality to their existing or new python code.  In order to take advantage of the SDK you need to import the `ds3` python package and module.  The following is an example that creates a ds3 client from environment variables, creates a bucket, and lists all the buckets that are visible to the user.

```python

from ds3 import ds3

client = ds3.createClientFromEnv()

client.putBucket("testBucket")

for bucket in client.getService():
        print bucket.name
```

Ds3Client
---------
In the ds3_python_sdk there are two ways that you can create a `Ds3Client` instance: environment variables, or manually.  `ds3.createClientFromEnv` will create a `Ds3Client` using the following environment variables:

* `DS3_ENDPOINT` - The url to the DS3 Endpoint
* `DS3_ACCESS_KEY` - The DS3 access key
* `DS3_SECRET_KEY` - The DS3 secret key
* `http_proxy` - If set, the `Ds3Client` instance will proxy through this url

The `Ds3Client` instance can also be created manually in code with:

```python

from ds3 import ds3

client = ds3.Ds3Client("endpoint", ds3.Credentials("access_key", "secret_key"))

```

The proxy url can be passed in as the named parameter `proxy` to `Ds3Client()`.
