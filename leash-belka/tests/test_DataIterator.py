from unittest import TestCase
from unittest.mock import patch

from leash_BELKA.DataIterator import DataIterator

file_paths = ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv', 'file5.csv']

def input_data(data, label):
    pass

class TestDataIterator(TestCase):
    def test_constructor(self):
        data_iterator = DataIterator(file_paths)
        self.assertIsNotNone(data_iterator)
        self.assertEqual(data_iterator._file_paths, file_paths)
        self.assertEqual(data_iterator._it, 0)

    @patch("leash_BELKA.DataIterator.pd.read_csv") #, new_callable=mock_open, read_data="")
    def test_next(self, mock_read_csv):
        data_iterator = DataIterator(file_paths)
        self.assertEqual(mock_read_csv.call_count, 0)
        self.assertEqual(data_iterator.next(input_data), 1)
        self.assertEqual(data_iterator._it, 1)
        mock_read_csv.assert_called_once_with(file_paths[0])
        self.assertEqual(data_iterator.next(input_data), 1)
        self.assertEqual(data_iterator.next(input_data), 1)
        self.assertEqual(data_iterator.next(input_data), 1)
        self.assertEqual(data_iterator.next(input_data), 1)
        self.assertEqual(data_iterator.next(input_data), 0)

    @patch("leash_BELKA.DataIterator.pd.read_csv") #, new_callable=mock_open, read_data="")
    def test_reset(self, mock_read_csv):
        data_iterator = DataIterator(file_paths)
        self.assertEqual(data_iterator.next(input_data), 1)
        self.assertEqual(data_iterator._it, 1)
        data_iterator.reset()
        self.assertEqual(data_iterator._it, 0)

