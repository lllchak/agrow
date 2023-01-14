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
    should be overwritten to perform text vectorization.
    """

    """
    BaseVectorizer attributes:
        1. stopwords_  - List of provided corpus stopwords
        2. corpus_     - List of corpus vocabulary (without punctuation).
                         In extracts from given documents at fit(...) stage.
        3. tk_         - Tokenizer used to divide string (sentence/context) 
                         by tokens
        4. indices_    - (Vocabulary element: its index) mapping dictionary
        5. invindices_ - Inversed (vocabulary element: its index) mapping 
                         dictionary (vocab. element index: its value).
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
        """
        Abstract given corpus (could be one sentence or a list of sentences) 
        fitting corpus method. As an advice - could call some helper which
        vectorize only one sentence.

        Args:
            input (CorpusInput)     : Corpus to fit with. Could be one sentence or 
                                      a list of sentences
            ignore_stopwords (bool) : If ignore corpus stopwords or not flag

        Returns:
            None (should only create vocabulary (with indices) from given corpus)
        """

        raise NotImplementedError("Base class methods should be overwritten")

    @abstractmethod
    def transform(self, input: CorpusInput) -> VectorizedOutput:
        """
        Abstract given corpus (could be one sentence or a list of sentences)
        tranforming method. After vectorizer is fitted we can tranform given
        corpus. Realizations could vary a lot due to different vectorization
        approaches (Count, TF-IDF, etc.)

        Args:
            input (CorpusInput) : Corpus to be vectorized. Could be one sentence or 
                                  a list of sentences

        Returns:
            Vectorized corpus
        """

        raise NotImplementedError("Base class methods should be overwritten")

    @abstractmethod
    def fit_transform(
        self, 
        input: CorpusInput, 
        ignore_stopwords: bool = True
    ) -> VectorizedOutput:
        """
        Abstract given corpus (could be one sentence of a list of sentences)
        fitting and tranforming method. According to the idea, simply - a wrapper
        above fit(...) and tranform(...) methods, tranforms given corpus after 
        fitting vectorizer on a it (corpus)

        Args:
            input (CorpusInput)     : Corpus to fit with and which to transform after.
                                      Could be one sentence or a list of sentences
            ignore_stopwords (bool) : If ignore corpus stopwords or not flag

        Returns:
            Vectorized corpus
        """

        raise NotImplementedError("Base class methods should be overwritten")

    """
    Given language stopwords
    """
    @property
    def lang_stopwords_(self, language: str = "english") -> dtypes.List[str]:
        return stopwords.words(language)
