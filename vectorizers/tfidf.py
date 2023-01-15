import math

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

    __slots__ = [
        "vidf_"
    ]

    def __repr__(self) -> str:
        return "{}()".format(
            self.__class__.__name__
        )

    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer
    ) -> None:
        self._check_input(input)

        self._ccorpus(
            input=input,
            ignore_stopwords=ignore_stopwords,
            tokenizer=tokenizer
        )

    def transform(self, input: CorpusInput) -> VectorizedOutput:
        self.__idf(input=input)

    def fit_transform(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer
    ) -> VectorizedOutput:
        return ["string"]

    def __idf(
        self,
        input: CorpusInput,
    ) -> None:
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
            self.vidf_[word] = 1 + math.log((1 + len(input)) / (1 + cnt))
