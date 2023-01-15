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
    vectorization. 
    
    Note: fit(...), tranform(...) and fit_transform(...) methods
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
        "tk_"
    ]

    corpus_: dtypes.Set[str] = set()
    stopwords_: dtypes.List[str] = []
    indices_: dtypes.Dict[str, int] = {}
    invindices_: dtypes.Dict[int, str] = {}

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
        approaches (Count, TF-IDF, etc.).

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
        fitting vectorizer on a it (corpus).

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

    def _preprocess_tok(
        self,
        tok: str,
        tokens: dtypes.List[str],
        curr_idx: int
    ) -> str:
        """
        Preprocessing separate token method.

        Args:
            tok (str)                 : Token to be preprocessed
            tokens (dtypes.List[str]) : All string (sentence/context) tokens array
            curr_idx (int)            : Source tokens array index

        Returns:
            Preprocessed token
        """

        tok = tok.lower()
        if tok[-1] == '.' and curr_idx == len(tokens) - 1: tok = tok[:-1]

        return tok

    def _check_input(self, input: CorpusInput) -> dtypes.List[str]:
        """
        Checking provided corpus validity method.

        Args:
            input (CorpusInput) : Corpus to be checked

        Returns:
            None (raises error if corpus is invalid) or corpus in appropriate view 
        """

        if isinstance(input, str): input = [input]
        if not all(isinstance(sent, str) for sent in input):
            raise TypeError(
                "Input corpus should be a list of strings or a string."
            )

        return input
