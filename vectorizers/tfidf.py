import math

from vectorizers import (
    BaseVectorizer,
    dtypes
)

CorpusInput = dtypes.Union[dtypes.List[str], str]
VectorizedOutput = dtypes.List[dtypes.List[str]]


class TfidfVectorizer(BaseVectorizer):
    """
    TF-IDF vectorizer class. Perform TF-IDF vectorization on a given corpus with
    fit(...) and tranform(...) or fit_tranform(...) methods (should be overwritten).
    """

    def __repr__(self) -> str:
        return "{}()".format(
            self.__class__.__name__
        )

    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True 
    ) -> None:
        pass

    def __ccorpus(self):
        pass