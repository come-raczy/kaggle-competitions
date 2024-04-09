import os
from typing import Callable, List

import pandas as pd
import xgboost


class DataIterator(xgboost.DataIter):
    """A custom data iterator for XGBoost.

    This iterator reads data from a list of CSV
    files and passes the data to XGBoost. This iterator is used to demonstrate how to
    implement a custom data iterator for XGBoost.

        """
    def __init__(self, csv_file_paths: List[str]) -> None:
        self._file_paths = csv_file_paths
        self._it = 0
        # XGBoost will generate some cache files under current directory with the prefix
        # "cache"
        super().__init__(cache_prefix=os.path.join(".", "cache"))

    def next(self, input_data: Callable) -> int:
        """Advance the iterator by 1 step and pass the data to XGBoost.  This function is
        called by XGBoost during the construction of ``DMatrix``

        """
        if self._it == len(self._file_paths):
          # return 0 to let XGBoost know this is the end of iteration
          return 0

        # input_data is a function passed in by XGBoost who has the exact same signature of
        # ``DMatrix``
        file_path = self._file_paths[self._it]
        df = pd.read_csv(file_path)
        X, y = df.iloc[:, 1:-1], df.iloc[:, -1]
        #X, y = load_svmlight_file(self._file_paths[self._it])
        input_data(data=X, label=y)
        self._it += 1
        # Return 1 to let XGBoost know we haven't seen all the files yet.
        return 1

    def reset(self) -> None:
        """Reset the iterator to its beginning"""
        self._it = 0

#it = Iterator(["file_0.svm", "file_1.svm", "file_2.svm"])
#Xy = xgboost.DMatrix(it)

# The ``approx`` also work, but with low performance. GPU implementation is different from CPU.
# as noted in following sections.
#booster = xgboost.train({"tree_method": "hist"}, Xy)
