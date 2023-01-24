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
        window_size: int = 2
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
        window_size: int = 2
    ) -> dtypes.List[np.float64]:
        pass


    def __gtrain(self, wsize: int) -> None:
        X: dtypes.List[int] = []
        Y: dtypes.List[int] = []
        vocab_size: int = len(self.vocab_)
        vocab_list: dtypes.List[str] = list(self.vocab_)

        for i in range(vocab_size):
            nbr_inds = (
                list(range(max(0, i - wsize), i)) + \
                list(range(i, min(vocab_size, i + wsize + 1)))
            )
            print(nbr_inds)
            for j in nbr_inds:
                if i == j: continue
                print(j)
                X.append(self.__onehot(self.indices_[vocab_list[i]], vocab_size))
                Y.append(self.__onehot(self.indices_[vocab_list[j]], vocab_size))

        self.train_ = (np.asarray(X), np.asarray(Y))

    def __onehot(self, word_id: int, vocab_len: int) -> dtypes.List[int]:
        ans: dtypes.List[int] = [0] * vocab_len
        ans[word_id] = 1

        return ans
