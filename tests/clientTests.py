import unittest
from ds3.ds3 import *

class BasicClientFunctionTestCase(unittest.TestCase):

    def setUp(self):
        self.client = createClientFromEnv()

    def test_create_bucket(self):
        def name(service):
            return service.name

        self.client.putBucket("python_test_bucket")

        bucketSet = frozenset(map(name, self.client.getService()))

        self.assertTrue("python_test_bucket" in bucketSet)

        self.client.deleteBucket("python_test_bucket")
