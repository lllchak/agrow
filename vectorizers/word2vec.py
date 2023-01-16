import numpy as np

from tokenizers import PunctTokenizer
from vectorizers import (
    BaseVectorizer,
    dtypes,
)

CorpusInput = dtypes.Union[dtypes.List[str], str]


class Word2Vec(BaseVectorizer):
    """
    Word2Vec embedder. Transforms word into float vector representation.
    Allows to process words like numbers, calculate the "distance" 
    between words, preserving the semantics of the language.
    """

    __slots__ = [
        "train_"
    ]

    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer,
        window_size: int = 3
    ) -> None:
        """
        You can find more complete docs at ./base.py

        Fitting on a given corpus method.

        Args:
            input (CorpusInput)     : Corpus to fit with
            ignore_stopwords (bool) : If ignore corpus stopwords or not flag

        Returns:
            None (only creates corpus vocabulary)
        """

        input = self._check_input(input)

        self._cvocab(
            input=input,
            ignore_stopwords=ignore_stopwords,
            tokenizer=tokenizer
        )

        self.__gtrain(wsize=window_size)

    def transform(self, input: str) -> dtypes.List[np.float64]:
        """
        You can find more complete docs at ./base.py

        Tranforming given corpus method.

        Args:
            input (CorpusInput) : Corpus to be vectorized

        Returns:
            Vectorized corpus
        """

        input = self._check_input(input)

        return [self.__trsent(sent) for sent in input]

    def fit_transform(
        self,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer,
        window_size: int = 3
    ) -> dtypes.List[np.float64]:
        pass


    def __gtrain(self, wsize: int) -> None:
        X: dtypes.List[int] = []
        Y: dtypes.List[int] = []

        for i in range(len(self.vocab_)):
            nbr_inds = list(range(max(0, i - wsize), i)) + \
                       list(range(i + 1, min(len(self.vocab_), wsize + 1)))
            for j in nbr_inds:
                X.append(self.indices_[list(self.vocab_)[i]])
                Y.append(self.indices_[list(self.vocab_)[j]])

        X = np.array(X)
        X = np.expand_dims(X, axis=0)
        Y = np.array(Y)
        Y = np.expand_dims(Y, axis=0)

        self.train_ = (X, Y)
        