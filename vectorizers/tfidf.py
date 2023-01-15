from math import log

from tokenizers import PunctTokenizer
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

    """
    TfidfVectorizer custom attributes
    """
    __slots__ = [
        "vidf_"
    ]

    def __repr__(self) -> str:
        return "{}(size={}, stopwords={})".format(
            self.__class__.__name__,
            len(self.corpus_),
            self.stopwords_
        )

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

        self._check_input(input)

        self._ccorpus(
            input=input,
            ignore_stopwords=ignore_stopwords,
            tokenizer=tokenizer
        )

        self.__idf(input=input)

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

    def __idf(
        self,
        input: CorpusInput,
    ) -> None:
        """
        Finding corpus elements IDF (Inverse document frequency) method.
        Calculates IDF value for each of the corpus elements by searching
        element occuracy in all contexts.

        Args:
            input (CorpusInput) : Corpus to run through

        Returns:
            None (only stores IDF value for each corpus element in vidf_ attribute (dict))
        """

        self.vidf_: dtypes.Dict[str, float] = {}

        if not self.corpus_: 
            raise AttributeError(
                "Vectorizer should be fitted to have vocabulary"
            )

        for word in self.corpus_:
            cnt: int = 0
            for sent in input:
                sent_tokens: dtypes.List[str] = self.tk_().tokenize(sent)
                for idx, tok in enumerate(sent_tokens):
                    tok = self._preprocess_tok(
                        tok=tok,
                        tokens=sent_tokens,
                        curr_idx=idx
                    )
                    cnt += word == tok
            self.vidf_[word] = 1 + log((1 + len(input)) / (1 + cnt))

    def __trsent(self, input: str) -> dtypes.List[str]:
        """
        Transforming single given string (sentence/context) method. Calls by tranform(...)
        to vectorize full corpus.

        Args:
            input (str) : String (sentence/context) to be vectorized

        Returns:
            Vectorized string (sentence/context)
        """

        input_tokens: dtypes.List[str] = self.tk_().tokenize(input)
        res_vec = [0] * len(self.corpus_)

        print(input_tokens)

        for idx, tok in enumerate(input_tokens):
            # In case we can't process tokens like "end." and "end" at the end 
            # of string (sentence/context) like different tokens.
            tok = self._preprocess_tok(tok=tok, tokens=input_tokens, curr_idx=idx)
            if tok in self.corpus_:
                res_vec[self.indices_[tok]] += 1

        for tok in input_tokens:
            if tok in self.corpus_:
                res_vec[self.indices_[tok]] /= self.vidf_[tok]

        return res_vec
