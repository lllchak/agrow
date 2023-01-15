from abc import (
    ABC,
    abstractmethod
)
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")

import dtypes
from .utils import is_punct

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
    stopwords_: dtypes.List[str] = []
    corpus_: dtypes.Set[str] = set()
    tk_: dtypes.Any = None
    indices_: dtypes.Dict[str, int] = {}
    invindices_: dtypes.Dict[int, str] = {}

    def __repr__(self) -> str:
        return "{}(size={}, stopwords={})".format(
            self.__class__.__name__,
            len(self.corpus_),
            self.stopwords_
        )

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

    def _ccorpus(
        self, 
        input: CorpusInput, 
        ignore_stopwords: bool,
        tokenizer: dtypes.Any
    ) -> None:
        """
        Creating corpus vocabulary (fitting wrapper) method. Creates corpus vocabulary
        adding token one-by-one while walking through each of the tokens (in fact, just
        flatten given multidimensional corpus into 1d vector).

        Args:
            input (CorpusInput)     : Corpus to fit with
            ignore_stopwords (bool) : If ignore corpus stopwords or not flag

        Returns:
            None (only creates corpus vocabulary)
        """

        self.tk_: dtypes.Any = tokenizer
        lstopwords: dtypes.List[str] = self.lang_stopwords_

        for sent in input:
            tokens: dtypes.List[str] = self.tk_().tokenize(sent)
            for idx, tok in enumerate(tokens):
                # In case we can't process tokens like "end." and "end" at the end 
                # of string (sentence/context) like different tokens.
                tok = self._preprocess_tok(tok=tok, tokens=tokens, curr_idx=idx)

                if not is_punct(tok) and tok not in self.corpus_:
                    if tok not in lstopwords: self.corpus_.add(tok)
                    else:
                        if ignore_stopwords: self.corpus_.add(tok) 
                        self.stopwords_.append(tok)

        self.indices_ = {word: idx for idx, word in enumerate(sorted(self.corpus_))}
        self.invindices_ = {idx: word for idx, word in enumerate(sorted(self.corpus_))}

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
