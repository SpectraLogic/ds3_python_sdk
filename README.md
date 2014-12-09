# DS3 Python SDK

---

A SDK conforming to the DS3 specification.

## Contact Us

Join us at our [Google Groups](https://groups.google.com/d/forum/spectralogicds3-sdks) forum to ask questions, or see frequently asked questions.

## Installing

To install the SDK un-tar `ds3_python_sdk.tar`, cd into `ds3_python_sdk`, and execute `sudo python setup.py install`

You will now have the cli available from your path.  The name of the cli client is `ds3_cli` (See CLI bellow).  In addition to the CLI a ds3 python package is installed into the local python installation and is available for import (See SDK bellow).

## SDK

---

The SDK provides an interface for a user to add DS3 functionality to their existing or new python code.  In order to take advantage of the SDK you need to import the ds3 python package and module.  The following is an example that connects to a remote ds3 server and lists all the buckets that have been added.

```python

from ds3 import ds3

client = ds3.Client("hostname:8080", ds3.Credentials("access_id", "key"))

for bucket in client.getService():
    print bucket.name
```
