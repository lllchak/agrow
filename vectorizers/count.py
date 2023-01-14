import gc

import dtypes
from .utils import is_punct
from vectorizers import BaseVectorizer
from tokenizers import PunctTokenizer

CorpusInput = dtypes.Union[dtypes.List[str], str]


class CountVectorizer(BaseVectorizer):
    """
    Count vectorizer based on Bag-of-Words (BoW) approach. It simply transforms
    input corpus into vector(-s) of token occurances.
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
    ):
        if isinstance(input, str): input = [input]
        if not all(isinstance(sent, str) for sent in input):
            raise TypeError(
                "Input corpus should be a list of strings or a string."
            )

        self.__ccorpus(input=input, ignore_stopwords=ignore_stopwords)

    def transform(self, input: CorpusInput) -> dtypes.List[dtypes.List[str]]:
        if isinstance(input, str): input = [input]
        if not all(isinstance(sent, str) for sent in input):
            raise TypeError(
                "Input corpus should be a list of strings or a string."
            )

        return [self.__trsent(sent) for sent in input]

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
            for idx, tok in enumerate(tokens):
                # In case we can't process tokens like "end." and "end" at the end 
                # of string (sentence/context) like different tokens.
                tok = self.__preprocess_tok(tok=tok, tokens=tokens, curr_idx=idx)

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

    def __trsent(self, input: dtypes.List[str]) -> dtypes.List[int]:
        input_tokens: dtypes.List[str] = self.tk_.tokenize(input)
        res_vec = [0] * len(self.corpus_)

        for idx, tok in enumerate(input_tokens):
            tok = self.__preprocess_tok(tok=tok, tokens=input_tokens, curr_idx=idx)
            if tok in self.corpus_:
                res_vec[self.indices_[tok]] += 1

        return res_vec

    def __preprocess_tok(
        self,
        tok: str,
        tokens: dtypes.List[str],
        curr_idx: int
    ) -> str:
        tok = tok.lower()
        if tok[-1] == '.' and curr_idx == len(tokens) - 1: tok = tok[:-1]

        return tok

        
        