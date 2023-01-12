from abc import (
    ABC,
    abstractmethod
)
import dtypes


class BaseTokenizer(ABC):
    """
    Tokenizer abstract class. It defines method for performing
    tokenization and getting dictionary stopwords (from nltk library).
    tokenize(self, string) and/or stokenize(strings) (for many sentences)
    could be overridden.

    Note: Override tokenize(...) and/or stokenize(...) (if neeeded) to perform 
          tokenization.
    """

    @abstractmethod
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def tokenize(self, string: str) -> dtypes.List[str]:
        """
        Abstract single string (sentence/context) tokenization method. 
        Runs stokenize with a single string (sentence/context). Can be 
        overritten by user.

        Args:
            string (str) : String (sentence/context) to be tokenized

        Returns:
            List of tokens, i.e "string to tokenize" -> ["string", "to", "tokenize"]
        """

        return self.stokenize([string])[0]

    def stokenize(self, strings: dtypes.List[str]) -> dtypes.List[dtypes.List[str]]:
        """
        Abstract list of strings (group of sentences/contexts) tokenization
        method. Runs tokenize for each string (sentence/context) in a list
        of strings.

        Args:
            strings (List[str]) : List of strings (sentences/contexts) to be
                                  tokenized

        Returns:
            List of tokenized strings (sentences/contexts), i.e:
            
            ["first string of tokens", "second string of tokens"] ->
            [["first", "string", "of", "tokens"], ["second", "string", "of", "tokens"]]
        """

        return [self.tokenize(string) for string in strings]

    @classmethod
    def gstopwords(language: str) -> dtypes.List[str]:
        """
        Method to get given language stopwords

        Args:
            language (str) : Language to get stopwords from

        Returns:
            List of stopwords
        """

        import nltk
        from nltk.corpus import stopwords
        nltk.download("stopwords")

        return stopwords.words(language)
