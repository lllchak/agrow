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
        "train_", "embed_size_", "history_"
        "model_"
    ]

    """
    Initializes to model with random weights matrices
    """
    
    def fit(
        self,
        input: CorpusInput,
        ignore_stopwords: bool = True,
        tokenizer: dtypes.Any = PunctTokenizer,
        n_iter: int = 50,
        learning_rate: float = 1e-4,
        embedding_size: int = 10,
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
        self.embed_size_ = embedding_size

        self._cvocab(
            input=input,
            ignore_stopwords=ignore_stopwords,
            tokenizer=tokenizer
        )

        self.__gtrain(wsize=window_size)

        self.model_ = self.__init_model()
        self.history_ = []
        for _ in range(n_iter):
            self.history_.append(self.__backward(learning_rate=learning_rate))

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
        n_iter: int = 50,
        learning_rate: float = 1e-4,
        embedding_size: int = 10,
        window_size: int = 2
    ) -> dtypes.List[np.float64]:
        pass

    def sample(self, instance) -> dtypes.List[str]:
        assert instance in self.indices_, f"Word '{instance}' is not in vocabulary, add it to your corpus first"
        oh_instance = self.__onehot(self.indices_[instance], len(self.vocab_))
        return self.__forward([oh_instance], self.model_, return_cache=False)[0]

    def __init_model(self) -> dtypes.Dict[str, np.random.randn]:
        vocab_size: int = len(self.vocab_)

        return {
            "w1": np.random.randn(vocab_size, self.embed_size_),
            "w2": np.random.randn(self.embed_size_, vocab_size)
        }

    def __backward(self, 
        learning_rate: float = 1e-4, 
    ) -> np.float64:
        cache: dtypes.Dict[str, np.ndarray] = self.__forward(
            X=self.train_[0], model=self.model_
        )
        assert isinstance(cache, dict), "Forward pass should return all layers states"

        da2: np.ndarray = cache["ans"] - self.train_[1]
        dw2: np.ndarray = cache["t1"].T @ da2
        da1: np.ndarray = da2 @ self.model_["w2"].T
        dw1: np.ndarray = self.train_[0].T @ da1

        assert dw2.shape == self.model_["w2"].shape, "Weigth matrices dimensions are not equal"
        assert dw1.shape == self.model_["w1"].shape, "Weigth matrices dimensions are not equal"

        self.model_["w1"] -= learning_rate * dw1
        self.model_["w2"] -= learning_rate * dw2

        return self.__cross_entropy(cache["ans"], self.train_[1])

    def __forward(
        self,
        X: np.ndarray,
        model: dtypes.Dict[str, np.ndarray],
        return_cache: bool = True
    ) -> dtypes.Union[dtypes.Dict[str, np.ndarray], np.ndarray]:
        cache: dtypes.Dict[str, np.ndarray] = {"t1": None, "t2": None, "prob": None}

        cache["t1"] = X @ model["w1"]
        cache["t2"] = cache["t1"] @ model["w2"]
        cache["ans"] = self.__softmax(cache["t2"])

        return cache["ans"] if not return_cache else cache

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
            for j in nbr_inds:
                if i == j: continue
                X.append(self.__onehot(self.indices_[vocab_list[i]], vocab_size))
                Y.append(self.__onehot(self.indices_[vocab_list[j]], vocab_size))

        self.train_ = (np.asarray(X), np.asarray(Y))

    def __softmax(self, X: np.ndarray) -> np.ndarray:
        ans: dtypes.List = []
        
        for vec in X:
            exp: np.array = np.exp(vec)
            ans.append(exp / exp.sum())

        return np.array(ans)

    def __cross_entropy(self, logit: np.ndarray, gt: np.ndarray) -> np.float64:
        return -np.sum(np.log(logit) * gt)

    def __onehot(self, word_id: int, vocab_len: int) -> dtypes.List[int]:
        ans: dtypes.List[int] = [0] * vocab_len
        ans[word_id] = 1

        return ans
