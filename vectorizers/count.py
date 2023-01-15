import gc

from .utils import is_punct
from vectorizers import (
    BaseVectorizer,
    dtypes
)
from tokenizers import PunctTokenizer

CorpusInput = dtypes.Union[dtypes.List[str], str]
VectorizedOutput = dtypes.List[dtypes.List[str]]


class CountVectorizer(BaseVectorizer):
    """
    Count vectorizer based on Bag-of-Words (BoW) approach class. It simply 
    transforms input corpus into vector(-s) of token occurances.
    """

    def __repr__(self) -> str:
        return "{}(size={}, stopwords={})".format(
            self.__class__.__name__,
            len(self.corpus_),
            self.stopwords_
        )

    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True
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

        input = self._BaseVectorizer__check_input(input)

        self.__ccorpus(input=input, ignore_stopwords=ignore_stopwords)

    def transform(self, input: CorpusInput) -> VectorizedOutput:
        """
        You can find more complete docs at ./base.py

        Tranforming given corpus method.

        Args:
            input (CorpusInput) : Corpus to be vectorized

        Returns:
            Vectorized corpus
        """

        input = self._BaseVectorizer__check_input(input)

        return [self.__trsent(sent) for sent in input]

    def fit_transform(
        self, 
        input: CorpusInput,
        ignore_stopwords: bool = True
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

        input = self._BaseVectorizer__check_input(input)

        self.fit(input=input, ignore_stopwords=ignore_stopwords)
        return self.transform(input)

    def __ccorpus(
        self, 
        input: CorpusInput, 
        ignore_stopwords: bool
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

        self.tk_: dtypes.Any = PunctTokenizer()
        self.corpus_: dtypes.List[str] = []
        lstopwords: dtypes.List[str] = self.lang_stopwords_
        self.stopwords_: dtypes.List[str] = []
        tunique: dtypes.Set = set()

        for sent in input:
            tokens: dtypes.List[str] = self.tk_.tokenize(sent)
            for idx, tok in enumerate(tokens):
                # In case we can't process tokens like "end." and "end" at the end 
                # of string (sentence/context) like different tokens.
                tok = self._BaseVectorizer__preprocess_tok(tok=tok, tokens=tokens, curr_idx=idx)

                if not is_punct(tok) and tok not in tunique:
                    if tok not in lstopwords: self.corpus_.append(tok)
                    else:
                        if ignore_stopwords: self.corpus_.append(tok) 
                        self.stopwords_.append(tok)
                    tunique.add(tok)

        self.indices_ = {word: idx for idx, word in enumerate(sorted(self.corpus_))}
        self.invindices_ = {idx: word for idx, word in enumerate(sorted(self.corpus_))}

        del tunique
        gc.collect()

    def __trsent(self, input: str) -> dtypes.List[int]:
        """
        Transforming single given string (sentence/context) method. Calls by tranform(...)
        to vectorize full corpus.

        Args:
            input (str) : String (sentence/context) to be vectorized

        Returns:
            Vectorized string (sentence/context)
        """

        input_tokens: dtypes.List[str] = self.tk_.tokenize(input)
        res_vec = [0] * len(self.corpus_)

        for idx, tok in enumerate(input_tokens):
            # In case we can't process tokens like "end." and "end" at the end 
            # of string (sentence/context) like different tokens.
            tok = self._BaseVectorizer__preprocess_tok(tok=tok, tokens=input_tokens, curr_idx=idx)
            if tok in self.corpus_:
                res_vec[self.indices_[tok]] += 1

        return res_vec
        