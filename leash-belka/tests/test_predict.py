#import sys
#from io import StringIO
from unittest import TestCase

#from unittest.mock import mock_open, patch
from leash_BELKA.predict import predict


class TestPredict(TestCase):
    def test_predict(self):
        predict()
        self.assertEqual(3, 3)
