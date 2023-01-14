from abc import (
    ABC,
    abstractmethod
)
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")

import dtypes

CorpusInput = dtypes.Union[dtypes.List[str], str]
VectorizedOutput = dtypes.List[dtypes.List[str]]


class BaseVectorizer(ABC):
    """
    Vectorizer base class. It defines abstract methods for performing 
    vectorization. fit(...), tranform(...) and fit_transform(...) methods
    can be overwritten.
    """

    __slots__ = [
        "stopwords_", "corpus_", "tk_", 
        "indices_", "invindices_"
    ]

    @abstractmethod
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True
    ) -> None:
        raise NotImplementedError("Base class methods should be overwritten")

    @abstractmethod
    def transform(self, input: CorpusInput) -> VectorizedOutput:
        raise NotImplementedError("Base class methods should be overwritten")

    @abstractmethod
    def fit_transform(self, input: CorpusInput) -> VectorizedOutput:
        raise NotImplementedError("Base class methods should be overwritten")

    @property
    def lang_stopwords_(self, language: str = "english") -> dtypes.List[str]:
        return stopwords.words(language)
