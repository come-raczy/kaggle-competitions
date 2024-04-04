import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import mock_open, patch

from leash_BELKA.train import train

files = [StringIO("file1"), StringIO("file2"), StringIO("file3")]

bad_data = """id,buildingblock1_smiles,buildingblock2_smiles,buildingblock3_smiles,molecule_smiles,protein_name,binds
1,CCO,CCO,CCO,CCO,AAA"""

read_data = """id,buildingblock1_smiles,buildingblock2_smiles,buildingblock3_smiles,molecule_smiles,protein_name,binds
1,CCO,CCO,CCO,CCO,AAA,1
2,CCO,CCO,CCO,CCO,AAA,0
3,CCO,CCO,CCO,CCO,BBB,1
4,CCO,CCO,CCO,CCO,BBB,0
"""

class TestTrain(TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_train_empty(self, mock_file):
        testargs = ["train", "--input", "/path/to/train.csv", "--output", "/path/to/model.bin", "--targets", "AAA,BBB"]
        with patch.object(sys, 'argv', testargs):
            self.assertRaises(ValueError, train)

    @patch("builtins.open", new_callable=mock_open, read_data="asdf,aaa")
    def test_train_bad_header(self, mock_file):
        testargs = ["train", "--input", "/path/to/train.csv", "--output", "/path/to/model.bin", "--targets", "AAA,BBB"]
        with patch.object(sys, 'argv', testargs):
            self.assertRaises(ValueError, train)

    @patch("builtins.open", new_callable=mock_open, read_data=bad_data)
    def test_train_bad_data(self, mock_file):
        testargs = ["train", "--input", "/path/to/train.csv", "--output", "/path/to/model.bin", "--targets", "AAA,BBB"]
        with patch.object(sys, 'argv', testargs):
            self.assertRaises(ValueError, train)

    @patch("builtins.open", new_callable=mock_open, read_data=read_data)
    def test_train_single_target(self, mock_file):
        testargs = ["train", "--input", "/path/to/train.csv", "--output", "/path/to/model.bin", "--targets", "BAA"]
        with patch.object(sys, 'argv', testargs):
            train()

    @patch("builtins.open", new_callable=mock_open, read_data=read_data)
    def test_train(self, mock_file):
        testargs = ["train", "--input", "/path/to/train.csv", "--output", "/path/to/model.bin", "--targets", "AAA,BBB"]
        with patch.object(sys, 'argv', testargs):
            train()
        handle = mock_file()
        self.assertEqual(handle.write.call_count, 0)
