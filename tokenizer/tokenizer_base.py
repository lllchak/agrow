from dtypes import *


class BaseTokenizer:
    def __init__(
        self,
        stop_words: List[str] = None
    ) -> None:
        if not stop_words:
            import nltk
            from nltk.corpus import stopwords
            nltk.download("stopwords")

            self.stop_words = stopwords.words("english")
        else:
            self.stop_words = stop_words

    def tokenize(self):
        for word in self.stop_words: print(word)
