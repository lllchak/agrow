from vectorizers import (
    BaseVectorizer,
    dtypes
)
from tokenizers import PunctTokenizer

CorpusInput = dtypes.Union[dtypes.List[str], str]
VectorizedOutput = dtypes.List[dtypes.List[str]]


class OneHotVectorizer(BaseVectorizer):
    """
    One-hot vectorizer based on one-hot approach. Transforms input
    corpus into one-hot vector(-s) of tokens.

    Note: Builds a vector for each word in string (sentence/context), hence
          tranforming a string (sentence/context) will return list of list of
          vectorized string words.
    """

    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer
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

    def transform(self, input: CorpusInput) -> VectorizedOutput:
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
        input: CorpusInput,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer
    ) -> VectorizedOutput:
        """
        You can find more complete docs at ./base.py

        Fitting and tranforming corpus wrapper method

        Args:
            input (CorpusInput)     : Corpus to fit with and which to transform after
            ignore_stopwords (bool) : If ignore corpus stopwords or not flag

        Returns:
            Vectorized corpus
        """

        input = self._check_input(input)

        self.fit(
            input=input,
            ignore_stopwords=ignore_stopwords,
            tokenizer=tokenizer
        )

        return self.transform(input)

    def __trsent(self, input: str) -> dtypes.List[str]:
        """
        Transforming single given string (sentence/context) method. Calls by tranform(...)
        to vectorize full corpus.

        Args:
            input (str) : String (sentence/context) to be vectorized

        Returns:
            Vectorized string (sentence/context)
        """

