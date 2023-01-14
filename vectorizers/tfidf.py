import math

import dtypes
from vectorizers import BaseVectorizer


class TfidfVectorizer(BaseVectorizer):
    """
    TF-IDF vectorizer class. Perform TF-IDF vectorization on a given corpus with
    fit(...) and tranform(...) or fit_tranform(...) methods (should be overwritten).
    """

    def __repr__(self) -> str:
        return "{}()".format(
            self.__class__.__name__
        )