from vectorizers import BaseVectorizer, dtypes
from tokenizers import PunctTokenizer

CorpusInput = dtypes.Union[dtypes.List[str], str]
VectorizedOutput = dtypes.List[dtypes.List[int]]


class CountVectorizer(BaseVectorizer):
    """
    Count vectorizer based on Bag-of-Words (BoW) approach class.
    Transforms input corpus into vector(-s) of token occurances.
    """

    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer,
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
            input=input, ignore_stopwords=ignore_stopwords, tokenizer=tokenizer
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

        return [self.__trsent(sent) for sent in input]

    def fit_transform(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer,
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

        return self.transform(input)

    def __trsent(self, input: str) -> dtypes.List[int]:
        """
        Transforming single given string (sentence/context) method. Calls by tranform(...)
        to vectorize full corpus.

        Args:
            input (str) : String (sentence/context) to be vectorized

        Returns:
            Vectorized string (sentence/context)
        """

        input_tokens: dtypes.List[str] = self.tk_().tokenize(input)
        res_vec = [0] * len(self.vocab_)

        for idx, tok in enumerate(input_tokens):
            # In case we can't process tokens like "end." and "end" at the end
            # of string (sentence/context) like different tokens.
            tok = self._preprocess_tok(tok=tok, tokens=input_tokens, curr_idx=idx)
            if tok in self.vocab_:
                res_vec[self.indices_[tok]] += 1

        return res_vec
