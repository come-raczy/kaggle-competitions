import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import mock_open, patch

from leash_BELKA.TrainingData import TrainingData


class TestTrainingData(TestCase):
    def test_constructor(self):
        td = TrainingData([])
        self.assertEqual(td.targets, [])
        td = TrainingData(["AAA", "BBB"])
        self.assertEqual(td.targets, ["AAA", "BBB"])

    def test_add(self):
        td = TrainingData([])
        td.add("AAA", "bb1", "bb2", "bb3", "smiles", 0)
        self.assertEqual(td.targets, ["AAA"])
