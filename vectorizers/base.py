import gc
from abc import (
    ABC,
    abstractmethod
)
import nltk

import dtypes
from .utils import is_punct
from tokenizers import PunctTokenizer

CorpusInput = dtypes.Union[dtypes.List[str], str]


class BaseVectorizer(ABC):
    """
    Vectorizer base class. It defines abstract methods for performing 
    vectorization.
    """

    __slots__ = [
        "stopwords_", "corpus_", "tk_", 
        "indices_", "invindices_"]

    # @abstractmethod
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    # @abstractmethod
    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True
    ) -> None:

        if isinstance(input, str): input = [input]
        if not all(isinstance(sent, str) for sent in input):
            raise TypeError(
                "Input corpus should be a list of strings or a string."
            )

        self.__ccorpus(input=input, ignore_stopwords=ignore_stopwords)

    def __ccorpus(
        self, 
        input: CorpusInput, 
        ignore_stopwords: bool
    ) -> None:
        self.tk_: dtypes.Any = PunctTokenizer()
        self.corpus_: dtypes.List[str] = []
        lstopwords: dtypes.List[str] = self.lang_stopwords_
        self.stopwords_: dtypes.List[str] = []
        tunique: dtypes.Set = set()

        for sent in input:
            tokens: dtypes.List[str] = self.tk_.tokenize(sent)
            for tok in tokens:
                if not is_punct(tok) and tok not in tunique:
                    if tok not in lstopwords: self.corpus_.append(tok.lower())
                    else:
                        if ignore_stopwords: self.corpus_.append(tok.lower()) 
                        self.stopwords_.append(tok.lower())
                    tunique.add(tok)

        self.indices_ = {word: idx for idx, word in enumerate(sorted(self.corpus_))}
        self.invindices_ = {idx: word for idx, word in enumerate(sorted(self.corpus_))}

        del tunique
        gc.collect()

    @property
    def lang_stopwords_(self, language: str = "english") -> dtypes.List[str]:
        import nltk
        from nltk.corpus import stopwords
        nltk.download("stopwords")

        return stopwords.words(language)
